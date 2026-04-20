"""
dsl_with_contracts_to_uclid5.py

Translate a BehaVerify-generated nuXmv SMV (NN encoded as lookup table) to
a UCLID5 .ucl model, replacing the NN table with verified A/G contracts.

Pipeline:
  1. Generate base SMV from .tree via dsl_to_nuxmv (NN = DEFINE table).
  2. Parse the BehaVerify-specific SMV structure.
  3. Inline BT module hierarchy: compute node.active / node.status as
     boolean expressions in terms of _stage_0 state variables.
  4. Remove the NN DEFINE block; treat NN as a free (havoc) variable.
  5. Translate nuXmv expressions to UCLID5 syntax.
  6. Render a UCLID5 module with init / next / invariant / control blocks.
  7. Inject A/G contracts as global assume statements.
  8. Write .ucl output.

Supported BehaVerify module patterns (composite, check, default leaves):
  composite_selector_without_memory_N
  composite_sequence_without_memory_N
  *_module(params)       — check nodes (condition ? success : failure)
  running_DEFAULT_module — always running
  success_DEFAULT_module — always success
  failure_DEFAULT_module — always failure

Usage:
  python dsl_with_contracts_to_uclid5.py \\
    --metamodel ../../../../src/behaverify/data/metamodel/behaverify.tx \\
    --tree      counter_template.tree \\
    --contracts contracts/crown/disabled_pgd/0995__6_18_0__200_1.json \\
    --output    results/uclid5/0995_contracts.ucl \\
    --neural-var network \\
    --pos-x drone_x --pos-y drone_y \\
    --domain left right up down no_action \\
    --dir-map '{"We":"left","Ea":"right","No":"up","So":"down","XX":"no_action"}' \\
    --bmc-steps 50
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Path setup: import dsl_to_nuxmv from the same src/ directory
# ---------------------------------------------------------------------------

_SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SRC)

import dsl_to_nuxmv as _base  # noqa: E402

# ---------------------------------------------------------------------------
# Default direction-label mapping (same as dsl_with_contracts_to_nuxmv.py)
# ---------------------------------------------------------------------------

DEFAULT_DIR_MAP: dict[str, str] = {
    "We": "left",
    "Ea": "right",
    "No": "up",
    "So": "down",
    "XX": "no_action",
}

# ---------------------------------------------------------------------------
# Data structures for the parsed SMV
# ---------------------------------------------------------------------------


@dataclass
class SMVParsed:
    """Structured representation of a BehaVerify-generated SMV file."""
    # Domain / type information
    constants: list[str] = field(default_factory=list)
    # State variables (from --START OF BLACKBOARD VARIABLES DECLARATION)
    state_vars: dict[str, str] = field(default_factory=dict)   # name → raw SMV type string
    # DEFINE assignments in system_module (name → raw SMV expr, may be multi-line)
    defines: dict[str, str] = field(default_factory=dict)
    # ASSIGN init(x_stage_0) := expr
    init_assigns: dict[str, str] = field(default_factory=dict)  # var_base → expr
    # ASSIGN next(x_stage_0) := expr
    next_assigns: dict[str, str] = field(default_factory=dict)  # var_base → expr
    # INVARSPEC lines (raw SMV expr, without the INVARSPEC keyword)
    invarspecs: list[str] = field(default_factory=list)
    # BT node instances from VAR section (before BLACKBOARD block)
    bt_instances: dict[str, tuple[str, list[str]]] = field(default_factory=dict)
    # Module definitions: module_type → {param_names, define_lines}
    module_defs: dict[str, dict[str, Any]] = field(default_factory=dict)
    # Explicit node.active assignments from system_module DEFINE
    explicit_actives: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Contract loading
# ---------------------------------------------------------------------------


def load_sat_contracts(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    sat = [c for c in data["contracts"] if c["status"] == "SAT"]
    print(f"  {len(sat)} SAT contracts loaded (of {len(data['contracts'])} total)")
    return sat


# ---------------------------------------------------------------------------
# SMV parsing helpers
# ---------------------------------------------------------------------------


def _collect_expr(lines: list[str], idx: int) -> tuple[str, int]:
    """
    Starting from lines[idx] (which contains ':='), collect until the
    matching semicolon, handling nested case...esac blocks.

    Returns (raw_expr, new_idx) where new_idx points past the final line.
    """
    text = []
    depth = 0
    i = idx
    while i < len(lines):
        line = lines[i]
        i += 1
        text.append(line)
        depth += line.count("case") - line.count("esac")
        if depth <= 0 and line.rstrip().endswith(";"):
            break
    return "\n".join(text), i


def _parse_module_section(module_text: str) -> dict[str, Any]:
    """
    Parse a single MODULE definition (everything after 'MODULE name...' line).
    Returns dict with keys: params (list), defines (dict name→expr).
    """
    lines = module_text.split("\n")
    params: list[str] = []
    defines: dict[str, str] = {}

    # Extract formal param names from the first line
    # e.g. "MODULE composite_selector_without_memory_2(child_0, child_1)"
    m = re.match(r"MODULE\s+\w+\s*\(([^)]*)\)", lines[0])
    if m and m.group(1).strip():
        params = [p.strip() for p in m.group(1).split(",") if p.strip()]

    # Parse DEFINE section
    in_define = False
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        if line == "DEFINE":
            in_define = True
            i += 1
            continue
        if line in ("VAR", "ASSIGN", "CONSTANTS", ""):
            in_define = False
            i += 1
            continue
        if not in_define:
            i += 1
            continue

        # Try to parse "name := expr;"
        cm = re.match(r"(\S+)\s*:=", line)
        if cm:
            name = cm.group(1)
            expr_raw, i = _collect_expr(lines, i)
            defines[name] = _extract_rhs(expr_raw)
        else:
            i += 1

    return {"params": params, "defines": defines}


def parse_behaverify_smv(smv_text: str) -> SMVParsed:
    """Parse a BehaVerify-generated nuXmv SMV into SMVParsed."""
    parsed = SMVParsed()

    # Split file into MODULE blocks
    module_pattern = re.compile(r"^MODULE\s+", re.MULTILINE)
    splits = list(module_pattern.finditer(smv_text))
    modules_text = []
    for idx, m in enumerate(splits):
        start = m.start()
        end = splits[idx + 1].start() if idx + 1 < len(splits) else len(smv_text)
        modules_text.append(smv_text[start:end].strip())

    # Extract INVARSPEC from MODULE main
    for block in modules_text:
        if block.startswith("MODULE main"):
            for line in block.split("\n"):
                ls = line.strip()
                if ls.startswith("INVARSPEC"):
                    parsed.invarspecs.append(ls[len("INVARSPEC"):].strip().rstrip(";"))
            break

    # Parse MODULE system_module
    for block in modules_text:
        if not block.startswith("MODULE system_module"):
            continue
        _parse_system_module(block, parsed)

    # Parse all other module definitions
    for block in modules_text:
        first_line = block.split("\n")[0]
        if first_line.startswith("MODULE main") or first_line.startswith("MODULE system_module"):
            continue
        if first_line.startswith("MODULE define_nodes"):
            continue
        mod_info = _parse_module_section(block)
        name_m = re.match(r"MODULE\s+(\w+)", first_line)
        if name_m:
            parsed.module_defs[name_m.group(1)] = mod_info

    return parsed


def _parse_system_module(block: str, parsed: SMVParsed) -> None:
    """Parse system_module block into parsed (mutates in place)."""
    lines = block.split("\n")
    section = None
    blackboard_vars = False
    blackboard_init = False
    blackboard_next = False
    bt_var_region = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Section markers
        if stripped == "CONSTANTS":
            section = "constants"
            i += 1
            continue
        if stripped == "DEFINE":
            section = "define"
            i += 1
            continue
        if stripped == "VAR":
            section = "var"
            bt_var_region = True
            i += 1
            continue
        if stripped == "ASSIGN":
            section = "assign"
            i += 1
            continue

        # Sub-markers inside VAR
        if stripped == "--START OF BLACKBOARD VARIABLES DECLARATION":
            bt_var_region = False
            blackboard_vars = True
            i += 1
            continue
        if stripped == "--END OF BLACKBOARD VARIABLES DECLARATION":
            blackboard_vars = False
            i += 1
            continue
        if stripped == "--START OF BLACKBOARD VARIABLES INITIALIZATION":
            blackboard_init = True
            i += 1
            continue
        if stripped == "--END OF BLACKBOARD VARIABLES INITIALIZATION":
            blackboard_init = False
            i += 1
            continue
        if stripped == "--START OF BLACKBOARD VARIABLES TRANSITION":
            blackboard_next = True
            i += 1
            continue
        if stripped == "--END OF BLACKBOARD VARIABLES TRANSITION":
            blackboard_next = False
            i += 1
            continue
        if stripped.startswith("--"):
            i += 1
            continue

        # Parse by section
        if section == "constants" and stripped:
            raw = stripped.rstrip(";")
            parsed.constants = [c.strip() for c in raw.split(",") if c.strip()]
            i += 1
            continue

        if section == "define" and stripped:
            # Check for explicit node.active := expr
            act_m = re.match(r"(\w+(?:\.\w+)?)\s*:=", stripped)
            if act_m:
                name = act_m.group(1)
                expr_raw, i = _collect_expr(lines, i)
                expr_clean = _extract_rhs(expr_raw)
                if ".active" in name:
                    parsed.explicit_actives[name] = expr_clean
                else:
                    # Strip _stage_0 suffix for DEFINE names used as intermediates
                    parsed.defines[name] = expr_clean
            else:
                i += 1
            continue

        if section == "var" and bt_var_region and stripped:
            # Parse "instance_name : module_type(p1, p2, ...);"
            vm = re.match(r"(\w+)\s*:\s*(\w+)\s*\(([^)]*)\)\s*;", stripped)
            if vm:
                inst_name = vm.group(1)
                mod_type = vm.group(2)
                raw_params = vm.group(3)
                params = [p.strip() for p in raw_params.split(",") if p.strip()]
                if inst_name != "node_names":
                    parsed.bt_instances[inst_name] = (mod_type, params)
            i += 1
            continue

        if section == "var" and blackboard_vars and stripped:
            # Parse "var_name_stage_0 : type;"
            vm = re.match(r"(\w+)\s*:\s*(.+?)\s*;", stripped)
            if vm:
                var_full = vm.group(1)
                var_type = vm.group(2)
                # Strip _stage_0 suffix to get the base name
                base = _strip_stage0(var_full)
                parsed.state_vars[base] = var_type
            i += 1
            continue

        if section == "assign" and blackboard_init and stripped:
            # Parse "init(var_name_stage_0) := expr;"
            im = re.match(r"init\((\w+)\)\s*:=", stripped)
            if im:
                var_full = im.group(1)
                base = _strip_stage0(var_full)
                expr_raw, i = _collect_expr(lines, i)
                parsed.init_assigns[base] = _extract_rhs(expr_raw)
            else:
                i += 1
            continue

        if section == "assign" and blackboard_next and stripped:
            # Parse "next(var_name_stage_0) := expr;"
            nm = re.match(r"next\((\w+)\)\s*:=", stripped)
            if nm:
                var_full = nm.group(1)
                base = _strip_stage0(var_full)
                expr_raw, i = _collect_expr(lines, i)
                parsed.next_assigns[base] = _extract_rhs(expr_raw)
            else:
                i += 1
            continue

        i += 1


def _extract_rhs(raw: str) -> str:
    """Extract the RHS from 'name := RHS;' text, stripping whitespace."""
    m = re.search(r":=\s*(.*)", raw, re.DOTALL)
    if m:
        return m.group(1).strip().rstrip(";").strip()
    return raw.strip().rstrip(";")


def _strip_stage0(name: str) -> str:
    """Remove _stage_0 suffix from a variable name."""
    if name.endswith("_stage_0"):
        return name[:-len("_stage_0")]
    return name


# ---------------------------------------------------------------------------
# BT hierarchy inlining
# ---------------------------------------------------------------------------


def _classify_module(module_type: str) -> str:
    """Classify a BehaVerify module type."""
    if module_type.startswith("composite_selector"):
        return "selector"
    if module_type.startswith("composite_sequence"):
        return "sequence"
    if module_type == "running_DEFAULT_module":
        return "running"
    if module_type == "success_DEFAULT_module":
        return "success"
    if module_type == "failure_DEFAULT_module":
        return "failure"
    return "check"  # any other *_module is a check node


def compute_bt_node_expressions(
    parsed: SMVParsed,
) -> dict[str, str]:
    """
    Walk the BT hierarchy, computing closed-form boolean/status expressions
    for every node.active and node.status in terms of _stage_0 state vars.

    Returns a dict: "node.active" → expr, "node.status" → expr,
    "node.internal_status" → expr
    """
    instances = parsed.bt_instances
    module_defs = parsed.module_defs
    result: dict[str, str] = {}

    # Seed with explicitly defined node.active values from system_module DEFINE
    for key, expr in parsed.explicit_actives.items():
        result[key] = expr

    # Topological order: roots first, then children
    # Find root nodes: those with explicit .active
    roots = [k.split(".")[0] for k in parsed.explicit_actives if ".active" in k]

    visited: set[str] = set()
    queue = list(roots)

    def _process_node(node: str) -> None:
        if node in visited:
            return
        visited.add(node)

        if node not in instances:
            return

        mod_type, params = instances[node]
        kind = _classify_module(mod_type)
        active_expr = result.get(f"{node}.active", "true")

        if kind in ("running", "success", "failure"):
            fixed = kind
            result[f"{node}.internal_status"] = fixed
            result[f"{node}.status"] = (
                f"(if ({active_expr}) then {fixed} else invalid)"
            )

        elif kind == "check":
            # Get internal_status from module definition
            mod_info = module_defs.get(mod_type, {})
            raw_int = mod_info.get("defines", {}).get("internal_status", "failure")
            # raw_int uses formal params; substitute with actual params if needed
            int_expr = _substitute_check_params(raw_int, mod_type, params, module_defs)
            int_expr = _clean_smv_expr(int_expr)
            result[f"{node}.internal_status"] = int_expr
            result[f"{node}.status"] = (
                f"(if ({active_expr}) then {int_expr} else invalid)"
            )

        elif kind == "selector":
            # params = [child_0, child_1, ..., child_{N-1}]
            # child_0.active = self.active
            # child_k.active = child_{k-1}.status == failure (for k>=1)
            child_statuses = []
            for k, child in enumerate(params):
                if k == 0:
                    child_active = active_expr
                else:
                    prev_status = result.get(f"{params[k-1]}.status",
                                             f"{params[k-1]}_status")
                    child_active = f"({prev_status} == failure)"
                result[f"{child}.active"] = child_active
                _process_node(child)
                child_statuses.append(result.get(f"{child}.status",
                                                  f"{child}_status"))

            # selector internal_status = first non-failure child, else failure
            int_expr = _build_selector_status(child_statuses)
            result[f"{node}.internal_status"] = int_expr
            result[f"{node}.status"] = (
                f"(if ({active_expr}) then {int_expr} else invalid)"
            )

        elif kind == "sequence":
            child_statuses = []
            for k, child in enumerate(params):
                if k == 0:
                    child_active = active_expr
                else:
                    prev_status = result.get(f"{params[k-1]}.status",
                                             f"{params[k-1]}_status")
                    child_active = f"({prev_status} == success)"
                result[f"{child}.active"] = child_active
                _process_node(child)
                child_statuses.append(result.get(f"{child}.status",
                                                  f"{child}_status"))

            # sequence internal_status = first non-success child, else success
            int_expr = _build_sequence_status(child_statuses)
            result[f"{node}.internal_status"] = int_expr
            result[f"{node}.status"] = (
                f"(if ({active_expr}) then {int_expr} else invalid)"
            )

    for root in queue:
        _process_node(root)

    return result


def _substitute_check_params(
    expr: str,
    mod_type: str,
    actual_params: list[str],
    module_defs: dict[str, dict],
) -> str:
    """
    Substitute formal parameters in a check module's internal_status expression
    with the actual parameters from the instantiation.

    BehaVerify often names formal params identically to actual params,
    so this is usually a no-op. But we handle the general case.
    """
    mod_info = module_defs.get(mod_type, {})
    formal_params = mod_info.get("params", [])
    if not formal_params:
        return expr
    for formal, actual in zip(formal_params, actual_params):
        if formal != actual:
            expr = re.sub(r"\b" + re.escape(formal) + r"\b", actual, expr)
    return expr


def _build_selector_status(child_statuses: list[str]) -> str:
    """Build selector status expression: first non-failure child, else failure."""
    if not child_statuses:
        return "failure"
    # Rightmost-first nesting: last else = failure
    expr = "failure"
    for cs in reversed(child_statuses):
        expr = f"(if ({cs} != failure) then {cs} else {expr})"
    return expr


def _build_sequence_status(child_statuses: list[str]) -> str:
    """Build sequence status expression: first non-success child, else success."""
    if not child_statuses:
        return "success"
    expr = "success"
    for cs in reversed(child_statuses):
        expr = f"(if ({cs} != success) then {cs} else {expr})"
    return expr


def _clean_smv_expr(expr: str) -> str:
    """Light SMV → UCLID5 expression cleaning (used on check module conditions)."""
    expr = expr.strip().rstrip(";")
    # Ternary ? : → if-then-else
    expr = _translate_ternary(expr)
    # Equality = → == (avoid :=, !=, ==, <=, >=)
    expr = re.sub(r"(?<![!:<>=])=(?!=)", "==", expr)
    # Boolean ops (single & → &&, single | → ||; avoid doubling)
    expr = re.sub(r"(?<!&)&(?!&)", "&&", expr)
    expr = re.sub(r"(?<!\|)\|(?!\|)", "||", expr)
    expr = re.sub(r"\bTRUE\b", "true", expr)
    expr = re.sub(r"\bFALSE\b", "false", expr)
    return expr


def _translate_ternary(expr: str) -> str:
    """Convert 'cond ? then_val : else_val' to '(if (cond) then then_val else else_val)'."""
    if "?" not in expr:
        return expr
    # Find ? at parenthesis depth 0
    depth = 0
    q_pos = -1
    for i, ch in enumerate(expr):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "?" and depth == 0:
            q_pos = i
            break
    if q_pos == -1:
        return expr
    # Find : after ? at depth 0
    depth = 0
    c_pos = -1
    for i in range(q_pos + 1, len(expr)):
        ch = expr[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == ":" and depth == 0:
            c_pos = i
            break
    if c_pos == -1:
        return expr
    cond = expr[:q_pos].strip()
    then_val = expr[q_pos + 1:c_pos].strip()
    else_val = expr[c_pos + 1:].strip().rstrip(";")
    return f"(if ({cond}) then {then_val} else {else_val})"


# ---------------------------------------------------------------------------
# Expression translation: nuXmv → UCLID5
# ---------------------------------------------------------------------------


def _replace_minmax_calls(expr: str) -> str:
    """Replace max(a,b) and min(a,b) with UCLID5 if-then-else, handling nested parens."""
    result: list[str] = []
    i = 0
    while i < len(expr):
        m = re.match(r"(max|min)\(", expr[i:])
        if not m:
            result.append(expr[i])
            i += 1
            continue
        fn = m.group(1)
        start = i + len(fn) + 1  # index after '('
        # Find comma at depth 0
        depth = 0
        comma_pos = -1
        j = start
        while j < len(expr):
            c = expr[j]
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                comma_pos = j
                break
            j += 1
        if comma_pos == -1:
            result.append(expr[i])
            i += 1
            continue
        arg1 = expr[start:comma_pos].strip()
        # Find end of call at depth 0 after comma
        depth = 0
        end_pos = -1
        j = comma_pos + 1
        while j < len(expr):
            c = expr[j]
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    end_pos = j
                    break
                depth -= 1
            j += 1
        if end_pos == -1:
            result.append(expr[i])
            i += 1
            continue
        arg2 = expr[comma_pos + 1:end_pos].strip()
        op = ">" if fn == "max" else "<"
        result.append(f"(if ({arg1} {op} {arg2}) then {arg1} else {arg2})")
        i = end_pos + 1
    return "".join(result)


def _topological_sort_defines(stage_defines: dict[str, str]) -> list[str]:
    """Topologically sort stage define names by their SMV expression dependencies."""
    stage_names = set(stage_defines.keys())
    deps: dict[str, set[str]] = {k: set() for k in stage_names}
    for name, expr in stage_defines.items():
        for ref in re.findall(r"\b\w+_stage_\d+\b", expr):
            if ref in stage_names and ref != name:
                deps[name].add(ref)
    # Kahn's algorithm
    in_degree = {k: len(v) for k, v in deps.items()}
    ready = [k for k, d in sorted(in_degree.items()) if d == 0]
    result: list[str] = []
    while ready:
        node = ready.pop(0)
        result.append(node)
        for other in list(stage_names):
            if node in deps.get(other, set()):
                deps[other].discard(node)
                in_degree[other] -= 1
                if in_degree[other] == 0:
                    ready.append(other)
    # Append any remaining (cycles shouldn't occur in valid BehaVerify SMV)
    result.extend(k for k in stage_defines if k not in result)
    return result


def translate_expr(
    smv_expr: str,
    node_props: dict[str, str],
    state_vars: set[str],
    neural_var: str,
    invarspec_mode: bool = False,
) -> str:
    """
    Translate a nuXmv SMV expression to UCLID5 syntax.

    Handles:
    - case...esac → nested if-then-else
    - max(a,b) / min(a,b) → conditional
    - & / | / ! / = → && / || / ! / ==
    - TRUE/FALSE → true/false
    - x_stage_0 → x (state var references)
    - x_stage_N → x_N (intermediate stages as local vars)
    - system.x_stage_0 → x (references from INVARSPEC)
    - node.active / node.status → inlined expressions from node_props
    - {0,1,2,...} → handled at call site (havoc pattern)
    """
    expr = smv_expr.strip().rstrip(";").strip()

    # Strip outer parens repeatedly to simplify
    # (don't strip all, just cosmetically)

    # Substitute node.active and node.status with inlined expressions
    for prop_key, prop_val in sorted(node_props.items(), key=lambda x: -len(x[0])):
        prop_key_safe = re.escape(prop_key)
        expr = re.sub(r"\b" + prop_key_safe + r"\b", f"({prop_val})", expr)

    # Handle case...esac blocks
    expr = _translate_case_expr(expr, state_vars, neural_var)

    # max/min builtins — use depth-aware parser to handle nested parens
    expr = _replace_minmax_calls(expr)

    # abs() — keep as-is for now (UCLID5 doesn't have abs, user handles separately)
    # Boolean ops (avoid doubling && → &&&&, etc.)
    expr = re.sub(r"(?<![!:<>=])=(?!=)", "==", expr)
    expr = re.sub(r"(?<!&)&(?!&)", "&&", expr)
    expr = re.sub(r"(?<!\|)\|(?!\|)", "||", expr)
    expr = re.sub(r"\bTRUE\b", "true", expr)
    expr = re.sub(r"\bFALSE\b", "false", expr)

    # Strip "system." prefix (from INVARSPEC)
    expr = re.sub(r"\bsystem\.", "", expr)

    # Rename _stage_0 → bare var name, _stage_N → var_N (or base in invarspec)
    expr = _rename_stage_vars(expr, state_vars, neural_var, invarspec_mode=invarspec_mode)

    return expr


def _translate_case_expr(expr: str, state_vars: set[str], neural_var: str) -> str:
    """
    Recursively translate case...esac to if-then-else expressions.
    Handles nested cases (though BehaVerify rarely nests them).
    """
    # Find outermost case...esac
    while re.search(r"\bcase\b", expr):
        m = re.search(r"\bcase\b(.*?)\besac\b", expr, re.DOTALL)
        if not m:
            break
        case_body = m.group(1)
        if_expr = _case_body_to_if(case_body)
        expr = expr[:m.start()] + if_expr + expr[m.end():]
    return expr


def _case_body_to_if(body: str) -> str:
    """
    Convert the body of a case...esac to nested if-then-else.
    Expects 'cond : val;' pairs, last one is 'TRUE : default;'.
    """
    # Split on ';' then parse each 'cond : val'
    arms = []
    for segment in body.split(";"):
        segment = segment.strip()
        if not segment:
            continue
        cm = re.match(r"(.+?)\s*:\s*(.+)", segment, re.DOTALL)
        if cm:
            cond = cm.group(1).strip()
            val = cm.group(2).strip()
            arms.append((cond, val))

    if not arms:
        return "true"

    # Build nested if-then-else from right to left
    # Last arm (TRUE : default) becomes the final else
    last_cond, last_val = arms[-1]
    if last_cond.strip().upper() == "TRUE":
        result = last_val
        arms = arms[:-1]
    else:
        result = last_val  # fallback

    for cond, val in reversed(arms):
        result = f"(if ({cond}) then {val} else {result})"

    return result


def _rename_stage_vars(
    expr: str,
    state_vars: set[str],
    neural_var: str,
    invarspec_mode: bool = False,
) -> str:
    """
    Replace x_stage_0 → x  (state variables) and
    x_stage_N → x_N (intermediate stage locals).

    In invarspec_mode, ALL stage_N refs (N>=1) are also mapped to x
    because UCLID5 invariants check the current state variable (which
    after a transition equals what nuXmv calls x_stage_1 at the prior step).
    """
    def replacer(m: re.Match) -> str:
        full = m.group(0)
        sm = re.match(r"^(.+)_stage_(\d+)$", full)
        if not sm:
            return full
        base = sm.group(1)
        stage = sm.group(2)
        if stage == "0" or invarspec_mode:
            return base  # state variable (or treat all stages as base in invariant)
        return f"{base}_{stage}"  # intermediate local

    return re.sub(r"\b\w+_stage_\d+\b", replacer, expr)


# ---------------------------------------------------------------------------
# UCLID5 type inference
# ---------------------------------------------------------------------------


def _smv_type_to_uclid5(smv_type: str, var_name: str) -> tuple[str, str | None]:
    """
    Convert a nuXmv type string to a UCLID5 type.
    Returns (uclid5_type, assume_constraint_or_None).

    Examples:
      'boolean'              → ('boolean', None)
      '0..6'                 → ('integer', 'var_name >= 0 && var_name <= 6')
      '{left, right, ...}'   → ('action_t', None)  (enum types collected separately)
      '{1, -1}'              → ('integer', 'var_name == 1 || var_name == -1')
    """
    smv_type = smv_type.strip()

    if smv_type == "boolean":
        return "boolean", None

    # Range: 0..6
    range_m = re.match(r"(-?\d+)\.\.(-?\d+)", smv_type)
    if range_m:
        lo, hi = range_m.group(1), range_m.group(2)
        return "integer", f"({var_name} >= {lo} && {var_name} <= {hi})"

    # Enum set: {val1, val2, ...}
    enum_m = re.match(r"\{([^}]+)\}", smv_type)
    if enum_m:
        vals = [v.strip() for v in enum_m.group(1).split(",")]
        # Check if values are integers
        if all(re.match(r"^-?\d+$", v) for v in vals):
            constraint = " || ".join(f"({var_name} == {v})" for v in vals)
            return "integer", constraint
        else:
            # Named enum — type name derived from values
            return _enum_type_name(vals), None

    return "integer", None  # fallback


def _enum_type_name(vals: list[str]) -> str:
    """Derive a UCLID5 type name for a set of enum values."""
    # Use a stable hash of sorted values to name the type
    key = "_".join(sorted(vals))
    # Common well-known sets
    status_vals = {"success", "failure", "running", "invalid"}
    if set(vals) == status_vals:
        return "status_t"
    return f"enum_{abs(hash(key)) % 10000}_t"


def _collect_enum_types(parsed: SMVParsed) -> dict[str, list[str]]:
    """Collect all named enum types from state_var declarations."""
    enum_types: dict[str, list[str]] = {}  # type_name → [values]
    for var_name, smv_type in parsed.state_vars.items():
        enum_m = re.match(r"\{([^}]+)\}", smv_type)
        if enum_m:
            vals = [v.strip() for v in enum_m.group(1).split(",")]
            if not all(re.match(r"^-?\d+$", v) for v in vals):
                etype = _enum_type_name(vals)
                if etype not in enum_types:
                    enum_types[etype] = vals
    return enum_types


# ---------------------------------------------------------------------------
# Conditional non-deterministic assignment helper
# ---------------------------------------------------------------------------


def _render_conditional_havoc(
    var_name: str,
    case_expr: str,
    prop_to_local: dict[str, str],
    state_var_names: set[str],
    neural_var: str,
    ind: str,
) -> list[str]:
    """
    Handle a case expression that contains a {set} arm for non-det assignment.

    nuXmv pattern:
        next(x) := case
            cond1 : val1;
            cond2 : {lo, ..., hi};   ← non-det
            TRUE  : valN;
        esac;

    UCLID5 output:
        if (cond1) { x' = val1; }
        else if (cond2) { havoc x; assume (x >= lo && x <= hi); }
        else { x' = valN; }
    """
    # Parse case arms
    body_m = re.search(r"\bcase\b(.*)\besac\b", case_expr, re.DOTALL)
    if not body_m:
        return [f"{ind}{ind}// WARNING: could not parse case for {var_name}: {case_expr[:80]}"]

    arms = []
    for seg in body_m.group(1).split(";"):
        seg = seg.strip()
        if not seg:
            continue
        cm = re.match(r"(.+?)\s*:\s*(.+)", seg, re.DOTALL)
        if cm:
            arms.append((cm.group(1).strip(), cm.group(2).strip()))

    # UCLID5 has no 'else if' — chains must be nested as 'else { if ... }'.
    # Build a recursive structure: emit the first arm, then nest remainder in else.
    def _emit_arms(arms_remaining: list, depth: int) -> list[str]:
        if not arms_remaining:
            return []
        cond, val = arms_remaining[0]
        rest = arms_remaining[1:]
        extra = ind * depth  # additional indentation for nesting
        result: list[str] = []
        set_m = re.match(r"\{([^}]+)\}", val)
        is_true_arm = cond.strip().upper() == "TRUE"

        if is_true_arm:
            # Final catch-all arm — emit as plain else
            if set_m:
                int_vals = [v.strip() for v in set_m.group(1).split(",")]
                lo = min(int(v) for v in int_vals)
                hi = max(int(v) for v in int_vals)
                result.append(f"{extra}{ind}{ind}else {{")
                result.append(f"{extra}{ind}{ind}{ind}havoc {var_name};")
                result.append(f"{extra}{ind}{ind}{ind}assume ({var_name} >= {lo} && {var_name} <= {hi});")
                result.append(f"{extra}{ind}{ind}}}")
            else:
                ucl_val = _translate_arm_val(val, prop_to_local, state_var_names, neural_var)
                result.append(f"{extra}{ind}{ind}else {{")
                result.append(f"{extra}{ind}{ind}{ind}{var_name}' = {ucl_val};")
                result.append(f"{extra}{ind}{ind}}}")
            return result

        ucl_cond = _translate_arm_cond(cond, prop_to_local, state_var_names, neural_var)
        keyword = "if" if depth == 0 else "if"
        if set_m:
            int_vals = [v.strip() for v in set_m.group(1).split(",")]
            lo = min(int(v) for v in int_vals)
            hi = max(int(v) for v in int_vals)
            result.append(f"{extra}{ind}{ind}{keyword} ({ucl_cond}) {{")
            result.append(f"{extra}{ind}{ind}{ind}havoc {var_name};")
            result.append(f"{extra}{ind}{ind}{ind}assume ({var_name} >= {lo} && {var_name} <= {hi});")
            result.append(f"{extra}{ind}{ind}}}")
        else:
            ucl_val = _translate_arm_val(val, prop_to_local, state_var_names, neural_var)
            result.append(f"{extra}{ind}{ind}{keyword} ({ucl_cond}) {{")
            result.append(f"{extra}{ind}{ind}{ind}{var_name}' = {ucl_val};")
            result.append(f"{extra}{ind}{ind}}}")

        if rest:
            if rest[0][0].strip().upper() == "TRUE":
                # next arm is the catch-all — emit as else directly
                result.extend(_emit_arms(rest, depth))
            else:
                # nest remaining arms inside an else block
                result.append(f"{extra}{ind}{ind}else {{")
                result.extend(_emit_arms(rest, depth + 1))
                result.append(f"{extra}{ind}{ind}}}")
        return result

    return _emit_arms(arms, 0)


def _translate_arm_cond(
    cond: str, prop_to_local: dict[str, str], state_vars: set[str], neural_var: str
) -> str:
    for prop_key, local in prop_to_local.items():
        cond = re.sub(r"\b" + re.escape(prop_key) + r"\b", local, cond)
    return translate_expr(cond, {}, state_vars, neural_var)


def _translate_arm_val(
    val: str, prop_to_local: dict[str, str], state_vars: set[str], neural_var: str
) -> str:
    for prop_key, local in prop_to_local.items():
        val = re.sub(r"\b" + re.escape(prop_key) + r"\b", local, val)
    return translate_expr(val, {}, state_vars, neural_var)


# ---------------------------------------------------------------------------
# UCLID5 rendering
# ---------------------------------------------------------------------------


def render_uclid5(
    parsed: SMVParsed,
    node_props: dict[str, str],
    neural_var: str,
    domain: list[str],
    bmc_steps: int,
    tree_file: str,
    contracts_file: str,
) -> str:
    """Render a complete UCLID5 module string from the parsed SMV."""
    lines: list[str] = []
    ind = "  "  # 2-space indent

    state_var_names = set(parsed.state_vars.keys())
    # Include neural_var as a state var for renaming purposes
    state_var_names.add(neural_var)

    # Collect enum types
    enum_types = _collect_enum_types(parsed)
    # Add status type (from CONSTANTS)
    status_vals = [c for c in parsed.constants if c in {"success", "failure", "running", "invalid"}]
    if status_vals:
        enum_types["status_t"] = ["success", "failure", "running", "invalid"]
    # Add domain enum type for neural var
    if domain:
        domain_type = _enum_type_name(domain)
        enum_types[domain_type] = domain

    lines.append(f"// Generated by dsl_with_contracts_to_uclid5.py")
    lines.append(f"// Tree: {tree_file}  Contracts: {contracts_file}")
    lines.append("")
    lines.append("module main {")
    lines.append("")

    # --- Types ---
    lines.append(f"{ind}// --- Types ---")
    for type_name, vals in sorted(enum_types.items()):
        vals_str = ", ".join(vals)
        lines.append(f"{ind}type {type_name} = enum {{ {vals_str} }};")
    lines.append("")

    # --- State variables ---
    lines.append(f"{ind}// --- State variables ---")
    for var_name, smv_type in parsed.state_vars.items():
        if var_name == neural_var:
            continue  # handled separately as free var
        ucl_type, _ = _smv_type_to_uclid5(smv_type, var_name)
        lines.append(f"{ind}var {var_name} : {ucl_type};")
    # Neural var: free (non-deterministic)
    neural_type = _enum_type_name(domain) if domain else "integer"
    lines.append(f"{ind}var {neural_var} : {neural_type};  "
                 f"// non-deterministic (constrained by A/G contracts below)")
    lines.append("")

    # --- A/G contract constraints placeholder (filled in later) ---
    lines.append(f"{ind}// --- A/G contract constraints (verified by alpha-beta-CROWN) ---")
    lines.append(f"{ind}// (injected below by inject_contract_assumes)")
    lines.append(f"{ind}// CONTRACT_INJECT_MARKER")
    lines.append("")

    # --- Range invariants for bounded integer vars ---
    range_assumes = []
    for var_name, smv_type in parsed.state_vars.items():
        _, constraint = _smv_type_to_uclid5(smv_type, var_name)
        if constraint:
            range_assumes.append((var_name, constraint))
    if range_assumes:
        lines.append(f"{ind}// --- Range constraints (from nuXmv variable types) ---")
        for var_name, constraint in range_assumes:
            lines.append(f"{ind}assume {var_name}_range : ({constraint});")
        lines.append("")

    # --- Initialization ---
    lines.append(f"{ind}init {{")
    for var_name, init_expr in parsed.init_assigns.items():
        if var_name == neural_var:
            continue
        ucl_init = translate_expr(init_expr, node_props, state_var_names, neural_var)
        lines.append(f"{ind}{ind}{var_name} = {ucl_init};")
    lines.append(f"{ind}}}")
    lines.append("")

    # --- Transition (next block) ---
    lines.append(f"{ind}next {{")

    # Step 1: Compute BT node active/status as local vars, in topological order
    # Find all node properties referenced in defines/next_assigns
    referenced_props: set[str] = set()
    all_exprs = list(parsed.defines.values()) + list(parsed.next_assigns.values())
    for expr in all_exprs:
        for prop_key in node_props:
            if re.search(r"\b" + re.escape(prop_key) + r"\b", expr):
                referenced_props.add(prop_key)

    # UCLID5 requires ALL var declarations before ANY statements in a block.
    # Collect var decls and assignment lines separately, then emit decls first.
    var_decl_lines: list[str] = []
    assign_lines: list[str] = []

    if referenced_props:
        assign_lines.append(f"{ind}{ind}// BT node active/status values (inlined from module hierarchy)")
        for prop_key in sorted(referenced_props):
            prop_val = node_props[prop_key]
            local_name = prop_key.replace(".", "_")
            ucl_val = translate_expr(prop_val, {}, state_var_names, neural_var)
            var_decl_lines.append(f"{ind}{ind}var {local_name} : boolean;")
            assign_lines.append(f"{ind}{ind}{local_name} = ({ucl_val});")
        assign_lines.append("")

        # Build a substitution map from prop_key → local_name for stage translations
        prop_to_local = {k: k.replace(".", "_") for k in node_props}
    else:
        prop_to_local = {}

    # Step 2: Compute intermediate stage variables (DEFINE x_stage_N)
    # Only stage_N (N>0) defines; not stage_0 (those are state vars)
    stage_defines = {
        k: v for k, v in parsed.defines.items()
        if re.search(r"_stage_[1-9]\d*$", k)
    }
    if stage_defines:
        assign_lines.append(f"{ind}{ind}// Intermediate stage computations (from DEFINE)")
        sorted_names = _topological_sort_defines(stage_defines)
        for def_name in sorted_names:
            def_expr = stage_defines[def_name]
            ucl_type = _infer_stage_type(def_name, parsed)
            # Rename the define var itself
            local_name = _rename_stage_vars(def_name, state_var_names, neural_var)
            # Translate expression, using prop_to_local substitutions
            expr_with_locals = def_expr
            for prop_key, local in prop_to_local.items():
                expr_with_locals = re.sub(
                    r"\b" + re.escape(prop_key) + r"\b",
                    local, expr_with_locals
                )
            ucl_expr = translate_expr(expr_with_locals, {}, state_var_names, neural_var)
            var_decl_lines.append(f"{ind}{ind}var {local_name} : {ucl_type};")
            assign_lines.append(f"{ind}{ind}{local_name} = {ucl_expr};")
        assign_lines.append("")

    # Emit all var declarations first, then all assignment statements
    lines.extend(var_decl_lines)
    if var_decl_lines:
        lines.append("")
    lines.extend(assign_lines)

    # Step 3: State update assignments
    lines.append(f"{ind}{ind}// State updates")
    for var_name, next_expr in parsed.next_assigns.items():
        if var_name == neural_var:
            continue
        # Check for top-level non-deterministic set {0, 1, ..., N}
        set_m = re.match(r"\{([^}]+)\}", next_expr.strip())
        if set_m:
            vals = [v.strip() for v in set_m.group(1).split(",")]
            if all(re.match(r"^-?\d+$", v) for v in vals):
                lo, hi = min(int(v) for v in vals), max(int(v) for v in vals)
                lines.append(f"{ind}{ind}havoc {var_name};")
                lines.append(f"{ind}{ind}assume ({var_name} >= {lo} && {var_name} <= {hi});")
                continue
        # Check if a case expression contains a {set} arm (conditional non-det)
        if "{" in next_expr and re.search(r":\s*\{[^}]+\}", next_expr):
            lines.extend(
                _render_conditional_havoc(var_name, next_expr, prop_to_local,
                                          state_var_names, neural_var, ind)
            )
            continue
        # Deterministic case/expr
        expr_with_locals = next_expr
        for prop_key, local in prop_to_local.items():
            expr_with_locals = re.sub(
                r"\b" + re.escape(prop_key) + r"\b",
                local, expr_with_locals
            )
        ucl_expr = translate_expr(expr_with_locals, {}, state_var_names, neural_var)
        lines.append(f"{ind}{ind}{var_name}' = {ucl_expr};")

    # Neural var: non-deterministic each step
    lines.append(f"{ind}{ind}havoc {neural_var};")
    lines.append(f"{ind}}}")
    lines.append("")

    # --- Safety invariants (from INVARSPEC) ---
    # Collect constant DEFINEs (non-stage, integer literal values) for substitution
    const_defs = {
        k: v for k, v in parsed.defines.items()
        if not re.search(r"_stage_\d+$", k) and re.match(r"^-?\d+$", v.strip())
    }

    if parsed.invarspecs:
        lines.append(f"{ind}// --- Safety properties (from INVARSPEC) ---")
        for idx, spec in enumerate(parsed.invarspecs):
            # Substitute constant DEFINEs (obstacles, obstacle_sizes, etc.)
            spec_subst = spec
            for const_name, const_val in const_defs.items():
                spec_subst = re.sub(
                    r"\bsystem\." + re.escape(const_name) + r"\b",
                    const_val.strip(), spec_subst
                )
                spec_subst = re.sub(
                    r"\b" + re.escape(const_name) + r"\b",
                    const_val.strip(), spec_subst
                )
            ucl_spec = translate_expr(
                spec_subst, node_props, state_var_names, neural_var,
                invarspec_mode=True,
            )
            lines.append(f"{ind}invariant safety_{idx} : {ucl_spec};")
        lines.append("")

    # --- Verification control ---
    lines.append(f"{ind}control {{")
    lines.append(f"{ind}{ind}bmc ({bmc_steps});")
    lines.append(f"{ind}{ind}check;")
    lines.append(f"{ind}{ind}print_results;")
    lines.append(f"{ind}}}")
    lines.append("")
    lines.append("}")

    return "\n".join(lines) + "\n"


def _stage_order(name: str) -> int:
    """Sort key: extract stage number from x_stage_N."""
    m = re.search(r"_stage_(\d+)$", name)
    return int(m.group(1)) if m else 0


def _infer_stage_type(def_name: str, parsed: SMVParsed) -> str:
    """Infer the UCLID5 type of a stage variable from the corresponding stage_0 var."""
    base = re.sub(r"_stage_\d+$", "", def_name)
    smv_type = parsed.state_vars.get(base, "")
    if smv_type == "boolean":
        return "boolean"
    enum_m = re.match(r"\{([^}]+)\}", smv_type)
    if enum_m:
        vals = [v.strip() for v in enum_m.group(1).split(",")]
        if not all(re.match(r"^-?\d+$", v) for v in vals):
            return _enum_type_name(vals)
    return "integer"


# ---------------------------------------------------------------------------
# A/G contract injection
# ---------------------------------------------------------------------------


def inject_contract_assumes(
    ucl: str,
    contracts: list[dict[str, Any]],
    neural_var: str,
    pos_x: str,
    pos_y: str,
    dir_map: dict[str, str],
) -> str:
    """Replace CONTRACT_INJECT_MARKER with global assume statements."""
    assume_lines: list[str] = []
    ind = "  "
    for i, c in enumerate(contracts):
        cx, cy = c["source"]
        label = dir_map.get(c["forbidden_dir"], c["forbidden_dir"])
        assume_lines.append(
            f"{ind}assume contract_{i} : "
            f"({pos_x} == {cx} && {pos_y} == {cy}) ==> ({neural_var} != {label});"
        )
    block = "\n".join(assume_lines)
    return ucl.replace(f"{ind}// CONTRACT_INJECT_MARKER", block, 1)


# ---------------------------------------------------------------------------
# NN DEFINE removal
# ---------------------------------------------------------------------------


def _remove_neural_define(smv_text: str, neural_var: str) -> str:
    """
    Remove the NEURAL variable's DEFINE lookup table from the SMV text.
    The pattern matches the giant case statement generated by dsl_to_nuxmv.
    """
    neural_smv = neural_var + "_stage_0"
    pattern = (
        r"        " + re.escape(neural_smv) + r" :=\n"
        r"            case\n"
        r".*?"
        r"            esac;\n"
    )
    result, n = re.subn(pattern, "", smv_text, flags=re.DOTALL)
    if n == 0:
        raise ValueError(
            f"NN DEFINE block for '{neural_smv}' not found. "
            "Check --neural-var matches the .tree file."
        )
    print(f"  Removed {n} NN DEFINE block(s) for '{neural_smv}'")
    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def dsl_with_contracts_to_uclid5(
    metamodel_file: str,
    tree_file: str,
    output_file: str,
    contracts_file: str,
    neural_var: str,
    pos_x: str,
    pos_y: str,
    domain: list[str],
    dir_map: dict[str, str],
    bmc_steps: int = 50,
    keep_last_stage: bool = False,
    do_not_trim: bool = False,
    skip_grammar_check: bool = False,
    recursion_limit: int = 0,
    record_times: str | None = None,
) -> None:
    """Full pipeline: .tree + contracts JSON → UCLID5 .ucl file."""
    print(f"\n[1/4] Loading contracts from {contracts_file}")
    contracts = load_sat_contracts(contracts_file)

    print(f"\n[2/4] Generating base SMV from {tree_file}")
    tmp = tempfile.NamedTemporaryFile(suffix=".smv", delete=False, mode="w")
    tmp.close()
    try:
        _base.dsl_to_nuxmv(
            metamodel_file, tree_file, tmp.name,
            False, keep_last_stage, do_not_trim, False,
            recursion_limit, False, skip_grammar_check, record_times,
        )

        with open(tmp.name, encoding="utf-8") as f:
            smv_text = f.read()

        print(f"\n[3/4] Removing NN DEFINE block and parsing SMV")
        smv_text = _remove_neural_define(smv_text, neural_var)
        parsed = parse_behaverify_smv(smv_text)
        print(f"  State vars:    {len(parsed.state_vars)}")
        print(f"  BT instances:  {len(parsed.bt_instances)}")
        print(f"  DEFINE stages: {sum(1 for k in parsed.defines if '_stage_' in k)}")
        print(f"  INVARSPEC:     {len(parsed.invarspecs)}")

        print(f"\n[4/4] Building UCLID5 model and injecting contracts")
        node_props = compute_bt_node_expressions(parsed)
        ucl = render_uclid5(
            parsed, node_props, neural_var, domain, bmc_steps,
            tree_file, contracts_file,
        )
        ucl = inject_contract_assumes(ucl, contracts, neural_var, pos_x, pos_y, dir_map)

        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ucl)
        print(f"  Injected {len(contracts)} A/G contract assumes")
        print(f"  Output: {output_file}")

    finally:
        os.unlink(tmp.name)

    print("\nDone.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Generate a UCLID5 model from a BehaVerify .tree file "
            "with verified A/G contracts as assume constraints."
        )
    )
    p.add_argument("--metamodel",   required=True, help="Path to behaverify.tx")
    p.add_argument("--tree",        required=True, help="Path to .tree input file")
    p.add_argument("--contracts",   required=True, help="Path to contract_results.json")
    p.add_argument("--output",      required=True, help="Output .ucl file path")
    p.add_argument("--neural-var",  required=True,
                   help='NN variable name in the .tree file (e.g. "network")')
    p.add_argument("--pos-x",       required=True,
                   help='X-position variable name (e.g. "drone_x")')
    p.add_argument("--pos-y",       required=True,
                   help='Y-position variable name (e.g. "drone_y")')
    p.add_argument("--domain",      nargs="+", required=True,
                   help="NN output domain labels (e.g. left right up down no_action)")
    p.add_argument("--dir-map",     default=None,
                   help="JSON dict mapping contract dir labels to domain labels")
    p.add_argument("--bmc-steps",   type=int, default=50,
                   help="Number of BMC steps (default: 50)")
    p.add_argument("--keep-last-stage",     action="store_true")
    p.add_argument("--do-not-trim",         action="store_true")
    p.add_argument("--skip-grammar-check",  action="store_true")
    p.add_argument("--recursion-limit",     type=int, default=0)
    p.add_argument("--record-times",        default=None)
    args = p.parse_args()

    dir_map = json.loads(args.dir_map) if args.dir_map else DEFAULT_DIR_MAP

    dsl_with_contracts_to_uclid5(
        metamodel_file    = args.metamodel,
        tree_file         = args.tree,
        output_file       = args.output,
        contracts_file    = args.contracts,
        neural_var        = args.neural_var,
        pos_x             = args.pos_x,
        pos_y             = args.pos_y,
        domain            = args.domain,
        dir_map           = dir_map,
        bmc_steps         = args.bmc_steps,
        keep_last_stage   = args.keep_last_stage,
        do_not_trim       = args.do_not_trim,
        skip_grammar_check= args.skip_grammar_check,
        recursion_limit   = args.recursion_limit,
        record_times      = args.record_times,
    )


if __name__ == "__main__":
    main()
