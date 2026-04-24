"""
agent_expander.py — Pre-processing pass for multi-agent BehaVerify models.

When a .tree file contains agent_types { } and agents { } blocks, this module
expands the templates into a flat single-agent model that the existing pipeline
(dsl_to_nuxmv, dsl_to_python, etc.) can process unchanged.

The expansion strategy ("expand early, not deep"):
  1. Parse the multi-agent .tree file with the extended grammar.
  2. Expand:
     - env array variables (x_pos[agents]) → x_pos_r0, x_pos_r1, …
     - agent-local bl variables (act) → act_r0, act_r1, …
     - environment_update [i] loops → N concrete statements
     - agent_type templates → concrete checks, actions, subtrees per instance
     - forall/exists over agents in specifications → conjunctions/disjunctions
  3. Return an ExpandedModel object whose model_to_tree_text() produces
     valid standard .tree text that the existing pipeline accepts.

Public API:
    expand_agents(model)          -> ExpandedModel
    model_to_tree_text(expanded)  -> str
    maybe_expand(file_path)       -> str (original or temp-file path)
"""

import re
import os
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# ExpandedModel data classes
# ---------------------------------------------------------------------------

class ExpandedVariable:
    """A single variable in the expanded flat model."""
    def __init__(self, name, scope, domain_text, initial_value=None, initial_text=None):
        self.name = name
        self.scope = scope            # 'bl', 'env', or 'local'
        self.domain_text = domain_text  # e.g. "{'We','Ea','XX'}" or "[0, 4]"
        self.initial_value = initial_value  # numeric/string for simple scalars
        self.initial_text = initial_text    # raw .tree assign text if complex

    def to_tree_text(self):
        if self.initial_text:
            assign = self.initial_text
        elif isinstance(self.initial_value, str):
            assign = f"assign{{result{{'{self.initial_value}'}}}}"
        else:
            assign = f"assign{{result{{{self.initial_value}}}}}"
        return f"variable {{ {self.scope} {self.name} VAR {self.domain_text} {assign}}}"


class ExpandedCheck:
    """A single environment_check in the expanded model."""
    def __init__(self, name, condition_text, read_vars=None):
        self.name = name
        self.condition_text = condition_text
        self.read_vars = read_vars or []

    def to_tree_text(self):
        rv = ', '.join(self.read_vars) if self.read_vars else ''
        return (
            f"environment_check {{ {self.name}\n"
            f"        arguments {{}} read_variables {{{rv}}}\n"
            f"        condition {{{self.condition_text}}}}}"
        )


class ExpandedAction:
    """A single action in the expanded model."""
    def __init__(self, name, write_vars, update_text):
        self.name = name
        self.write_vars = write_vars  # list of var names
        self.update_text = update_text  # raw .tree update body text

    def to_tree_text(self):
        wv = ', '.join(self.write_vars)
        return (
            f"action {{ {self.name}\n"
            f"        arguments {{}} local_variables {{}} read_variables {{}}"
            f" write_variables {{{wv}}}\n"
            f"        initial_values {{}}\n"
            f"        update {{\n"
            f"            {self.update_text}\n"
            f"        }}}}"
        )


class ExpandedSpec:
    """A single specification (INVARSPEC / CTLSPEC / LTLSPEC)."""
    def __init__(self, spec_type, body_text):
        self.spec_type = spec_type
        self.body_text = body_text

    def __str__(self):
        return f"{self.spec_type} {{{self.body_text}}}"


class ExpandedTreeNode:
    """A node in the expanded behavior tree."""
    def __init__(self, node_type, name, children=None, leaf_name=None,
                 parallel_policy='success_on_all'):
        self.node_type = node_type    # 'parallel', 'selector', 'sequence', 'leaf'
        self.name = name
        self.children = children or []
        self.leaf_name = leaf_name    # for leaf nodes: name of check/action
        self.parallel_policy = parallel_policy

    def to_tree_text(self, indent=4):
        pad = ' ' * indent
        if self.node_type == 'leaf':
            return f"{pad}{self.leaf_name} {{}}"
        elif self.node_type == 'parallel':
            child_text = '\n'.join(c.to_tree_text(indent + 4) for c in self.children)
            return (
                f"{pad}composite {{ {self.name} parallel policy"
                f" {self.parallel_policy} children {{\n"
                f"{child_text}\n"
                f"{pad}}}}}"
            )
        else:
            child_text = '\n'.join(c.to_tree_text(indent + 4) for c in self.children)
            return (
                f"{pad}composite {{ {self.name} {self.node_type} children {{\n"
                f"{child_text}\n"
                f"{pad}}}}}"
            )


