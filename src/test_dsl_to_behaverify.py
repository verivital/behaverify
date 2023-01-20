import textx
import argparse
import pprint
import os
import sys
import itertools
import copy

from behaverify_common import create_node_name, create_node_template, create_variable_template_keep_stage as create_variable_template


def get_variables(model):
    '''
    this constructs and returns variables and local variables.
    variables are constructed based on variables and environment_variables
    -- arguments
    @ model := a model. one created using behaverify.tx as the metamodel (probably)
    -- return
    @ variables := a dictionary from variable_name (string) to variable informaion
    @ local_variables := a dictionary from variable_name (string) to variable informaion
    -- side effects
    none. purely functional.
    '''
    variables = {variable_reference(variable.name, False, '', False) :
                 create_variable_template(variable.name, variable.model_as,
                                          (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
                                          0 if variable.domain.min_val is None else variable.domain.min_val,
                                          1 if variable.domain.min_val is None else variable.domain.max_val,
                                          None, [], 'var_', False
                                          )
                 for variable in model.variables}
    env_variables = {variable_reference(variable.name, False, '', True) :
                     create_variable_template(variable.name, variable.model_as,
                                              (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
                                              0 if variable.domain.min_val is None else variable.domain.min_val,
                                              1 if variable.domain.min_val is None else variable.domain.max_val,
                                              None, [], 'env_', False
                                              )
                     for variable in model.environment_variables}
    variables.update(env_variables)
    local_variables = {variable.name :
                       create_variable_template(variable.name, variable.model_as,
                                                (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
                                                0 if variable.domain.min_val is None else variable.domain.min_val,
                                                1 if variable.domain.min_val is None else variable.domain.max_val,
                                                None, [], '', False
                                                )
                       for variable in model.local_variables}
    return (variables, local_variables)


def make_new_stage(statement, node_name, variables, local_variables, use_stages, use_next, not_next):
    '''
    this creates a new_stage and returns it.
    the stage consists of (conditions, results) pairs in order.
    if a condition is met, that value is used.
    the last condition is always TRUE, ensuring at least one condition will be met.
    -- @ arguments
    statement := a code statement (see grammar defined in behaverify.tx)
     -> the statement contains the information we need.
    node_name := the name of the node to use string usually, can be None.
     -> this is used by methods called by make_new_stage.
    variables := a dictionary of variables_names to variable_info
    local_variables := a dictionary of variable_names to variable_info
    use_stages := a boolean.
     -> if true, variables will be formattted to use their current stage.
     -> if false, variables will just use their name
    call_blackboard := a boolean
     -> WARNING. DEPRICATED. should always be false.
     -> in older versions, blackboard was seperate.
     -> this necessitated some things calling the blackboard. this is no longer accurate.
    use_next := a boolean
     -> WARNING. DEPRICATED. should always be false
     -> in older versions it was sometimes useful to call next value instead of current
     -> that was mostly because i overthought it and made a bad and complicated encoding.
    -- side effects
    none directly. however, this method calls format_code which calls format_variable
    format_variable has side effects. can modify variables.
    '''
    return ([(format_code(case_result.condition, node_name, variables, local_variables, use_stages, use_next, not_next)
              ,
              (
                  ('{' if len(case_result.values) > 1 else '')
                  + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next)
                               for value in case_result.values])
                  + ('}' if len(case_result.values) > 1 else '')
              )
              )
             for case_result in statement.case_results
             ]
            +
            [('TRUE'
              ,
              (
                  ('{' if len(statement.default_result.values) > 1 else '')
                  + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, use_next, not_next)
                               for value in statement.default_result.values])
                  + ('}' if len(statement.default_result.values) > 1 else '')
              )
              )
             ]
            )


def variable_reference(base_name, is_local, node_name, is_env):
    return (
        ('env_' if is_env else ((node_name + '_DOT_') if is_local else ('')))
        + base_name)


def complete_environment_variables(model, variables, local_variables, delayed_statements):
    '''
    completes the environment variables.
    --arguments
    @ model :=
    '''
    for (node_name, statement) in delayed_statements:
        new_stage = make_new_stage(statement, node_name, variables, local_variables, True, False, None)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((node_name, non_determinism, new_stage))

    for statement in model.initial:
        new_stage = make_new_stage(statement, None, variables, {}, False, False, False)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        variables[variable_name]['initial_value'] = new_stage

    for statement in model.update:
        new_stage = make_new_stage(statement, None, variables, {}, True, False, False)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((None, non_determinism, new_stage))

    return


