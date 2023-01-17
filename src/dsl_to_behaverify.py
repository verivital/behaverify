import textx
import argparse
import pprint
import os
import sys
import itertools
import copy

from behaverify_common import create_node_name, create_variable_template, create_node_template


def get_variables(model):
    variables = {variable.name :
                 create_variable_template(variable.name, variable.model_as,
                                          (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
                                          0 if variable.domain.min_val is None else variable.domain.min_val,
                                          1 if variable.domain.min_val is None else variable.domain.max_val,
                                          None, []
                                          )
                 for variable in itertools.chain(model.variables, model.environment_variables)}
    local_variables = {variable.name :
                       create_variable_template(variable.name, variable.model_as,
                                                (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
                                                0 if variable.domain.min_val is None else variable.domain.min_val,
                                                1 if variable.domain.min_val is None else variable.domain.max_val,
                                                None, []
                                                )
                       for variable in model.local_variables}
    return (variables, local_variables)


def make_new_stage(statement, node_name, variables, local_variables, use_stages, call_blackboard, use_next):
    new_stage = [(format_code(case_result.condition, node_name, variables, local_variables, use_stages, call_blackboard, use_next)
                  ,
                  (
                      ('{' if len(case_result.values) > 1 else '')
                      + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, call_blackboard, use_next)
                                   for value in case_result.values])
                      + ('}' if len(case_result.values) > 1 else '')
                  )
                  )
                 for case_result in statement.case_results
                 ]
    new_stage.append(
        ('TRUE'
         ,
         (
             ('{' if len(statement.default_result.values) > 1 else '')
             + ', '.join([format_code(value, node_name, variables, local_variables, use_stages, call_blackboard, use_next)
                          for value in statement.default_result.values])
             + ('}' if len(statement.default_result.values) > 1 else '')
         )
         )
    )
    return new_stage


def create_environment_variables(model, variables, local_variables, delayed_statements):
    for (node_name, statement) in delayed_statements:
        new_stage = make_new_stage(statement, node_name, variables, local_variables, True, False, False)
        variable_name = format_variable(statement.variable, False, node_name, variables, local_variables, False, False, False)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((node_name, non_determinism, new_stage))

    for statement in model.initial:
        new_stage = make_new_stage(statement, None, variables, {}, False, False, False)
        variable_name = format_variable(statement.variable, False, None, variables, {}, False, False, False)
        variables[variable_name]['initial_value'] = new_stage

    for statement in model.update:
        new_stage = make_new_stage(statement, None, variables, {}, True, False, False)
        variable_name = format_variable(statement.variable, False, None, variables, {}, False, False, False)
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


def add_local_variable(variables, local_variables, variable_name, local_variable_name):
    variables[local_variable_name] = copy.deepcopy(local_variables[variable_name])
    variables[local_variable_name]['name'] = local_variable_name
    return


def format_variable(variable, is_local, node_name, variables, local_variables, use_stages, call_blackboard, use_next):
    variable_name = ((node_name + '_DOT_') if is_local else ('')) + variable.name
    if variable_name not in variables:
        add_local_variable(variables, local_variables, variable.name, variable_name)
    return (('' if (len(variables[variable_name]['next_value']) == 0 or not use_next) else 'next(')
            + (('blackboard.') if call_blackboard else (''))
            + variable_name
            + compute_stage(variable_name, variables, use_stages)
            + ('' if (len(variables[variable_name]['next_value']) == 0 or not use_next) else ')'))


def format_code(code, node_name, variables, local_variables, use_stages, call_blackboard, use_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, (code.is_local if hasattr(code, 'is_local') else False), node_name, variables, local_variables, use_stages, call_blackboard, use_next)) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if code.code_statement is not None else (
                    (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 0 else (
                        (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ', ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 1 else (
                            '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ' ' + FUNCTION_FORMAT[code.function_call.function_name][0] + ' ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')'
                        )
                    )
                )
            )
        )
    )


def find_used_variables(code, node_name, variables, local_variables, use_stages, call_blackboard, use_next):
    return (
        [] if code.constant is not None else (
            [format_variable(code.variable, (code.is_local if hasattr(code, 'is_local') else False), node_name, variables, local_variables, use_stages, call_blackboard, use_next)] if code.variable is not None else (
                find_used_variables(code.code_statement, node_name, variables, local_variables, use_stages, call_blackboard, use_next) if code.code_statement is not None else (
                    find_used_variables(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next)
                    +
                    (find_used_variables(code.function_call.value2, node_name, variables, local_variables, use_stages, call_blackboard, use_next) if FUNCTION_FORMAT[code.function_call.function_name][1] != 0 else [])
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
                                True, False, False)
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
                                                    + format_code(current_node.condition, node_name, variables, local_variables, True, False, False)
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
                    else:
                        statement = cur_statement.variable_statement
                    new_stage = make_new_stage(statement, node_name, variables, local_variables, not (init_statement), False, False)
                    variable_name = format_variable(statement.variable, statement.is_local, node_name, variables, local_variables, False, False, False)
                    if init_statement:
                        variables[variable_name]['initial_value'] = new_stage
                        # print(variables[variable_name])
                    else:
                        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
                        variables[variable_name]['next_value'].append((node_name, non_determinism, new_stage))
                elif cur_statement.read_statement is not None:
                    statement = cur_statement.read_statement
                    if statement.condition is None:
                        condition_variable_name = format_variable(statement.condition_variable, True, node_name, variables, local_variables, False, False, False)
                        new_stage = [('TRUE', '{TRUE, FALSE}')]
                        variables[condition_variable_name]['next_value'].append((node_name, True, new_stage))
                    condition = (
                        format_code(statement.condition, node_name, variables, local_variables, True, False, False) if statement.condition is not None else (
                            format_variable(statement.condition_variable, True, node_name, variables, local_variables, True, False, False)
                            )
                        )
                    for variable_environment_pair in statement.variable_environment_pairs:
                        variable_name = format_variable(variable_environment_pair.variable, variable_environment_pair.is_local,
                                                        node_name, variables, local_variables, False, False, False)
                        variables[variable_name]['next_value'].append((node_name,
                                                                       False,
                                                                       [(condition,
                                                                         format_variable(variable_environment_pair.environment_variable,
                                                                                         False, node_name, variables, local_variables,
                                                                                         True, False, True)
                                                                         ),
                                                                        ('TRUE',
                                                                         format_variable(variable_environment_pair.variable, variable_environment_pair.is_local,
                                                                                         node_name, variables, local_variables, True, False, False)
                                                                         )
                                                                        ]
                                                                       ))
                elif cur_statement.write_statement is not None:
                    statements = cur_statement.write_statement.update
                    for statement in statements:
                        if statement.instant:
                            new_stage = make_new_stage(statement, node_name, variables, local_variables, not (init_statement), False, False)
                            variable_name = format_variable(statement.variable, False, node_name, variables, local_variables, False, False, False)
                            non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
                            variables[variable_name]['next_value'].append((node_name, non_determinism, new_stage))
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
                                                     True, False, False)
        variable_set = [*set(variable_list)]  # remove duplicates, but force a specific order.

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
                                                                  + format_code(case_result.condition, node_name, variables, local_variables, True, False, False)
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
    create_environment_variables(model, variables, local_variables, delayed_statements)

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