class ExpandedModel:
    """The fully expanded flat model ready for model_to_tree_text()."""
    def __init__(self):
        self.configuration_text = ''
        self.enumerations = []
        self.constants_text = ''
        self.variables = []             # list of ExpandedVariable
        self.environment_update_text = ''
        self.check_nodes = []
        self.environment_checks = []    # list of ExpandedCheck
        self.action_nodes = []          # list of ExpandedAction
        self.sub_trees_text = ''
        self.tree = None                # ExpandedTreeNode (root)
        self.tick_prerequisite_text = '(True)'
        self.specifications = []        # list of ExpandedSpec
        self.agent_types = []           # always empty after expansion


# ---------------------------------------------------------------------------
# Helper: resolve constants from model
# ---------------------------------------------------------------------------

def _resolve_constants(model):
    """Return a dict of constant name -> numeric or string value."""
    consts = {}
    for c in model.constants:
        val = c.val
        if hasattr(val, 'val') and val.val is not None:
            consts[c.name] = val.val
        elif isinstance(val, (int, float)):
            consts[c.name] = val
        else:
            # Try extracting the raw value
            raw = str(val)
            try:
                consts[c.name] = int(raw)
            except ValueError:
                try:
                    consts[c.name] = float(raw)
                except ValueError:
                    consts[c.name] = raw.strip("'\"")
    return consts


def _resolve_value(value_obj, consts):
    """Resolve a constant_or_reference to a Python value."""
    if value_obj is None:
        return None
    if value_obj.constant is not None:
        v = value_obj.constant
        if hasattr(v, 'val') and v.val is not None:
            return v.val
        return v
    if value_obj.reference:
        ref = value_obj.reference
        if ref in consts:
            return consts[ref]
        return ref
    return None


# ---------------------------------------------------------------------------
# Helper: code_statement to text (AST serializer)
# ---------------------------------------------------------------------------

def _cs_to_text(cs):
    """Convert a code_statement AST node back to .tree expression text."""
    if cs is None:
        return 'None'

    # agent_param_ref: agents[i].param_name
    if cs.agent_param_ref:
        return f'agents[{cs.agent_param_index}].{cs.agent_param_name}'

    # indexed_var: x_pos[i] or x_pos[i] at -1
    if cs.indexed_var:
        txt = f'{cs.indexed_var}[{cs.indexed_var_index}]'
        if cs.read_at_idx is not None:
            txt += f' at {_cs_to_text(cs.read_at_idx)}'
        return txt

    # function_call — wrap in parens to produce valid .tree syntax
    if cs.function_call:
        return '(' + _func_to_text(cs.function_call) + ')'

    # nested (code_statement)
    if cs.code_statement:
        return f'({_cs_to_text(cs.code_statement)})'

    # atom
    if cs.atom is not None:
        atom = cs.atom
        if atom.constant is not None:
            v = atom.constant
            if hasattr(v, 'val') and v.val is not None:
                raw = str(v.val)
                # Strings need quoting
                if isinstance(v.val, str):
                    return f"'{v.val}'"
                return raw
            # TextX returns the primitive value directly for constant_value rules
            if isinstance(v, str):
                return f"'{v}'"
            raw = str(v)
            return raw
        if atom.reference:
            txt = atom.reference
            if cs.node_name is not None:
                txt += f' node {_cs_to_text(cs.node_name)}'
            if cs.read_at is not None:
                txt += f' at {_cs_to_text(cs.read_at)}'
            if cs.trace_num is not None:
                txt += f' trace {_cs_to_text(cs.trace_num)}'
            return txt

    return 'UNKNOWN'


def _func_to_text(func):
    """Convert a function AST node back to .tree function text (without parens)."""
    fname = func.function_name

    # loop
    if fname == 'loop':
        domain = _loop_domain_text(func)
        cond = _cs_to_text(func.loop_condition)
        val = _cs_to_text(func.values)
        rev = 'reverse ' if func.reverse else ''
        return f'loop, {func.loop_variable}, {rev}{domain} such_that {cond}, {val}'

    # case_loop
    if fname == 'case_loop':
        domain = _loop_domain_text(func)
        cond = _cs_to_text(func.loop_condition)
        cv = _cs_to_text(func.cond_value)
        val = _cs_to_text(func.values)
        dv = _cs_to_text(func.default_value)
        rev = 'reverse ' if func.reverse else ''
        return f'case_loop, {func.loop_variable}, {rev}{domain} such_that {cond}, {cv}, {val}, {dv}'

    # index
    if fname == 'index':
        idx = _cs_to_text(func.to_index)
        ci = 'constant_index ' if func.constant_index == 'constant_index' else ''
        val = _cs_to_text(func.values)
        parts = [f'index, {idx}']
        if func.node_name:
            parts.append(_cs_to_text(func.node_name))
        if func.read_at:
            parts.append(_cs_to_text(func.read_at))
        if func.trace_num:
            parts.append(_cs_to_text(func.trace_num))
        parts.append(f'{ci}{val}')
        return ', '.join(parts)

    # bounded functions
    if fname in ('globally_bounded', 'finally_bounded', 'until_bounded',
                 'release_bounded', 'historically_bounded', 'once_bounded',
                 'since_bounded', 'triggered_bounded'):
        lb = _cs_to_text(func.bound.lower_bound)
        ub = _cs_to_text(func.bound.upper_bound)
        val = _cs_to_text(func.values)
        return f'{fname}, [{lb}, {ub}], {val}'

    # status functions
    if fname in ('active', 'success', 'running', 'failure'):
        return f'{fname}, {_cs_to_text(func.node_name)}'

    # regular functions (including forall, exists, and, or, etc.)
    args = ', '.join(_cs_to_text(v) for v in func.values)
    return f'{fname}, {args}'


