'''
conver btree dsl to behaverify
'''
import argparse
import pprint
import os
# import sys
# import itertools
import copy
import textx
# import serene_functions
from ros_behaverify_to_smv import write_smv

from ros_behaverify_common import create_node_name, create_node_template, create_variable_template


# decoy functions


def is_array(_):
    '''hi'''
    return False


def is_local(_):
    '''hi'''
    return False


def build_range_func(_):
    '''hi'''
    return lambda x: x


# --------from old verstion


def make_new_stage(statement, misc_args):
    '''make a new stage'''
    return (
        [(format_code(case_result.condition, misc_args),
          format_code(case_result.update_value, misc_args))
         for case_result in statement.updates]
        +
        [('TRUE',
          format_code(statement.default_update, misc_args))]
    )


# a NEXT_VALLUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE


# -------------- FUNCTIONS


def format_function_before(function_name, code, misc_args):
    '''function_name(vals)'''
    return (
        function_name + '('
        + ', '.join([format_code(value, misc_args) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, misc_args):
    '''(vals function_name vals)'''
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, misc_args) for value in code.function_call.values])
        + ')'
        )


def format_function_after(function_name, code, _):
    '''(node_name.function_name)'''
    return (
        '('
        + code.function_call.node_name
        + function_name
        + ')'
        )


def format_function_before_bounded(function_name, code, misc_args):
    '''function_name [min, max] (vals)'''
    return (
        function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] '  '('
        + ', '.join([format_code(value, misc_args) for value in code.function_call.values])
        + ')'
        )


def format_function_between_bounded(function_name, code, misc_args):
    ''' honestly not sure '''
    return (
        '('
        + (' ' + function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] ').join([format_code(value, misc_args) for value in code.function_call.values])
        + ')'
        )


def format_function_before_between(function_name, code, misc_args):
    '''probably some spec thing'''
    return (
        function_name[0] + '['
        + (' ' + function_name[1] + ' ').join([format_code(value, misc_args) for value in code.function_call.values])
        + ']'
        )


def format_function_index(_, code, misc_args):
    '''variable[val]'''
    return (
        format_variable(code.function_call.variable, misc_args) + '[' + format_code(code.function_call.values[0], misc_args) + ']'
    )


def format_function_non_determinism(_, code, misc_args):
    '''deal with non_determinism'''
    return (
        '{'
        + ', '.join([format_code(value, misc_args) for value in code.function_call.values])
        + '}'
    )


def format_function(code, misc_args):
    '''this just calls the other format functions. moved here to make format_code less cluttered.'''
    (function_name, function_to_call) = FUNCTION_FORMAT[code.function_call.function_name]
    return function_to_call(function_name, code, misc_args)


def create_misc_args(node_name, use_stages, use_next, not_next, overwrite_stage):
    '''
    -- ARGUMENTS
    @ node_name := the name of the node which caused this to be called. used for formatting local variables.
    @ use_stages := are we using stages for this? (note: does not affect variable renaming).
    @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
    @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
    @ overwrite_stage := overwrite which stage we're asking for.
    '''
    return {
        'node_name' : node_name,
        'use_stages' : use_stages,
        'use_next' : use_next,
        'not_next' : not_next,
        'overwrite_stage' : overwrite_stage,
    }


def compute_stage(variable_key, misc_args):
    '''
    compute the stage for the variable now
    -- GLOBALS
    @ variables := a dictionary of variables
    -- arguments
    @ variable_key := used to index into the variable.
    @ use_stages := if true, use stages
    @ overwrite_stage := forces a specific stage
    -- return
    @ the string with appropriate stage number
    -- side effects
    none.
    '''
    variables = global_vars['variables']
    variable = variables[variable_key]

    # node_name = misc_args['node_name']
    # use_stages = misc_args['use_stages']
    # use_next = misc_args['use_next']
    # not_next = misc_args['not_next']
    # init_mode = misc_args['init_mode']
    overwrite_stage = misc_args['overwrite_stage']
    return (
        '_stage_'
        + str(
            len(variable['next_value'])
            if overwrite_stage is None or overwrite_stage < 0
            else
            min(overwrite_stage, len(variable['next_value']))
        )
    )