FUNCTION_FORMAT = {
    'abs' : ('abs', 0),
    'max' : ('max', 1),
    'min' : ('min', 1),
    'sin' : ('sin', 0),
    'cos' : ('cos', 0),
    'tan' : ('tan', 0),
    'ln' : ('ln', 0),
    'not' : ('!', 0),
    'and' : ('&', 2),
    'or' : ('|', 2),
    'xor' : ('xor', 2),
    'xnor' : ('xnor', 2),
    'implies' : ('=>', 2),
    'equivalent' : ('<=>', 2),
    'equal' : ('=', 2),
    'not_equal' : ('!=', 2),
    'less_than' : ('<', 2),
    'greater_than' : ('>', 2),
    'less_than_or_equal' : ('<=', 2),
    'greater_than_or_equal' : ('>=', 2),
    'negative' : ('-', 0),
    'addition' : ('+', 2),
    'subtraction' : ('-', 2),
    'multiplication' : ('*', 2),
    'division' : ('/', 2),
    'mod' : ('mod', 2)
}


def compute_stage(variable_name, variables, use_stages):
    return (('_stage_' + str(len(variables[variable_name]['next_value']))) if (use_stages and len(variables[variable_name]['next_value']) > 0) else (''))


def add_local_variable(variables, local_variables, variable_name, variable_key):
    variables[variable_key] = copy.deepcopy(local_variables[variable_name])
    variables[variable_key]['name'] = variable_key
    return


def format_variable(variable, is_local, node_name, is_env, variables, local_variables, use_stages, use_next, not_next):
    variable_key = variable_reference(variable.name, is_local, node_name, is_env)
    if variable_key not in variables:
        add_local_variable(variables, local_variables, variable.name, variable_key)
    variable = variables[variable_key]
    if use_stages and len(variable['next_value']) == 0:
        variable['keep_stage_0'] = True
    if use_next and variable_key == not_next:
        return 'LINK_TO_PREVIOUS_FINAL_' + variable['prefix'] + variable['name']
    return (('' if not use_next else 'next(')
            + variable['prefix']
            + variable['name']
            + compute_stage(variable_key, variables, use_stages)
            + ('' if not use_next else ')'))


def format_function_0(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, use_next, not_next) + ')')


def format_function_1(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        FUNCTION_FORMAT[code.function_call.function_name][0] + '('
        + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, use_next, not_next)
        + ', ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, use_next, not_next)
        + ')')


def format_function_2(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return ('('
            + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, use_next, not_next)
            + ' ' + FUNCTION_FORMAT[code.function_call.function_name][0]
            + ' ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, use_next, not_next)
            + ')')


def format_function(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    code_num = FUNCTION_FORMAT[code.function_call.function_name][1]
    return (
        format_function_0(code, node_name, variables, local_variables, use_stages, use_next, not_next) if code_num == 0 else (
            format_function_1(code, node_name, variables, local_variables, use_stages, use_next, not_next) if code_num == 1 else (
                format_function_2(code, node_name, variables, local_variables, use_stages, use_next, not_next)
            )
        )
    )


def format_code(code, node_name, variables, local_variables, use_stages, use_next, not_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, (code.is_local if hasattr(code, 'is_local') else False), node_name, (code.is_env if hasattr(code, 'is_env') else False), variables, local_variables, use_stages, use_next, not_next)) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name, variables, local_variables, use_stages, use_next, not_next) + ')') if code.code_statement is not None else (
                    format_function(code, node_name, variables, local_variables, use_stages, use_next, not_next)
                )
            )
        )
    )


def find_used_variables(code, node_name, variables, local_variables, use_stages):
    return (
        [] if code.constant is not None else (
            [format_variable(code.variable, (code.is_local if hasattr(code, 'is_local') else False), node_name, (code.is_env if hasattr(code, 'is_env') else False), variables, local_variables, use_stages, False, None)] if code.variable is not None else (
                find_used_variables(code.code_statement, node_name, variables, local_variables, use_stages) if code.code_statement is not None else (
                    find_used_variables(code.function_call.value1, node_name, variables, local_variables, use_stages)
                    +
                    (find_used_variables(code.function_call.value2, node_name, variables, local_variables, use_stages) if FUNCTION_FORMAT[code.function_call.function_name][1] != 0 else [])
                    )
                )
            )
        )


def walk_tree(model, variables, local_variables):
    nodes = {}
    delayed_statements = []
    walk_tree_recursive(model.root, None, nodes, set(), variables, local_variables, delayed_statements)
    return (nodes, delayed_statements)