def _loop_domain_text(func):
    if func.loop_variable_domain:
        inner = ', '.join(_cs_to_text(v) for v in func.loop_variable_domain)
        return f'{{{inner}}}'
    return f'[{_cs_to_text(func.min_val)}, {_cs_to_text(func.max_val)}]'


# ---------------------------------------------------------------------------
# Helper: assign_value to text
# ---------------------------------------------------------------------------

def _assign_to_text(assign_val):
    """Convert assign_value AST back to .tree assign text."""
    if assign_val is None:
        return 'assign{result{0}}'
    parts = []
    for cr in assign_val.case_results:
        cond = _cs_to_text(cr.condition)
        vals = ', '.join(_cs_to_text(v) for v in cr.values)
        parts.append(f'case {{{cond}}} result {{{vals}}}')
    dr = assign_val.default_result
    if dr:
        vals = ', '.join(_cs_to_text(v) for v in dr.values)
        parts.append(f'result {{{vals}}}')
    return 'assign{\n            ' + '\n            '.join(parts) + '}'


# ---------------------------------------------------------------------------
# Substitution helpers
# ---------------------------------------------------------------------------

def _substitute(text, substitutions):
    """Apply a dict of {old: new} substitutions to text."""
    # Sort by length descending to avoid partial matches
    for old, new in sorted(substitutions.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text


def _build_agent_subs(agent_name, agent_vars, env_arrays, consts, params):
    """
    Build substitution dict for expanding a template to agent 'agent_name'.

    agent_vars  : list of agent-local bl variable base names (e.g. ['act'])
    env_arrays  : list of env array base names (e.g. ['x_pos'])
    consts      : {name: value} for constants
    params      : {param_name: value} for this agent's parameters
    """
    subs = {}
    # [self] → _rN
    for var in env_arrays:
        subs[f'{var}[self]'] = f'{var}_{agent_name}'
    # agent-local vars → suffixed
    for var in agent_vars:
        subs[var] = f'{var}_{agent_name}'
    # parameter names → their resolved values
    for pname, pval in params.items():
        if pname in consts:
            # Already handled via direct value — but also substitute the name
            pass
        subs[pname] = str(pval)
    return subs


# ---------------------------------------------------------------------------
# Core expansion logic
# ---------------------------------------------------------------------------

def expand_agents(model):
    """
    Expand a parsed multi-agent model into a flat ExpandedModel.

    Args:
        model: TextX-parsed BehaviorModel with agent_types and agents.

    Returns:
        ExpandedModel ready for model_to_tree_text().
    """
    expanded = ExpandedModel()

    # If no agent_types/agents, just wrap original model (pass-through)
    if not model.agent_types and not model.agents:
        return _passthrough(model)

    # --- Step 1: resolve constants ---
    consts = _resolve_constants(model)

    # --- Step 2: parse agent instances and their parameters ---
    agent_names = []
    agent_params = {}  # agent_name -> {param_name: resolved_value}
    for inst in model.agents:
        name = inst.name
        agent_names.append(name)
        params = {}
        for pa in inst.param_assignments:
            params[pa.name] = _resolve_value(pa.value, consts)
        agent_params[name] = params

    # --- Step 3: find env array variables (those with agents_array == 'agents') ---
    env_arrays = {}   # base_name -> {domain_text, init_param}
    non_array_vars = []

    for var in model.variables:
        if var.agents_array == 'agents':
            domain_text = _domain_to_text(var.domain)
            # The assign has agents[i].start_x — extract param name from assign text
            init_param = _extract_agent_param_from_assign(var.assign)
            env_arrays[var.name] = {
                'domain_text': domain_text,
                'init_param': init_param,
                'scope': var.var_type,
            }
        else:
            non_array_vars.append(var)

    # --- Step 4: get agent_type template ---
    # We only support one agent type for now
    at = model.agent_types[0] if model.agent_types else None

    # Agent-local bl variable base names from agent_type
    agent_local_vars = []
    if at:
        for v in at.agent_variables:
            agent_local_vars.append(v.name)

    # --- Step 5: build expanded variables ---
    # Non-array top-level variables (pass through)
    for var in non_array_vars:
        ev = _expand_variable(var)
        if ev:
            expanded.variables.append(ev)

    # Env array variables → one per agent
    for arr_name, arr_info in env_arrays.items():
        for agent_name in agent_names:
            params = agent_params[agent_name]
            init_param = arr_info['init_param']
            if init_param and init_param in params:
                init_val = params[init_param]
            else:
                init_val = 0
            ev = ExpandedVariable(
                name=f'{arr_name}_{agent_name}',
                scope=arr_info['scope'],
                domain_text=arr_info['domain_text'],
                initial_value=init_val,
            )
            expanded.variables.append(ev)

    # Agent-local bl variables → one per agent
    if at:
        for v in at.agent_variables:
            domain_text = _domain_to_text(v.domain)
            init_text = _assign_to_text(v.assign)
            for agent_name in agent_names:
                ev = ExpandedVariable(
                    name=f'{v.name}_{agent_name}',
                    scope=v.var_type,
                    domain_text=domain_text,
                    initial_text=init_text,
                )
                expanded.variables.append(ev)

    # --- Step 6: expand environment_update ---
    expanded.environment_update_text = _expand_env_update(
        model, agent_names, env_arrays, agent_local_vars, consts
    )

    # --- Step 7: pass through top-level checks ---
    # (model.check_nodes are usually empty in multi-agent files)

    # --- Step 8: expand environment_checks from agent_type template ---
    if at:
        for ck in at.agent_environment_checks:
            for agent_name in agent_names:
                params = agent_params[agent_name]
                cond_text = _cs_to_text(ck.condition)
                # substitute: x_pos[self] → x_pos_rN, goal_x → val, etc.
                subs = {}
                for arr_name in env_arrays:
                    subs[f'{arr_name}[self]'] = f'{arr_name}_{agent_name}'
                for v in at.agent_variables:
                    subs[v.name] = f'{v.name}_{agent_name}'
                for pname, pval in params.items():
                    if pname not in subs:
                        if isinstance(pval, str) and not str(pval).lstrip('-').isdigit():
                            subs[pname] = f"'{pval}'"
                        else:
                            subs[pname] = str(pval)
                cond_text = _substitute(cond_text, subs)
                read_vars = [
                    f'{r.indexed_name}_{agent_name}' if r.indexed_name else r.plain_name
                    for r in ck.read_vars_raw
                    if r.indexed_name or r.plain_name
                ]
                expanded.environment_checks.append(ExpandedCheck(
                    name=f'{ck.name}_{agent_name}',
                    condition_text=cond_text,
                    read_vars=read_vars,
                ))

    # --- Step 8b: pass through top-level environment_checks ---
    # These are cross-agent checks that reference specific expanded variable names.
    # read_variables that name an array variable are expanded to all agent instances.
    # indexed refs like x_pos[r0] in the condition are resolved to x_pos_r0.
    for ck in model.environment_checks:
        cond_text = _cs_to_text(ck.condition)
        for arr_name in env_arrays:
            for agent_name in agent_names:
                cond_text = cond_text.replace(
                    f'{arr_name}[{agent_name}]', f'{arr_name}_{agent_name}'
                )
        for blv in agent_local_vars:
            for agent_name in agent_names:
                cond_text = cond_text.replace(
                    f'{blv}[{agent_name}]', f'{blv}_{agent_name}'
                )
        read_vars = []
        for v in ck.read_variables:
            if v.name in env_arrays:
                for agent_name in agent_names:
                    read_vars.append(f'{v.name}_{agent_name}')
            else:
                read_vars.append(v.name)
        expanded.environment_checks.append(ExpandedCheck(
            name=ck.name,
            condition_text=cond_text,
            read_vars=read_vars,
        ))

    # --- Step 9: expand actions from agent_type template ---
    if at:
        for act in at.agent_actions:
            for agent_name in agent_names:
                params = agent_params[agent_name]
                subs = {}
                for v in at.agent_variables:
                    subs[v.name] = f'{v.name}_{agent_name}'
                for arr_name in env_arrays:
                    subs[f'{arr_name}[self]'] = f'{arr_name}_{agent_name}'
                for pname, pval in params.items():
                    if pname not in subs:
                        if isinstance(pval, str) and not str(pval).lstrip('-').isdigit():
                            subs[pname] = f"'{pval}'"
                        else:
                            subs[pname] = str(pval)
                # Build update text from pre_update_statements + return
                update_parts = []
                for stmt in act.pre_update_statements:
                    if stmt.variable_statement:
                        vs = stmt.variable_statement
                        assign_text = _substitute(_assign_to_text(vs.assign), subs)
                        var_nm = _substitute(vs.var_name, subs)
                        update_parts.append(
                            f'variable_statement {{{var_nm} {assign_text}}}'
                        )
                rs = act.return_statement
                ret_status = rs.default_result.status if rs and rs.default_result else 'success'
                update_parts.append(f'return_statement {{result{{{ret_status}}}}}')
                update_text = '\n            '.join(update_parts)
                write_vars = [
                    f'{r.plain_name}_{agent_name}' if r.plain_name else f'{r.indexed_name}_{agent_name}'
                    for r in act.write_vars_raw
                ]
                expanded.action_nodes.append(ExpandedAction(
                    name=f'{act.name}_{agent_name}',
                    write_vars=write_vars,
                    update_text=update_text,
                ))

    # --- Step 10: build tree ---
    agent_subtrees = []
    if at:
        for agent_name in agent_names:
            subtree = _expand_agent_tree(
                at.agent_root, agent_name, at
            )
            agent_subtrees.append(subtree)

    root = ExpandedTreeNode(
        node_type='parallel',
        name='Root',
        children=agent_subtrees,
        parallel_policy='success_on_all',
    )
    expanded.tree = root

    # --- Step 11: expand specifications ---
    expanded.specifications = _expand_specifications(
        model, agent_names, env_arrays, agent_local_vars, agent_params, consts
    )

    # --- Metadata ---
    expanded.configuration_text = _config_to_text(model)
    expanded.enumerations = list(model.enumerations)
    expanded.constants_text = _constants_to_text(model)
    expanded.tick_prerequisite_text = _cs_to_text(model.tick_condition)

    return expanded


# ---------------------------------------------------------------------------
# Tree expansion
# ---------------------------------------------------------------------------

def _expand_agent_tree(agent_node, agent_name, at):
    """Recursively expand an agent_node into an ExpandedTreeNode."""
    # Composite node
    if hasattr(agent_node, 'children'):
        node_type = agent_node.node_type
        parallel_policy = getattr(agent_node, 'parallel_policy', 'success_on_all')
        children = [_expand_agent_tree(c, agent_name, at) for c in agent_node.children]
        return ExpandedTreeNode(
            node_type=node_type,
            name=f'{agent_node.name}_{agent_name}',
            children=children,
            parallel_policy=parallel_policy,
        )
    # Leaf node
    leaf_name = agent_node.leaf_name
    return ExpandedTreeNode(
        node_type='leaf',
        name=f'{leaf_name}_{agent_name}',
        leaf_name=f'{leaf_name}_{agent_name}',
    )


# ---------------------------------------------------------------------------
# Environment update expansion
# ---------------------------------------------------------------------------

def _expand_env_update(model, agent_names, env_arrays, agent_local_vars, consts):
    """
    Expand variable_statement { x_pos[i] ... } loops into N concrete statements.
    Returns the full environment_update body as .tree text.
    """
    parts = []
    for vs in model.update:
        if vs.indexed_var_name:
            # This is an indexed statement: x_pos[i] or act[i]
            base_name = vs.indexed_var_name
            idx_var = vs.indexed_var_idx  # usually 'i'
            assign_text = _assign_to_text(vs.assign)
            for agent_name in agent_names:
                # Substitute [i] → agent-specific suffix in assign text
                subs = {}
                # env arrays: x_pos[i] → x_pos_rN
                for arr in env_arrays:
                    subs[f'{arr}[{idx_var}]'] = f'{arr}_{agent_name}'
                # bl vars: act[i] → act_rN
                for blv in agent_local_vars:
                    subs[f'{blv}[{idx_var}]'] = f'{blv}_{agent_name}'
                flat_name = f'{base_name}_{agent_name}'
                flat_assign = _substitute(assign_text, subs)
                parts.append(
                    f'    variable_statement {{ {flat_name}\n'
                    f'        {flat_assign}}}'
                )
        else:
            # Regular (non-indexed) statement — pass through with agent-ref substitution.
            # Resolves arr_name[agent_name] → arr_name_agent_name so that a non-indexed
            # statement can reference expanded array variables by explicit agent name,
            # e.g. (or, on_bridge[r0], on_bridge[r1], on_bridge[r2]) → correct flat refs.
            var_nm = vs.variable.name if vs.variable else 'UNKNOWN'
            assign_text = _assign_to_text(vs.assign)
            for arr_name in env_arrays:
                for agent_name in agent_names:
                    assign_text = assign_text.replace(
                        f'{arr_name}[{agent_name}]', f'{arr_name}_{agent_name}'
                    )
            for blv in agent_local_vars:
                for agent_name in agent_names:
                    assign_text = assign_text.replace(
                        f'{blv}[{agent_name}]', f'{blv}_{agent_name}'
                    )
            parts.append(
                f'    variable_statement {{ {var_nm}\n'
                f'        {assign_text}}}'
            )
    return '\n'.join(parts)


# ---------------------------------------------------------------------------
# Specification expansion
# ---------------------------------------------------------------------------

def _expand_specifications(model, agent_names, env_arrays, agent_local_vars,
                            agent_params, consts):
    """
    Expand specifications:
    - CTLSPEC/LTLSPEC with top-level (forall, i, agents, P(i)) → N separate specs
    - INVARSPEC with forall → expand inline, simplifying agent-identity comparisons
    """
    result = []
    for spec in model.specifications:
        body = _cs_to_text(spec.code_statement)
        spec_type = spec.spec_type

        # Check if the body's outermost call is (forall/exists, var, agents, BODY)
        outermost = _try_extract_top_forall(body)
        if outermost and spec_type in ('CTLSPEC', 'LTLSPEC'):
            # Generate one spec per agent
            quant, var, domain, inner_body = outermost
            if domain.strip() == 'agents':
                for agent_name in agent_names:
                    expanded = _substitute_agent_in_body(
                        inner_body, var, agent_name,
                        env_arrays, agent_local_vars, agent_params, consts
                    )
                    # Expand any nested forall/exists
                    expanded = _expand_spec_body(
                        expanded, agent_names, env_arrays, agent_local_vars,
                        agent_params, consts
                    )
                    result.append(ExpandedSpec(spec_type, expanded))
                continue

        # Default: expand inline
        expanded_body = _expand_spec_body(
            body, agent_names, env_arrays, agent_local_vars, agent_params, consts
        )
        # Simplify agent-identity comparisons (neq/eq of agent names)
        expanded_body = _simplify_agent_identities(expanded_body, agent_names)
        result.append(ExpandedSpec(spec_type, expanded_body))

    return result


def _try_extract_top_forall(text):
    """
    If text is '(forall/exists, var, domain, body)', return (quant, var, domain, body).
    Otherwise return None.
    """
    text = text.strip()
    if not (text.startswith('(') and text.endswith(')')):
        return None
    inner = text[1:-1]
    parts = _split_top_level(inner)
    if len(parts) < 4:
        return None
    quant = parts[0].strip()
    if quant not in ('forall', 'exists'):
        return None
    var = parts[1].strip()
    domain = parts[2].strip()
    body = ', '.join(parts[3:]).strip()
    return (quant, var, domain, body)


def _simplify_agent_identities(text, agent_names):
    """
    Replace compile-time agent identity comparisons:
      (eq, rA, rA) → True    (eq, rA, rB) where A≠B → False
      (neq, rA, rA) → False  (neq, rA, rB) where A≠B → True
    Then simplify:
      (implies, True, X) → X
      (implies, False, X) → True
    Filter out True values in (and, ...) conjunctions.
    """
    for na in agent_names:
        for nb in agent_names:
            same = (na == nb)
            text = text.replace(f'(eq, {na}, {nb})', 'True' if same else 'False')
            text = text.replace(f'(neq, {na}, {nb})', 'False' if same else 'True')

    # Simplify (implies, True, X) → X   (simple regex-free approach)
    # We do multiple passes since nesting requires it
    for _ in range(5):
        text = _simplify_implies(text)

    # Simplify (and, ...) by removing True items
    text = _remove_true_from_and(text)

    return text


def _simplify_implies(text):
    """Replace (implies, True, X) → X and (implies, False, X) → True."""
    # (implies, True, X)
    pat = '(implies, True, '
    while pat in text:
        idx = text.find(pat)
        start_of_x = idx + len(pat)
        # Find the end of X (matching paren for the full implies)
        full_inner = _extract_inner(text, idx)
        if full_inner is None:
            break
        # Parse (implies, True, X) — X is everything after 'True, '
        inner_parts = _split_top_level(full_inner)
        if len(inner_parts) < 3 or inner_parts[0].strip() != 'implies' or inner_parts[1].strip() != 'True':
            break
        x = ', '.join(inner_parts[2:]).strip()
        end_idx = idx + len(full_inner) + 2
        text = text[:idx] + x + text[end_idx:]

    # (implies, False, X) → True
    pat = '(implies, False, '
    while pat in text:
        idx = text.find(pat)
        full_inner = _extract_inner(text, idx)
        if full_inner is None:
            break
        inner_parts = _split_top_level(full_inner)
        if len(inner_parts) < 3 or inner_parts[0].strip() != 'implies' or inner_parts[1].strip() != 'False':
            break
        end_idx = idx + len(full_inner) + 2
        text = text[:idx] + 'True' + text[end_idx:]

    return text


def _remove_true_from_and(text):
    """
    Simplify (and, True, X) → X, (and, X, True) → X, etc.
    Works for 2-argument and expressions.
    """
    for _ in range(5):
        changed = False
        idx = text.find('(and, True, ')
        if idx != -1:
            full_inner = _extract_inner(text, idx)
            if full_inner:
                parts = _split_top_level(full_inner)
                if len(parts) >= 2 and parts[0].strip() == 'and' and parts[1].strip() == 'True':
                    remainder = ', '.join(parts[2:]).strip()
                    end_idx = idx + len(full_inner) + 2
                    text = text[:idx] + remainder + text[end_idx:]
                    changed = True
        idx2 = text.find('(and, ')
        while idx2 != -1:
            full_inner = _extract_inner(text, idx2)
            if full_inner is None:
                break
            parts = _split_top_level(full_inner)
            if (len(parts) == 3 and parts[0].strip() == 'and' and
                    parts[2].strip() == 'True'):
                remainder = parts[1].strip()
                end_idx = idx2 + len(full_inner) + 2
                text = text[:idx2] + remainder + text[end_idx:]
                changed = True
                break
            idx2 = text.find('(and, ', idx2 + 1)
        if not changed:
            break
    return text


def _expand_spec_body(text, agent_names, env_arrays, agent_local_vars,
                      agent_params, consts):
    """
    Text-level expansion of forall/exists quantifiers and indexed references.
    Works on the serialized spec text.
    """
    # Expand (forall, i, agents, BODY) → (and, BODY[i=r0], BODY[i=r1], ...)
    # Expand (exists, i, agents, BODY) → (or, BODY[i=r0], BODY[i=r1], ...)
    changed = True
    while changed:
        changed = False
        for quant, op in (('forall', 'and'), ('exists', 'or')):
            idx = text.find(f'({quant}, ')
            if idx == -1:
                continue
            inner = _extract_inner(text, idx)
            if inner is None:
                continue
            parts = _split_top_level(inner)
            if len(parts) < 4:
                continue
            q, var, domain, *body_parts = parts
            q = q.strip()
            var = var.strip()
            domain = domain.strip()
            body = ', '.join(body_parts).strip()
            if domain != 'agents':
                continue
            # Expand body for each agent
            expanded_parts = []
            for agent_name in agent_names:
                b = _substitute_agent_in_body(
                    body, var, agent_name, env_arrays, agent_local_vars,
                    agent_params, consts
                )
                expanded_parts.append(b)
            if len(expanded_parts) == 1:
                replacement = expanded_parts[0]
            else:
                inner_joined = ', '.join(expanded_parts)
                replacement = f'({op}, {inner_joined})'
            end_idx = idx + len(inner) + 2  # +2 for parens
            text = text[:idx] + replacement + text[end_idx:]
            changed = True
            break

    return text


def _extract_inner(text, start):
    """Extract the content between matching parens starting at start."""
    if start >= len(text) or text[start] != '(':
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return None


def _split_top_level(text):
    """Split text by top-level commas (not inside parens/braces)."""
    parts = []
    depth = 0
    current = ''
    for ch in text:
        if ch in '({[':
            depth += 1
            current += ch
        elif ch in ')}]':
            depth -= 1
            current += ch
        elif ch == ',' and depth == 0:
            parts.append(current)
            current = ''
        else:
            current += ch
    if current:
        parts.append(current)
    return parts


def _substitute_agent_in_body(body, var, agent_name, env_arrays,
                               agent_local_vars, agent_params, consts):
    """
    Substitute index variable 'var' with agent_name-specific references.
    e.g. if var='i', replace x_pos[i] → x_pos_rN, goal_x[i] → resolved_val
    """
    subs = {}
    # env arrays: x_pos[i] → x_pos_rN, including 'at' variants
    for arr in env_arrays:
        subs[f'{arr}[{var}]'] = f'{arr}_{agent_name}'
    # goal parameters: goal_x[i] → value for this agent
    params = agent_params.get(agent_name, {})
    for pname, pval in params.items():
        if isinstance(pval, str) and not str(pval).lstrip('-').isdigit():
            val_str = f"'{pval}'"
        else:
            val_str = str(pval)
        subs[f'{pname}[{var}]'] = val_str
    # Also substitute the bare index variable in non-indexed contexts
    # (e.g., (neq, i, j) where i/j are agent IDs as string refs)
    # We replace the bare 'var' only when it's the exact var name
    subs[f', {var},'] = f', {agent_name},'
    subs[f', {var})'] = f', {agent_name})'
    subs[f'({var},'] = f'({agent_name},'
    result = _substitute(body, subs)
    return result


# ---------------------------------------------------------------------------
# Variable helpers
# ---------------------------------------------------------------------------

def _expand_variable(var):
    """Convert a TextX variable object to ExpandedVariable."""
    if var is None:
        return None
    domain_text = _domain_to_text(var.domain)
    init_text = _assign_to_text(var.assign)
    return ExpandedVariable(
        name=var.name,
        scope=var.var_type,
        domain_text=domain_text,
        initial_text=init_text,
    )


def _domain_to_text(domain):
    """Convert a variable_domain AST to string."""
    if domain is None:
        return 'INT'
    if domain.boolean:
        return 'BOOLEAN'
    if domain.true_int:
        return 'INT'
    if domain.true_real:
        return 'REAL'
    if domain.min_val is not None and domain.max_val is not None:
        return f'[{_cs_to_text(domain.min_val)}, {_cs_to_text(domain.max_val)}]'
    if domain.domain_codes:
        inner = ', '.join(f"'{_cs_to_text(c)}'" if not str(_cs_to_text(c)).startswith("'") else _cs_to_text(c)
                          for c in domain.domain_codes)
        return '{' + inner + '}'
    return 'INT'


def _extract_agent_param_from_assign(assign_val):
    """
    Extract the parameter name from an assign like assign{result{agents[i].param_name}}.
    Returns param_name string or None.
    """
    if assign_val is None:
        return None
    dr = assign_val.default_result
    if dr and dr.values:
        cs = dr.values[0]
        if cs.agent_param_ref:
            return cs.agent_param_name
    return None


# ---------------------------------------------------------------------------
# Model metadata helpers
# ---------------------------------------------------------------------------

def _config_to_text(model):
    parts = []
    if model.hypersafety:
        parts.append('hypersafety')
    if model.use_reals:
        parts.append('use_reals')
    if model.neural:
        parts.append('neural')
    return ' '.join(parts)


def _constants_to_text(model):
    parts = []
    for c in model.constants:
        val = c.val
        if hasattr(val, 'val') and val.val is not None:
            parts.append(f'{c.name} := {val.val}')
        else:
            parts.append(f'{c.name} := {val}')
    return ', '.join(parts)


# ---------------------------------------------------------------------------
# Passthrough for non-multi-agent models
# ---------------------------------------------------------------------------

def _passthrough(model):
    """Wrap a regular (non-multi-agent) model as ExpandedModel (minimal)."""
    expanded = ExpandedModel()
    for var in model.variables:
        ev = _expand_variable(var)
        if ev:
            expanded.variables.append(ev)
    expanded.configuration_text = _config_to_text(model)
    expanded.enumerations = list(model.enumerations)
    expanded.constants_text = _constants_to_text(model)
    expanded.tick_prerequisite_text = _cs_to_text(model.tick_condition)
    for spec in model.specifications:
        expanded.specifications.append(ExpandedSpec(
            spec.spec_type, _cs_to_text(spec.code_statement)
        ))
    return expanded


# ---------------------------------------------------------------------------
# Serialization: model_to_tree_text
# ---------------------------------------------------------------------------

def model_to_tree_text(expanded):
    """
    Serialize an ExpandedModel to valid standard .tree text.

    Args:
        expanded: ExpandedModel

    Returns:
        str containing a complete .tree file that the existing pipeline accepts.
    """
    lines = []

    # configuration
    lines.append(f'configuration {{{expanded.configuration_text}}}')

    # enumerations
    enum_inner = ', '.join(f"'{e}'" for e in expanded.enumerations)
    lines.append(f'enumerations {{{enum_inner}}}')

    # constants
    lines.append(f'constants {{{expanded.constants_text}}}')

    # variables
    lines.append('variables {')
    for v in expanded.variables:
        lines.append(f'    {v.to_tree_text()}')
    lines.append('}')

    # environment_update
    lines.append('environment_update {')
    if expanded.environment_update_text:
        lines.append(expanded.environment_update_text)
    lines.append('}')

    # checks
    lines.append('checks {}')

    # environment_checks
    lines.append('environment_checks {')
    for ck in expanded.environment_checks:
        lines.append(f'    {ck.to_tree_text()}')
    lines.append('}')

    # actions
    lines.append('actions {')
    for act in expanded.action_nodes:
        lines.append(f'    {act.to_tree_text()}')
    lines.append('}')

    # sub_trees
    lines.append('sub_trees {}')

    # tree
    lines.append('tree {')
    if expanded.tree:
        lines.append(expanded.tree.to_tree_text(indent=4))
    lines.append('}')

    # tick_prerequisite
    lines.append(f'tick_prerequisite {{{expanded.tick_prerequisite_text}}}')

    # specifications
    lines.append('specifications {')
    for spec in expanded.specifications:
        lines.append(f'    {spec}')
    lines.append('}')

    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Public entry point for behaverify.py
# ---------------------------------------------------------------------------

def maybe_expand(model_file_path):
    """
    Detect whether a .tree file uses multi-agent syntax.
    If yes, expand it and write the result to a temp file, returning the temp path.
    If no, return the original path unchanged.

    Args:
        model_file_path: str path to a .tree file

    Returns:
        str path — either the original or a temp expanded file
    """
    try:
        with open(model_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError:
        return model_file_path

    if 'agent_types' not in content and 'agents' not in content:
        return model_file_path

    try:
        from textx import metamodel_from_file
        try:
            from importlib.resources import files
            tx_file = str(files('behaverify').joinpath('data', 'metamodel', 'behaverify.tx'))
        except Exception:
            tx_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'data', 'metamodel', 'behaverify.tx'
            )
        mm = metamodel_from_file(tx_file)
        model = mm.model_from_file(model_file_path)
        expanded = expand_agents(model)
        tree_text = model_to_tree_text(expanded)

        # Write to a temp file
        suffix = Path(model_file_path).stem + '_expanded.tree'
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.tree', prefix='behaverify_',
            delete=False, encoding='utf-8'
        )
        tmp.write(tree_text)
        tmp.close()
        return tmp.name
    except Exception as e:
        print(f'[agent_expander] Warning: expansion failed ({e}), using original file.')
        return model_file_path