def find_used_variables(code, misc_args):
    '''Returns the list of used variables (will also format them)'''
    return (
        [] if code.constant is not None else (
            [format_variable(code.variable, misc_args)] if code.variable is not None else (
                find_used_variables(code.code_statement, misc_args) if code.code_statement is not None else (
                    [variable for value in code.function_call.values for variable in find_used_variables(value, misc_args)]
                    +
                    ([format_variable(code.function_call.variable, misc_args)] if code.function_call.function_name == 'index' else [])
                )
            )
        )
    )


def format_variable(variable_obj, misc_args):
    '''
    -- GLOBALS
    @ variables := a dict of all variables
    -- ARGUMENTS
    @ variable_obj := a textx object of a variable that we will be formatting.
    @ node_name := the name of the node which caused this to be called.
    @ use_stages := are we using stages for this?
    @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
    @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
    @ overwrite_stage := overwrite which stage we're asking for.
    '''
    # global variables
    variables = global_vars['variables']

    node_name = misc_args['node_name']
    use_stages = misc_args['use_stages']
    use_next = misc_args['use_next']
    not_next = misc_args['not_next']
    overwrite_stage = misc_args['overwrite_stage']

    variable_key = variable_reference(variable_obj.name, is_local(variable_obj), node_name)
    variable = variables[variable_key]

    # if variable['mode'] == 'DEFINE':
    #     if overwrite_stage is not None:
    #         return (
    #             ('' if not use_next else 'next(')
    #             + variable['prefix']
    #             + variable['name']
    #             + '_stage_' + str(overwrite_stage)
    #             + ('' if not use_next else ')'))
    #     used_vars = []
    #     if is_array(variable_obj) and variable_obj.array_mode != 'range':
    #         for assign in variable_obj.assigns:
    #             if assign.default_result.range_mode != 'range':
    #                 for code_fragment in assign.default_result.values:
    #                     used_vars += find_used_variables(code_fragment, misc_args)
    #             for case_result in assign.case_results:
    #                 if case_result.range_mode != 'range':
    #                     for code_fragment in case_result.values:
    #                         used_vars += find_used_variables(code_fragment, misc_args)
    #                 used_vars += find_used_variables(case_result.condition, misc_args)
    #     else:
    #         if variable_obj.assign.default_result.range_mode != 'range':
    #             for code_fragment in variable_obj.assign.default_result.values:
    #                 used_vars += find_used_variables(code_fragment, misc_args)
    #         for case_result in variable_obj.assign.case_results:
    #             if case_result.range_mode != 'range':
    #                 for code_fragment in case_result.values:
    #                     used_vars += find_used_variables(code_fragment, misc_args)
    #             used_vars += find_used_variables(case_result.condition, misc_args)
    #     used_vars = tuple(sorted(list(set(used_vars))))
    #     if used_vars not in variable['existing_definitions']:
    #         variable['existing_definitions'][used_vars] = len(variable['next_value'])
    #         variable['next_value'].append(handle_variable_statement(variable_obj, variable_obj, None, misc_args))
    #     stage = variable['existing_definitions'][used_vars]
    #     return (
    #         ('' if not use_next else 'next(')
    #         + variable['name']
    #         + '_stage_' + str(stage)
    #         + ('' if not use_next else ')'))

    if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
        variable['keep_stage_0'] = True
    if use_next and variable_key == not_next:
        return 'LINK_TO_PREVIOUS_FINAL_' + variable['name']
    return (('' if not use_next else 'next(')
            + variable['name']
            + compute_stage(variable_key, misc_args)
            + ('' if not use_next else ')'))


def adjust_args(code, misc_args):
    '''
    creates a new arg based on the old one, but modifies it. should only be used by format_code
    Declared not as nested function cuz that would tank performance.
    '''
    new_misc_args = copy.deepcopy(misc_args)
    new_misc_args['node_name'] = code.node_name if hasattr(code, 'node_name') else new_misc_args['node_name']
    new_misc_args['overwrite_stage'] = code.read_at if hasattr(code, 'read_at') else new_misc_args['overwrite_stage']
    return new_misc_args



def format_code(code, misc_args):
    '''format code'''
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, adjust_args(code, misc_args))) if code.variable is not None else (
                ('(' + format_code(code.CodeStatement, misc_args) + ')') if code.CodeStatement is not None else (
                    format_function(code, misc_args)
                )
            )
        )
    )