def walk_tree_recursive(current_node, parent_name, nodes, node_names, variables, local_variables, delayed_statements):
    if not hasattr(current_node, 'name'):
        current_node = current_node.leaf
    # next, we get the name of this node, and correct for duplication

    node_name = create_node_name(current_node.name.replace(' ', ''), node_names)
    node_names.add(node_name)

    if parent_name is not None:
        nodes[parent_name]['children'].append(node_name)
        # update parent's list of children

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    if current_node.node_type == 'sequence':
        if current_node.memory:
            memory_string = 'sequence_with_memory'
        else:
            memory_string = 'sequence_without_memory'
        nodes[node_name] = create_node_template(node_name, parent_name, 'composite', memory_string,
                                                True, True, True)
    elif current_node.node_type == 'selector':
        if current_node.memory:
            memory_string = 'selector_with_memory'
        else:
            memory_string = 'selector_without_memory'
        nodes[node_name] = create_node_template(node_name, parent_name, 'composite', memory_string,
                                                True, True, True)
    elif current_node.node_type == 'parallel':
        cur_type = 'parallel'
        if current_node.memory:
            cur_type += '_' + current_node.parallel_policy + '_with_memory'
        else:
            cur_type += '_success_on_all_without_memory'
        nodes[node_name] = create_node_template(node_name, parent_name, 'composite', cur_type,
                                                True, True, True)

    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            sys.exit()

        nodes[node_name] = create_node_template(node_name, parent_name, 'decorator', 'X_is_Y',
                                                True, True, True,
                                                additional_arguments = [current_node.x, current_node.y])

    elif current_node.node_type == 'check':

        variable_list = (
            find_used_variables(current_node.condition,
                                node_name, variables, local_variables,
                                True)
            if current_node.condition is not None else [])

        variable_set = [*set(variable_list)]  # remove duplicates, but force a specific order.

        nodes[node_name] = create_node_template(node_name, parent_name, 'leaf', 'check',
                                                True, False, True,
                                                additional_arguments = variable_set,
                                                internal_status_module_name = None if current_node.condition is None else node_name + '_module',
                                                internal_status_module_code = None if current_node.condition is None else (
                                                    'MODULE ' + node_name + '_module(' + ', '.join(variable_set) + ')' + os.linesep
                                                    + '\tCONSTANTS' + os.linesep
                                                    + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                    + '\tDEFINE' + os.linesep
                                                    + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                    + '\t\tinternal_status := ('
                                                    + format_code(current_node.condition, node_name, variables, local_variables, True, False, None)
                                                    + ') ? success : failure;' + os.linesep
                                                ))

    elif current_node.node_type == 'action':
        statuses = {result.status for result in itertools.chain([current_node.return_statement.default_result], current_node.return_statement.case_results)}
        success = 'success' in statuses
        running = 'running' in statuses
        failure = 'failure' in statuses
        # print(node_name + ' : ' + str(statuses))

        def handle_statements(statements, init_statement = False):
            for cur_statement in statements:
                if init_statement or cur_statement.variable_statement is not None:
                    if init_statement:
                        statement = cur_statement
                        new_stage = make_new_stage(statement, node_name, variables, local_variables, False, False, None)
                        variable_key = variable_reference(statement.variable.name, statement.is_local, node_name, False)
                        variables[variable_key]['initial_value'] = new_stage
                    else:
                        statement = cur_statement.variable_statement
                        variable_key = variable_reference(statement.variable.name, statement.is_local, node_name, False)
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
                    for variable_environment_pair in statement.variable_environment_pairs:
                        variable_key = variable_reference(variable_environment_pair.variable.name, variable_environment_pair.is_local, node_name, False)
                        if variable_key not in variables:
                            format_variable(variable_environment_pair.variable, variable_environment_pair.is_local,
                                            node_name, False, variables, local_variables, False, False, None)
                        variable = variables[variable_key]
                        variable['keep_stage_0'] = variable['keep_stage_0'] if len(variable['next_value']) > 0 else True
                        variable['next_value'].append((node_name,
                                                       False,
                                                       [(condition,
                                                         format_variable(variable_environment_pair.environment_variable,
                                                                         False, node_name, True, variables, local_variables,
                                                                         True, False, None)
                                                         ),
                                                        ('TRUE',
                                                         format_variable(variable_environment_pair.variable, variable_environment_pair.is_local,
                                                                         node_name, False, variables, local_variables, True, False, None)
                                                         )
                                                        ]
                                                       ))
                elif cur_statement.write_statement is not None:
                    statements = cur_statement.write_statement.update
                    for statement in statements:
                        if statement.instant:
                            variable_key = variable_reference(statement.variable.name, False, '', True)
                            variable = variables[variable_key]
                            keep_stage_0 = variable['keep_stage_0']
                            non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
                            keep_stage_0 = keep_stage_0 or (not non_determinism)
                            if keep_stage_0 or len(variable['next_value']) > 0:
                                variable['next_value'].append((node_name,
                                                               non_determinism,
                                                               make_new_stage(statement, node_name, variables, local_variables, True, False, None)))
                            else:
                                variable['next_value'].append((node_name,
                                                               non_determinism,
                                                               make_new_stage(statement, node_name, variables, local_variables, True, True, variable_key)))
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

        nodes[node_name] = create_node_template(node_name, parent_name, 'leaf', 'action',
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


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    (variables, local_variables) = get_variables(model)
    (nodes, delayed_statements) = walk_tree(model, variables, local_variables)
    complete_environment_variables(model, variables, local_variables, delayed_statements)

    if args.output_file is None:
        printer = pprint.PrettyPrinter(indent = 4)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    return


if __name__ == '__main__':
    main()
