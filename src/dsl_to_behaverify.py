import textx
import argparse
import pprint
import os
import sys
import itertools
import copy
import serene_functions

from behaverify_common import create_node_name, create_node_template, create_variable_template

# a NEXT_VALLUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE


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
    # create each variable type using the template.
    global test_variable
    variables = {variable_reference(variable.name, False, '', False) :
                 (
                     create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], 'var_', False)
                     if variable.model_as == 'DEFINE' else
                     create_variable_template(variable.name, variable.model_as,
                                              (None if (variable.domain.min_val is not None or variable.model_as == 'DEFAULT') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                              0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                              1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                              None, [], 'var_', keep_stage_0
                                              )
                  )
                 for variable in model.blackboard_variables}
    env_variables = {variable_reference(variable.name, False, '', True) :
                     (
                         create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], 'env_', False)
                         if variable.model_as == 'DEFINE' else
                         create_variable_template(variable.name, variable.model_as,
                                                  (None if (variable.domain.min_val is not None or variable.model_as == 'DEFAULT') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                                  0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                                  1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                                  None, [], 'env_', keep_stage_0
                                                  )
                     )
                     for variable in model.environment_variables}
    variables.update(env_variables)
    local_variables = {variable.name :
                       (
                           create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], '', False)
                           if variable.model_as == 'DEFINE' else
                           create_variable_template(variable.name, variable.model_as,
                                                    (None if (variable.domain.min_val is not None or variable.model_as == 'DEFAULT') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                                    0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                                    1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                                    None, [], '', keep_stage_0
                                                    )
                       )
                       for variable in model.local_variables}

    for variable in model.blackboard_variables:
        if variable.model_as == 'DEFINE':
            variables[variable_reference(variable.name, False, '', False)]['existing_definitions'] = {}
        else:
            variables[variable_reference(variable.name, False, '', False)]['initial_value'] = make_new_stage(variable.initial_value, None, variables, local_variables, False, False, None)
    for variable in model.environment_variables:
        if variable.model_as == 'DEFINE':
            variables[variable_reference(variable.name, False, '', True)]['existing_definitions'] = {}
        else:
            variables[variable_reference(variable.name, False, '', True)]['initial_value'] = make_new_stage(variable.initial_value, None, variables, local_variables, False, False, None)
    for variable in model.local_variables:
        if variable.model_as == 'DEFINE':
            local_variables[variable.name]['existing_definitions'] = {}
        else:
            local_variables[variable.name]['initial_value'] = make_new_stage(variable.initial_value, None, variables, local_variables, False, False, None)
    return (variables, local_variables)


RANGE_FUNCTION = {
    'abs' : serene_functions.serene_abs,
    'max' : serene_functions.serene_max,
    'min' : serene_functions.serene_min,
    'sin' : serene_functions.serene_sin,
    'cos' : serene_functions.serene_cos,
    'tan' : serene_functions.serene_tan,
    'ln' : serene_functions.serene_log,
    'not' : serene_functions.serene_not,
    'and' : serene_functions.serene_and,
    'or' : serene_functions.serene_or,
    'xor' : serene_functions.serene_xor,
    'xnor' : serene_functions.serene_xnor,
    'implies' : serene_functions.serene_implies,
    'equivalent' : serene_functions.serene_eq,
    'equal' : serene_functions.serene_eq,
    'not_equal' : serene_functions.serene_ne,
    'less_than' : serene_functions.serene_lt,
    'greater_than' : serene_functions.serene_gt,
    'less_than_or_equal' : serene_functions.serene_lte,
    'greater_than_or_equal' : serene_functions.serene_gte,
    'negative' : serene_functions.serene_neg,
    'addition' : serene_functions.serene_sum,
    'subtraction' : serene_functions.serene_sub,
    'multiplication' : serene_functions.serene_mult,
    'division' : serene_functions.serene_truediv,
    'mod' : serene_functions.serene_mod,
    'count' : serene_functions.serene_count
}