def handle_specifications(specifications):
    '''this handles specifications'''
    return [
        (
            specification.spec_type
            + ' '
            + format_code(specification.CodeStatement, create_misc_args(None, True, False, None, None))
            + ';'
        )
        for specification in specifications
        ]


def handle_constant(constant):
    '''this handles a constant by checking if it is in constants and replacing if appropriate'''
    constants = global_vars['constants']
    if constant == 'serene_index':
        return global_vars['serene_index'][-1]
    return (constants[constant] if constant in constants else constant)


def variable_reference(base_name, _is_local_, node_name):
    '''
    creates the name used to store the variable in variables.
    -- arguments
    @ base_name := what is normally stored in 'variable_name'
    @ is_local := is the variable local
    @ node_name := the name of the node (only relevant if local)
    @ is_env := is the variable an environment_variable
    -- return
    @ UNNAMED := returns the variable name
    -- side effects
    none
    '''
    return ((node_name + '_DOT_' + base_name) if _is_local_ else base_name)



def get_variables(model, keep_stage_0):
    '''
    this constructs and returns variables and local variables.
    variables are constructed based on variables and environment_variables
    -- arguments
    @ model := a model. one created using behaverify.tx as the metamodel (probably)
    @ keep_stage_0 := a boolean. indicates if we should be default keep_stage_0.
    -- return
    @ variables := a dictionary from variable_name (string) to variable informaion
    @ local_variables := a dictionary from variable_name (string) to variable informaion
    -- side effects
    none. purely functional.
    '''

    def build_custom_range(variable, expand_int):
        if expand_int:
            return (
                (
                    '{'
                    + ', '.join(map(str, range(variable.model.range_minimum, variable.model.range_maximum + 1)))
                    + '}'
                )
                if variable.model.range_minimum is not None
                else
                (
                    '{TRUE, FALSE}'
                    if variable.model.is_bool is not None
                    else
                    ('{' + ', '.join(map(str, variable.model.enums)) + '}')
                )
            )
        else:
            return (None if variable.model.range_minimum is not None else ('{TRUE, FALSE}' if variable.model.is_bool is not None else ('{' + ', '.join(map(str, variable.model.enums)) + '}')))

    return {variable.name :
            create_variable_template(
                variable.name,
                'DEFINE' if (len(variable.model.enums) == 1) else 'VAR',
                None,
                build_custom_range(variable, False),
                0 if variable.model.range_minimum is None else variable.model.range_minimum,
                1 if variable.model.range_minimum is None else variable.model.range_maximum,
                (
                    (None, False, [('TRUE', build_custom_range(variable, True))])
                    if variable.initial_value is None
                    else
                    (None, False, [('TRUE', (str(variable.initial_value).upper() if isinstance(variable.initial_value, bool) else str(variable.initial_value)))])
                ),
                [],
                keep_stage_0 = keep_stage_0
            )
            for variable in model.bbVariables if variable.model is not None}


def is_nondeterministic(code):
    ''' searches if there is any nondeterminism in this statement '''
    return (
        False if (code.constant is not None or code.variable is not None) else (
            is_nondeterministic(code.CodeStatement) if code.CodeStatement is not None else (
                True if code.function_call.function_name == 'any' else (
                    any([is_nondeterministic(value) for value in code.function_call.values])
                    )
                )
            )
        )


def walk_tree(model):
    '''driver method for getting nodes from model'''
    nodes = {}
    walk_tree_recursive(model.tree.btree, None, nodes, set(), {})
    return nodes



def walk_tree_recursive(current_node, parent_name, nodes, node_names, node_names_map):
    '''actual work method for getting nodes from model'''
    metamodel = global_vars['metamodel']
    variables = global_vars['variables']
    if hasattr(current_node, 'name'):
        # next, we get the name of this node, and correct for duplication
        new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        node_names.add(node_name)
        node_names_map[current_node.name.replace(' ', '')] = modifier

        if parent_name is not None:
            nodes[parent_name]['children'].append(node_name)
            # update parent's list of children
    else:
        node_name = None

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    if textx.textx_isinstance(current_node, metamodel['SeqBTNode']):
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'composite',
                                                'sequence',
                                                '',
                                                'with_partial_memory',
                                                True, True, True)
    elif textx.textx_isinstance(current_node, metamodel['SelBTNode']):
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'composite',
                                                'selector',
                                                '',
                                                '',
                                                True, True, True)
    elif textx.textx_isinstance(current_node, metamodel['ParBTNode']):
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'composite',
                                                'parallel',
                                                '_success_on_all',
                                                '',
                                                True, True, True)

    elif textx.textx_isinstance(current_node, metamodel['SIFBTNode']):
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'decorator',
                                                'X_is_Y',
                                                '',
                                                '',
                                                False, True, True,
                                                additional_arguments = ['success', 'failure'])

        # ok, we've added the decorator. now we add in the selector node
        parent_name = node_name
        # selector is going to use the same name as the decorator.
        # next, we get the name of this node, and correct for duplication
        new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        node_names.add(node_name)
        node_names_map[current_node.name.replace(' ', '')] = modifier

        if parent_name is not None:
            nodes[parent_name]['children'].append(node_name)
            # update parent's list of children
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'composite',
                                                'selector',
                                                '',
                                                '',
                                                True, True, True)
        # selector added
        selector_name = node_name  # store this. we will restore it after adding the checks in
        decorator_name = parent_name

        parent_name = node_name
        # ok, now we add all the checks, which are here for some reason.
        for check in current_node.checks:
            new_name = create_node_name(check.name.replace(' ', ''), node_names, node_names_map)
            node_name = new_name[0]
            modifier = new_name[1]
            node_names.add(node_name)
            node_names_map[check.name.replace(' ', '')] = modifier

            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            variable_name = format_variable(check.bbvar, create_misc_args(node_name, True, False, None, None))

            nodes[node_name] = create_node_template(node_name,
                                                    parent_name,
                                                    [],
                                                    'leaf',
                                                    'check',
                                                    '',
                                                    '',
                                                    True, False, True,
                                                    additional_arguments = [variable_name],
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(' + variable_name + ')' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ('
                                                        + variable_name + ' = ' + (str(check.default).upper() if isinstance(check.default, bool) else str(check.default))
                                                        + ') ? success : failure;' + os.linesep
                                                    ))
        # all checks added in, so now we restore back up to the selector
        node_name = selector_name
        parent_name = decorator_name

    elif textx.textx_isinstance(current_node, metamodel['CheckBTNode']):
        for check in current_node.check:
            new_name = create_node_name(check.name.replace(' ', ''), node_names, node_names_map)
            node_name = new_name[0]
            modifier = new_name[1]
            node_names.add(node_name)
            node_names_map[check.name.replace(' ', '')] = modifier

            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            variable_name = format_variable(check.bbvar, create_misc_args(node_name, True, False, None, None))

            nodes[node_name] = create_node_template(node_name,
                                                    parent_name,
                                                    [],
                                                    'leaf',
                                                    'check',
                                                    '',
                                                    '',
                                                    True, False, True,
                                                    additional_arguments = [variable_name],
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(' + variable_name + ')' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ('
                                                        + variable_name + ' = ' + (str(check.default).upper() if isinstance(check.default, bool) else str(check.default))
                                                        + ') ? success : failure;' + os.linesep
                                                    ))

    elif textx.textx_isinstance(current_node, metamodel['TaskBTNode']):
        for task in current_node.task:
            new_name = create_node_name(task.name.replace(' ', ''), node_names, node_names_map)
            node_name = new_name[0]
            modifier = new_name[1]
            node_names.add(node_name)
            node_names_map[task.name.replace(' ', '')] = modifier

            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            if hasattr(task, 'type'):
                nodes[node_name] = create_node_template(node_name,
                                                        parent_name,
                                                        [],
                                                        'leaf',
                                                        'action',
                                                        '',
                                                        '',
                                                        str(task.type) == 'success', str(task.type) == 'running', str(task.type) == 'failure',
                                                        additional_arguments = [],
                                                        internal_status_module_name = None,
                                                        internal_status_module_code = None)
                continue

            nodes[node_name] = create_node_template(node_name,
                                                    parent_name,
                                                    [],
                                                    'leaf',
                                                    'action',
                                                    '',
                                                    '',
                                                    task.return_status == 'success', task.return_status == 'running', task.return_status == 'failure',
                                                    additional_arguments = [],
                                                    internal_status_module_name = None,
                                                    internal_status_module_code = None)

            for set_var in task.set_vars:
                variable_name = set_var.variable.name
                keep_stage_0 = variables[variable_name]['keep_stage_0']
                non_determinism = is_nondeterministic(set_var.default_update) or any([is_nondeterministic(update.update_value) for update in set_var.updates])
                keep_stage_0 = keep_stage_0 or (not non_determinism)  # if stage_1 is deterministic, then we keep stage 0.
                variables[variable_name]['next_value'].append((node_name,
                                                               non_determinism,
                                                               make_new_stage(set_var, create_misc_args(node_name, True, False, None, None))))
                variables[variable_name]['keep_stage_0'] = keep_stage_0  # reset keep_stage_0 (or properly mark it if non_determinism changed it)

    elif textx.textx_isinstance(current_node, metamodel['MonBTNode']):
        for mon in current_node.mon:
            if mon.ignore_node:
                continue
            new_name = create_node_name(mon.name.replace(' ', ''), node_names, node_names_map)
            node_name = new_name[0]
            modifier = new_name[1]
            node_names.add(node_name)
            node_names_map[mon.name.replace(' ', '')] = modifier
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            nodes[node_name] = create_node_template(node_name,
                                                    parent_name,
                                                    [],
                                                    'leaf',
                                                    'read_action',
                                                    '',
                                                    '',
                                                    True, True, False,
                                                    additional_arguments = [node_name + '_update_success_stage_1'],
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(' + node_name + '_update_success_stage_1)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ' + node_name + '_update_success_stage_1 ? success : running;' + os.linesep))

            variables[node_name + '_update_success'] = create_variable_template(node_name + '_update_success',
                                                                                'VAR',
                                                                                None,
                                                                                '{TRUE, FALSE}',
                                                                                0,
                                                                                1,
                                                                                (node_name, True, [('TRUE', '{TRUE, FALSE}')]),
                                                                                [
                                                                                    (node_name,
                                                                                     True,
                                                                                     [('TRUE', '{TRUE, FALSE}')]
                                                                                     )
                                                                                ], keep_stage_0 = False)

            if (mon.topic_bbvar.name) in variables and (not mon.ignore_topic):
                variable = variables[mon.topic_bbvar.name]
                keep_stage_0 = variable['keep_stage_0']
                variable['next_value'].append((node_name,
                                               True,  # this is assumed to be non_deterministic
                                               [(node_name + '_update_success_stage_1',
                                                 (('{' + ', '.join(map(str, range(variable['min_value'], variable['max_value'] + 1))) + '}') if variable['custom_value_range'] is None else (
                                                     variable['custom_value_range']))),
                                                ('TRUE',
                                                 format_variable(mon.topic_bbvar, create_misc_args(node_name, True, False, None, None)))
                                                ]))
                variable['keep_stage_0'] = keep_stage_0  # we don't want to keep stage 0 if we only changed it during this update.

            for set_var in mon.set_vars:
                variable_name = set_var.variable.name
                keep_stage_0 = variables[variable_name]['keep_stage_0']
                non_determinism = is_nondeterministic(set_var.default_update) or any([is_nondeterministic(update.update_value) for update in set_var.updates])
                keep_stage_0 = keep_stage_0 or (not non_determinism)  # if stage_1 is deterministic, then we keep stage 0.
                variables[variable_name]['next_value'].append((node_name,
                                                               non_determinism,
                                                               [('!(' + node_name + '_update_success_stage_1)', format_variable(set_var.variable, create_misc_args(node_name, True, False, None, None)))]
                                                               + make_new_stage(set_var, create_misc_args(node_name, True, False, None, None))))
                variables[variable_name]['keep_stage_0'] = keep_stage_0  # reset keep_stage_0 (or properly mark it if non_determinism changed it)

    elif textx.textx_isinstance(current_node, metamodel['TimerBTNode']):
        nodes[node_name] = create_node_template(node_name,
                                                parent_name,
                                                [],
                                                'leaf', 'action',
                                                '', '',
                                                True, True, False,
                                                internal_status_module_name = None,
                                                internal_status_module_code = None)

    if node_name is None or nodes[node_name]['category'] == 'leaf':
        pass
    else:
        for child in current_node.nodes:
            walk_tree_recursive(
                child,
                node_name,
                nodes,
                node_names,
                node_names_map
            )

    return


# --------------- CONSTANTS


FUNCTION_FORMAT = {
    'abs' : ('abs', format_function_before),
    'max' : ('max', format_function_before),
    'min' : ('min', format_function_before),
    'sin' : ('sin', format_function_before),
    'cos' : ('cos', format_function_before),
    'tan' : ('tan', format_function_before),
    'ln' : ('ln', format_function_before),
    'not' : ('!', format_function_before),
    'and' : ('&', format_function_between),
    'or' : ('|', format_function_between),
    'xor' : ('xor', format_function_between),
    'xnor' : ('xnor', format_function_between),
    'implies' : ('->', format_function_between),
    'equivalent' : ('<->', format_function_between),
    'equal' : ('=', format_function_between),
    'not_equal' : ('!=', format_function_between),
    'less_than' : ('<', format_function_between),
    'greater_than' : ('>', format_function_between),
    'less_than_or_equal' : ('<=', format_function_between),
    'greater_than_or_equal' : ('>=', format_function_between),
    'negative' : ('-', format_function_before),
    'addition' : ('+', format_function_between),
    'subtraction' : ('-', format_function_between),
    'multiplication' : ('*', format_function_between),
    'division' : ('/', format_function_between),
    'mod' : ('mod', format_function_between),
    'any' : (None, format_function_non_determinism),
    'count' : ('count', format_function_before),
    'index' : ('index', format_function_index),
    'active' : ('.active', format_function_after),
    'success' : ('.status = success', format_function_after),
    'running' : ('.status = running', format_function_after),
    'failure' : ('.status = failure', format_function_after),
    'next' : ('X', format_function_before),
    'globally' : ('G', format_function_before),
    'globally_bounded' : ('G', format_function_before_bounded),
    'finally' : ('F', format_function_before),
    'finally_bounded' : ('F', format_function_before_bounded),
    'until' : ('U', format_function_between),
    'until_bounded' : ('U', format_function_between_bounded),
    'release' : ('V', format_function_between),
    'release_bounded' : ('V', format_function_between_bounded),
    'previous' : ('Y', format_function_before),
    'not_previous_not' : ('Z', format_function_before),
    'historically' : ('H', format_function_before),
    'historically_bounded' : ('H', format_function_before_bounded),
    'once' : ('O', format_function_before),
    'once_bounded' : ('O', format_function_before_bounded),
    'since' : ('S', format_function_between),
    'since_bounded' : ('S', format_function_between_bounded),
    'triggered' : ('T', format_function_between),
    'triggered_bounded' : ('T', format_function_between_bounded),
    'exists_globally' : ('EG', format_function_before),
    'exists_next' : ('EX', format_function_before),
    'exists_finally' : ('EF', format_function_before),
    'exists_until' : (('E', 'U'), format_function_before_between),
    'always_globally' : ('AG', format_function_before),
    'always_next' : ('AX', format_function_before),
    'always_finally' : ('AF', format_function_before),
    'always_until' : (('A', 'U'), format_function_before_between)
}


COMPOSITES = {
    'parallel',
    'sequence',
    'selector',
}


global_vars = {'constants' : {}, 'metamodel' : {}, 'variables' : {}, 'serene_index' : []}


# --------------- Main


def main():
    '''main method'''
    # global constants, metamodel, variables

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    arg_parser.add_argument('--behave_only', action = 'store_true')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    global_vars['metamodel'] = metamodel
    model = metamodel.model_from_file(args.model_file)

    variables = get_variables(model, args.keep_stage_0)
    global_vars['variables'] = variables
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, create_misc_args(None, True, False, None, None))
    specifications = handle_specifications(model.specifications)  # this included here to ensure we don't erase stage 0 used by specifications.
    nodes = walk_tree(model)
    specifications = handle_specifications(model.specifications)

    if args.behave_only:
        if args.output_file is None:
            printer = pprint.PrettyPrinter(indent = 4)
            printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
        else:
            with open(args.output_file, 'w') as f:
                printer = pprint.PrettyPrinter(indent = 4, stream = f)
                printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
    else:
        write_smv(nodes, variables, tick_condition, specifications, args.output_file, args.do_not_trim)
    return


if __name__ == '__main__':
    main()