def build_range_func(code):
    return (
        (lambda x : handle_constant(code.constant)) if code.constant is not None else (
            (lambda x : x) if code.value else (
                build_range_func(code.code_statement) if code.code_statement is not None else (
                    (lambda x : RANGE_FUNCTION[code.function_call.function_name]([build_range_func(value) for value in code.function_call.values], x))
                )
            )
        )
    )


def make_new_stage(statement, node_name, variables, local_variables, use_stages, use_next, not_next):
    '''
    this creates a new_stage and returns it.
    the stage consists of (conditions, results) pairs in order.
    if a condition is met, that value is used.
    the last condition is always TRUE, ensuring at least one condition will be met.
    -- arguments
    @ statement := a code statement (see grammar defined in behaverify.tx)
     -> the statement contains the information we need.
    @ node_name := the name of the node to use string usually, can be None.
     -> this is used by methods called by make_new_stage.
    @ variables := a dictionary of variables_names to variable_info
    @ local_variables := a dictionary of variable_names to variable_info
    @ use_stages := a boolean.
     -> if true, variables will be formattted to use their current stage.
     -> if false, variables will just use their name
    @ use_next := a boolean
     -> usually false. This is only True in the case where we've decided we will
     -> be deleting stage_0, and therefore stage_1 must use next statements.
    @ not_next := a string or None.
     -> Only relevant if use_next is true. in that case, this is the name of the
     -> variable which is having stage_0 deleted, which requires some mapping.
     -> Should only be None if use_next is False.
    -- return
    @ UNNAMED := a new stage is returned.
    -- side effects
    none directly. however, this method calls format_code which calls format_variable
    format_variable has side effects. can modify variables.
    '''
    return (
        [
            (
                format_code(case_result.condition, node_name, variables, local_variables, use_stages, use_next, not_next)
                ,
                (
                    (
                        '{'
                        + ', '.join([str(value) for value in range(handle_constant(case_result.values[0]), handle_constant(case_result.values[1]) + 1)
                                     if cond_func(value)])
                        + '}'
                    )
                    if (case_result.range_mode and ((cond_func := build_range_func(case_result.values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
                    (
                        ('{' if len(case_result.values) > 1 else '')
                        + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next)
                                     for value in case_result.values])
                        + ('}' if len(case_result.values) > 1 else '')
                    )
                )
            )
            for case_result in statement.case_results
        ]
        +
        [
            (
                'TRUE'
                ,
                (
                    (
                        '{'
                        + ', '.join([str(value) for value in range(handle_constant(statement.default_result.values[0]), handle_constant(statement.default_result.values[1]) + 1)
                                     if cond_func(value)])
                        + '}'
                    )
                    if (statement.default_result.range_mode and ((cond_func := build_range_func(statement.default_result.values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
                    (
                        ('{' if len(statement.default_result.values) > 1 else '')
                        + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next)
                                     for value in statement.default_result.values])
                        + ('}' if len(statement.default_result.values) > 1 else '')
                    )
                )
            )
        ]
    )


def handle_constant(constant):
    global constants
    return (constants[constant] if constant in constants else constant)


def variable_reference(base_name, is_local, node_name, is_env):
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
    return (
        ('env_' if is_env else ((node_name + '_DOT_') if is_local else ('')))
        + base_name)


def complete_environment_variables(model, variables, local_variables, delayed_statements):
    '''
    completes the environment variables.
    -- arguments
    @ model := a model.
    @ variables := a dictionary of variables
    @ local_variables := a dictionary of local variables that will be used to create new variable
    @ delayed_statements := a list of statements that need to be processed now
    -- return
    no return
    -- side effects
    changes variables.
    '''
    for (node_name, statement) in delayed_statements:
        new_stage = make_new_stage(statement, node_name, variables, local_variables, True, False, None)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((node_name, non_determinism, new_stage))

    # for statement in model.initial:
    #     new_stage = make_new_stage(statement, None, variables, {}, False, False, False)
    #     variable_name = variable_reference(statement.variable.name, False, '', True)
    #     variables[variable_name]['initial_value'] = new_stage

    for statement in model.update:
        new_stage = make_new_stage(statement, None, variables, {}, True, False, False)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((None, non_determinism, new_stage))

    return


def compute_stage(variable_key, variables, use_stages, overwrite_stage = None):
    '''
    compute the stage for the variable now
    -- arguments
    @ variable_key := used to index into the variable.
    @ variables := a dictionary of variables
    @ use_stages := if true, use stages
    @ overwrite_stage := forces a specific stage
    -- return
    @ the string with appropriate state number
    -- side effects
    none.
    '''
    if overwrite_stage is not None:
        return (('_stage_' + str(min(overwrite_stage, len(variables[variable_key]['next_value']))) if overwrite_stage > 0 else (
            '' if overwrite_stage == 0 else (
                '_stage_' + str(len(variables[variable_key]['next_value']))
            ))))
    return (('_stage_' + str(len(variables[variable_key]['next_value']))) if (use_stages and len(variables[variable_key]['next_value']) > 0) else (''))


def add_local_variable(variables, local_variables, variable_name, variable_key):
    variables[variable_key] = copy.deepcopy(local_variables[variable_name])
    variables[variable_key]['name'] = variable_key
    return


def format_variable(variable_obj, is_local, node_name, is_env, variables, local_variables, use_stages, use_next, not_next, overwrite_stage = None):
    variable_key = variable_reference(variable_obj.name, is_local, node_name, is_env)
    if variable_key not in variables:
        add_local_variable(variables, local_variables, variable_obj.name, variable_key)
    variable = variables[variable_key]
    if variable['mode'] == 'DEFINE':
        used_vars = []
        for code_fragment in variable_obj.initial_value.default_result.values:
            used_vars += find_used_variables(code_fragment, node_name, variables, local_variables, use_stages)
        for case_result in variable_obj.initial_value.case_results:
            for code_fragment in case_result.values:
                used_vars += find_used_variables(code_fragment, node_name, variables, local_variables, use_stages)
            used_vars += find_used_variables(case_result.condition, node_name, variables, local_variables, use_stages)
        used_vars = tuple(sorted(list(set(used_vars))))
        if used_vars not in variable['existing_definitions']:
            variable['existing_definitions'][used_vars] = len(variable['next_value'])
            variable['next_value'].append(make_new_stage(variable_obj.initial_value, node_name, variables, local_variables, use_stages, use_next, not_next))
        stage = variable['existing_definitions'][used_vars]
        return (
            ('' if not use_next else 'next(')
            + variable['prefix']
            + variable['name']
            + '_stage_' + str(stage)
            + ('' if not use_next else ')'))

    if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
        variable['keep_stage_0'] = True
    if use_next and variable_key == not_next:
        return 'LINK_TO_PREVIOUS_FINAL_' + variable['prefix'] + variable['name']
    return (('' if not use_next else 'next(')
            + variable['prefix']
            + variable['name']
            + compute_stage(variable_key, variables, use_stages, overwrite_stage)
            + ('' if not use_next else ')'))


def format_function_before(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        function_name + '('
        + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_after(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        '('
        + code.function_call.node_name
        + function_name
        + ')'
        )


def format_function_before_bounded(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] '  '('
        + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_between_bounded(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] ').join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_before_between(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        function_name[0] + '('
        + (' ' + function_name[1] + ' ').join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


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
    'count' : ('count', format_function_before),
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


def format_function(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    (function_name, function_to_call) = FUNCTION_FORMAT[code.function_call.function_name]
    return function_to_call(function_name, code, node_name, variables, local_variables, use_stages, use_next, not_next)


def format_code(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(handle_constant(code.constant))) if code.constant is not None else (
            (format_variable(code.variable, (code.mode == 'local'), (code.node_name if hasattr(code, 'node_name') else node_name), (code.mode == 'env'), variables, local_variables, use_stages, use_next, not_next, (code.read_at if hasattr(code, 'read_at') else None))) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name, variables, local_variables, use_stages, use_next, not_next) + ')') if code.code_statement is not None else (
                    format_function(code, node_name, variables, local_variables, use_stages, use_next, not_next)
                )
            )
        )
    )


def find_used_variables(code, node_name, variables, local_variables, use_stages):
    return (
        [] if code.constant is not None else (
            [format_variable(code.variable, (code.mode == 'local'), node_name, (code.mode == 'env'), variables, local_variables, use_stages, False, None)] if code.variable is not None else (
                find_used_variables(code.code_statement, node_name, variables, local_variables, use_stages) if code.code_statement is not None else (
                    [variable for value in code.function_call.values for variable in find_used_variables(value, node_name, variables, local_variables, use_stages)]
                    )
                )
            )
        )


def create_sequence_selector(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    return create_node_template(node_name, parent_name, 'composite',
                                current_node.node_type + ('_with_memory' if current_node.memory else '_without_memory'),
                                True, True, True)


def create_parallel(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    return create_node_template(node_name, parent_name, 'composite',
                                (current_node.node_type
                                 + ('_' + current_node.parallel_policy + '_without_memory' if not current_node.memory else (
                                     '_success_on_all_with_memory')
                                    )
                                 ),
                                True, True, True)


def create_X_is_Y(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    if current_node.x == current_node.y:
        print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
        sys.exit()
    return create_node_template(node_name, parent_name, 'decorator', 'X_is_Y',
                                (current_node.x != 'success'), (current_node.x != 'running'), (current_node.x != 'failure'),
                                additional_arguments = [current_node.x, current_node.y])


def create_inverter(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    return create_node_template(node_name, parent_name, 'decorator', 'inverter',
                                True, True, True)


def create_check(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    variable_list = (
        find_used_variables(current_node.condition,
                            node_name, variables, local_variables,
                            True)
        if current_node.condition is not None else [])

    variable_set = [*set(variable_list)]  # remove duplicates, but force a specific order.

    return create_node_template(node_name, parent_name, 'leaf', current_node.node_type,
                                True, False, True,
                                additional_arguments = variable_set,
                                internal_status_module_name = node_name + '_module',
                                internal_status_module_code = (
                                    'MODULE ' + node_name + '_module(' + ', '.join(variable_set) + ')' + os.linesep
                                    + '\tCONSTANTS' + os.linesep
                                    + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                    + '\tDEFINE' + os.linesep
                                    + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                    + '\t\tinternal_status := ('
                                    + format_code(current_node.condition, node_name, variables, local_variables, True, False, None)
                                    + ') ? success : failure;' + os.linesep
                                ))


def create_action(current_node, node_name, parent_name, variables, local_variables, delayed_statements):
    statuses = {result.status for result in itertools.chain([current_node.return_statement.default_result], current_node.return_statement.case_results)}
    success = 'success' in statuses
    running = 'running' in statuses
    failure = 'failure' in statuses

    def handle_statements(statements, init_statement = False):
        for cur_statement in statements:
            if cur_statement.variable_statement is not None:
                statement = cur_statement.variable_statement
                format_variable(statement.variable, statement.mode == 'local', node_name, False, variables, local_variables, False, False, False, None)
                if init_statement:
                    new_stage = make_new_stage(statement, node_name, variables, local_variables, False, False, None)
                    variable_key = variable_reference(statement.variable.name, statement.mode == 'local', node_name, False)
                    # print(variables.keys())
                    variables[variable_key]['initial_value'] = new_stage
                else:
                    variable_key = variable_reference(statement.variable.name, statement.mode == 'local', node_name, False)
                    keep_stage_0 = variables[variable_key]['keep_stage_0']
                    non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
                    keep_stage_0 = keep_stage_0 or (not non_determinism)
                    if keep_stage_0 or len(variables[variable_key]['next_value']) > 0:
                        variables[variable_key]['next_value'].append((node_name,
                                                                      non_determinism,
                                                                      make_new_stage(statement, node_name, variables, local_variables, True, False, None)))
                    else:
                        variables[variable_key]['next_value'].append((node_name,
                                                                      non_determinism,
                                                                      make_new_stage(statement, node_name, variables, local_variables, True, True, variable_key)))
                    variables[variable_key]['keep_stage_0'] = keep_stage_0
            elif cur_statement.read_statement is not None:
                statement = cur_statement.read_statement
                if init_statement:
                    if statement.condition is None:
                        condition_variable_key = variable_reference(statement.condition_variable.name, True, node_name, False)
                        if condition_variable_key not in variables:
                            format_variable(statement.condition_variable, True, node_name, False, variables, local_variables, False, False, None)
                        new_stage = [('TRUE', '{TRUE, FALSE}')]
                        variables[condition_variable_key]['initial_value'] = new_stage
                    condition = (
                        format_code(statement.condition, node_name, variables, local_variables, False, False, None) if statement.condition is not None else (
                            format_variable(statement.condition_variable, True, node_name, False, variables, local_variables, False, False, None)
                            )
                        )
                    for variable_statement in statement.variable_statements:
                        variable_key = variable_reference(variable_statement.variable.name, variable_statement.mode == 'local', node_name, False)
                        if variable_key not in variables:
                            format_variable(variable_statement.variable, variable_statement.mode == 'local',
                                            node_name, False, variables, local_variables, False, False, None)
                        variable = variables[variable_key]
                        variable['intial_value'] = ([('!(' + condition + ')',
                                                      variable['custom_value_range'] if variable['custom_value_range'] is not None else (
                                                          str(variable['min_val']) + '..' + str(variable['max_val'])
                                                      )
                                                      )]
                                                    +
                                                    make_new_stage(variable_statement, node_name, variables, local_variables, False, False, None)
                                                    )
                else:
                    if statement.condition is None:
                        condition_variable_key = variable_reference(statement.condition_variable.name, True, node_name, False)
                        if condition_variable_key not in variables:
                            format_variable(statement.condition_variable, True, node_name, False, variables, local_variables, False, False, None)
                        new_stage = [('TRUE', '{TRUE, FALSE}')]
                        variables[condition_variable_key]['next_value'].append((node_name, True, new_stage))
                    condition = (
                        format_code(statement.condition, node_name, variables, local_variables, True, False, None) if statement.condition is not None else (
                            format_variable(statement.condition_variable, True, node_name, False, variables, local_variables, True, False, None)
                            )
                        )
                    for variable_statement in statement.variable_statements:
                        variable_key = variable_reference(variable_statement.variable.name, variable_statement.mode == 'local', node_name, False)
                        if variable_key not in variables:
                            format_variable(variable_statement.variable, variable_statement.mode == 'local',
                                            node_name, False, variables, local_variables, False, False, None)
                        variable = variables[variable_key]
                        keep_stage_0 = variable['keep_stage_0']
                        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([variable_statement.default_result], variable_statement.case_results)])
                        keep_stage_0 = keep_stage_0 or (not non_determinism)
                        variable['next_value'].append((node_name,
                                                       non_determinism,
                                                       (
                                                           [('!(' + condition + ')',
                                                             format_variable(variable_statement.variable, variable_statement.mode == 'local',
                                                                             node_name, False, variables, local_variables, True,
                                                                             (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
                                                                             (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key))
                                                             )]
                                                           +
                                                           make_new_stage(variable_statement, node_name, variables, local_variables, True,
                                                                          (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
                                                                          (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key)))))
                        variable['keep_stage_0'] = keep_stage_0
            elif cur_statement.write_statement is not None:
                statements = cur_statement.write_statement.update
                for statement in statements:
                    if statement.instant:
                        variable_key = variable_reference(statement.variable.name, False, '', True)
                        variable = variables[variable_key]
                        keep_stage_0 = variable['keep_stage_0']
                        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
                        keep_stage_0 = keep_stage_0 or (not non_determinism)
                        variable['next_value'].append((node_name,
                                                       non_determinism,
                                                       make_new_stage(statement, node_name, variables, local_variables, True,
                                                                      (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
                                                                      (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key))))
                        variable['keep_stage_0'] = keep_stage_0
                    else:
                        delayed_statements.append((node_name, statement))
        return

    handle_statements(current_node.init_statements, True)
    handle_statements(current_node.pre_update_statements, False)

    variable_list = []
    if not (len(current_node.return_statement.case_results) == 0 or len(statuses) == 1):
        for case_result in current_node.return_statement.case_results:
            variable_list += find_used_variables(case_result.condition,
                                                 node_name, variables, local_variables,
                                                 True)
    variable_set = [*set(variable_list)]  # remove duplicates, but force a specific order. (order can be arbitrary, just needs to be the same each time from here on out)

    node = create_node_template(node_name, parent_name, 'leaf', 'action',
                                success, running, failure,
                                additional_arguments = variable_set,
                                internal_status_module_name = None if (len(current_node.return_statement.case_results) == 0
                                                                       or len(statuses) == 1) else
                                (
                                    node_name + '_module'
                                ),
                                internal_status_module_code = None if (len(current_node.return_statement.case_results) == 0
                                                                       or len(statuses) == 1) else
                                (
                                    'MODULE ' + node_name + '_module(' + ', '.join(variable_set) + ')' + os.linesep
                                    + '\tCONSTANTS' + os.linesep
                                    + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                    + '\tDEFINE' + os.linesep
                                    + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                    + '\t\tinternal_status := ' + os.linesep
                                    + '\t\t\tcase' + os.linesep
                                    + ('').join([('\t\t\t\t'
                                                  + format_code(case_result.condition, node_name, variables, local_variables, True, False, None)
                                                  + ' : '
                                                  + case_result.status
                                                  + ';' + os.linesep)
                                                 for case_result in current_node.return_statement.case_results])
                                    + '\t\t\t\tTRUE : ' + current_node.return_statement.default_result.status + ';' + os.linesep
                                    + '\t\t\tesac;' + os.linesep
                                ))

    handle_statements(current_node.post_update_statements, False)
    return node


CREATE_NODE = {
    'sequence' : create_sequence_selector,
    'selector' : create_sequence_selector,
    'parallel' : create_parallel,
    'X_is_Y' : create_X_is_Y,
    'inverter' : create_inverter,
    'check' : create_check,
    'check_environment' : create_check,
    'action' : create_action
}


def walk_tree(model, variables, local_variables):
    nodes = {}
    delayed_statements = []
    walk_tree_recursive(model.root, None, nodes, set(), variables, local_variables, delayed_statements)
    return (nodes, delayed_statements)


def walk_tree_recursive(current_node, parent_name, nodes, node_names, variables, local_variables, delayed_statements):
    while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
        if hasattr(current_node, 'leaf'):
            current_node = current_node.leaf
        else:
            # print(dir(current_node))
            current_node = current_node.sub_root
    # the above deals with sub_trees and leaf nodes, ensuring that the current_node variable has the next actual node at this point
    # next, we get the name of this node, and correct for duplication

    node_name = create_node_name(current_node.name.replace(' ', ''), node_names)
    node_names.add(node_name)

    if parent_name is not None:
        nodes[parent_name]['children'].append(node_name)
        # update parent's list of children

    nodes[node_name] = CREATE_NODE[current_node.node_type](current_node, node_name, parent_name, variables, local_variables, delayed_statements)

    if nodes[node_name]['category'] == 'leaf':
        pass
    elif nodes[node_name]['category'] == 'decorator':
        walk_tree_recursive(
            current_node.child,
            node_name,
            nodes, node_names,
            variables, local_variables,
            delayed_statements
            )
    else:
        for child in current_node.children:
            walk_tree_recursive(
                child,
                node_name,
                nodes, node_names,
                variables, local_variables,
                delayed_statements
            )

    return


def handle_specifications(specifications, variables, local_variables):
    return [
        (
            specification.spec_type
            + ' '
            + format_code(specification.code_statement, '', variables, local_variables, True, False, None)
            + ';'
        )
        for specification in specifications
        ]


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    (variables, local_variables) = get_variables(model, args.keep_stage_0)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, None, variables, local_variables, True, False, None)
    specifications = handle_specifications(model.specifications, variables, local_variables)  # this included here to ensure we don't erase stage 0 used by specifications.
    (nodes, delayed_statements) = walk_tree(model, variables, local_variables)
    complete_environment_variables(model, variables, local_variables, delayed_statements)
    specifications = handle_specifications(model.specifications, variables, local_variables)

    if args.output_file is None:
        printer = pprint.PrettyPrinter(indent = 4)
        printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
    else:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, stream = f)
            printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
    return


if __name__ == '__main__':
    main()
