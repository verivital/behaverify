import textx
import argparse
import pprint
import os
import sys
import itertools
import copy


def get_variables(model):
    variables = {variable.name : {
        'variable_name' : variable.name,
        'mode' : variable.model_as,
        'custom_value_range' : (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
        'min_value' : 0 if variable.domain.min_val is None else variable.domain.min_val,
        'max_value' : 1 if variable.domain.min_val is None else variable.domain.max_val,
        'init_value' : None,
        # 'always_exist' : True,
        # 'init_exist' : True,
        # 'auto_change' : False,
        'next_value' : [],
        'environment_update' : None
        # 'next_exist' : {},
        # 'use_separate_stages' : True,
        # 'read_by' : [],
        # 'read_by_init' : []
    } for variable in itertools.chain(model.variables, model.environment_variables)}
    local_variables = {variable.name : {
        'variable_name' : variable.name,
        'mode' : variable.model_as,
        'custom_value_range' : (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
        'min_value' : 0 if variable.domain.min_val is None else variable.domain.min_val,
        'max_value' : 1 if variable.domain.min_val is None else variable.domain.max_val,
        'init_value' : None,
        # 'always_exist' : True,
        # 'init_exist' : True,
        # 'auto_change' : False,
        'next_value' : [],
        'environment_update' : None
        # 'next_exist' : {},
        # 'use_separate_stages' : True,
        # 'read_by' : [],
        # 'read_by_init' : []
    } for variable in model.local_variables}
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


def create_environment_variables(model, variables):
    inits = {statement.variable.name : make_new_stage(statement, None, variables, {}, False, False, False) for statement in model.initial}
    updates = {statement.variable.name : make_new_stage(statement, None, variables, {}, True, False, True) for statement in model.update}

    return {variable.name : {
        'variable_name' : variable.name,
        'mode' : variable.model_as,
        'custom_value_range' : (None if variable.domain.min_val is not None else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(variable.domain.enums) + '}'))),
        'min_value' : 0 if variable.domain.min_val is None else variable.domain.min_val,
        'max_value' : 1 if variable.domain.min_val is None else variable.domain.max_val,
        'init_value' : (None if variable.name not in inits else inits[variable.name]),
        # 'always_exist' : True,
        # 'init_exist' : True,
        # 'auto_change' : False,
        'next_value' : [],
        'environment_update' : (None if variable.name not in inits else updates[variable.name]),
        # 'next_exist' : {},
        # 'use_separate_stages' : True,
        # 'read_by' : [],
        # 'read_by_init' : []
    } for variable in model.environment_variables}


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
    variables[local_variable_name]['variable_name'] = local_variable_name
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
            (format_variable(code.variable, code.is_local, node_name, variables, local_variables, use_stages, call_blackboard, use_next)) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if code.code_statement is not None else (
                    (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 0 else (
                        (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ', ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 1 else (
                            format_code(code.function_call.value1, node_name, variables, local_variables, use_stages, call_blackboard, use_next) + ' ' + FUNCTION_FORMAT[code.function_call.function_name][0] + ' ' + format_code(code.function_call.value2, node_name, variables, local_variables, use_stages, call_blackboard, use_next)
                        )
                    )
                )
            )
        )
    )


def walk_tree(model, variables, local_variables):
    nodes = {}
    walk_tree_recursive(model.root, None, nodes, {}, variables, local_variables)
    return nodes


def walk_tree_recursive(current_node, parent_name, nodes, node_names, variables, local_variables):
    if not hasattr(current_node, 'name'):
        current_node = current_node.leaf
    # next, we get the name of this node, and correct for duplication
    node_name = current_node.name.replace(' ', '')
    if node_name in node_names:
        node_names[node_name] = node_names[node_name] + 1
        node_name = node_name + str(node_names[node_name])
    else:
        node_names[node_name] = 0

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
        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : None,
            'internal_status_module_name' : None,
            'internal_status_module_code' : None
        }
    elif current_node.node_type == 'selector':
        if current_node.memory:
            memory_string = 'selector_with_memory'
        else:
            memory_string = 'selector_without_memory'
        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'composite',
            'type' : memory_string,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : None,
            'internal_status_module_name' : None,
            'internal_status_module_code' : None
        }
    elif current_node.node_type == 'parallel':
        cur_type = 'parallel'
        if current_node.memory:
            cur_type += '_' + current_node.parallel_policy + '_with_memory'
        else:
            cur_type += '_success_on_all_without_memory'
        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'composite',
            'type' : cur_type,
            'return_arguments' : {
                'success' : True,
                'running' : True,
                'failure' : True
            },
            'additional_arguments' : None,
            'internal_status_module_name' : None,
            'internal_status_module_code' : None
        }

    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            sys.exit()

        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'decorator',
            'type' : 'X_is_Y',
            'return_arguments' : {
                'success' : not current_node.x == 'success',
                'running' : not current_node.x == 'running',
                'failure' : not current_node.x == 'failure'
            },
            'additional_arguments' : [current_node.x, current_node.y],
            'internal_status_module_name' : None,
            'internal_status_module_code' : None
        }

    elif current_node.node_type == 'check':
        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'leaf',
            'type' : 'check',
            'return_arguments' : {
                'success' : True,
                'running' : False,
                'failure' : True
            },
            'internal_status_module_name' : None if current_node.condition is None else node_name + '_module',
            'internal_status_module_code' : None if current_node.condition is None else (
                'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                + '\tCONSTANTS' + os.linesep
                + '\t\tsuccess, failure, running, invalid;' + os.linesep
                + '\tDEFINE' + os.linesep
                + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                + '\t\tinternal_status := ('
                + format_code(current_node.condition, node_name, variables, local_variables, True, True, False)
                + ') ? success : failure;' + os.linesep
                )
        }

    elif current_node.node_type == 'action':
        success = current_node.return_statement.default_result.can_success
        running = current_node.return_statement.default_result.can_running
        failure = current_node.return_statement.default_result.can_failure
        for result in current_node.return_statement.case_results:
            success = success or result.can_success
            running = running or result.can_running
            failure = failure or result.can_failure
        if not (success or running or failure):
            print('no valid return type for action node!' + node_name)
            sys.exit()

        def handle_statements(statements, init_statement = False):
            for statement in statements:
                new_stage = make_new_stage(statement, node_name, variables, local_variables, not (init_statement), False, True)
                variable_name = format_variable(statement.variable, statement.is_local, node_name, variables, local_variables, False, False, False)
                if init_statement:
                    variables[variable_name]['init_value'] = new_stage
                else:
                    variables[variable_name]['next_value'].append((node_name, new_stage))
            return

        handle_statements(current_node.init_statements, True)
        handle_statements(current_node.pre_update_statements, False)

        nodes[node_name] = {
            'name' : node_name,
            'parent' : parent_name,
            'children' : [],
            'category' : 'leaf',
            'type' : 'action',
            'return_arguments' : {
                'success' : success,
                'running' : running,
                'failure' : failure
            },
            'internal_status_module_name' : None if (len(current_node.return_statement.case_results) == 0 or [success, running, failure].count(True) == 1) else node_name + '_module',
            'internal_status_module_code' : None if (len(current_node.return_statement.case_results) == 0 or [success, running, failure].count(True) == 1) else (
                'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                + '\tCONSTANTS' + os.linesep
                + '\t\tsuccess, failure, running, invalid;' + os.linesep
                + '\tDEFINE' + os.linesep
                + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                + '\tVAR' + os.linesep
                + '\t\tinternal_status : {' + ', '.join([status for (status, possible) in [('success', success), ('running', running), ('failure', failure)] if possible]) + '};' + os.linesep
                + '\tASSIGN' + os.linesep
                + '\t\tinit(internal_status) := ' + [status for (status, possible) in [('success', success), ('running', running), ('failure', failure)] if possible][0] + ';' + os.linesep
                + '\t\tnext(internal_status) := ' + os.linesep
                + '\t\t\tcase' + os.linesep
                + ('').join([('\t\t\t\t'
                              + format_code(case_result.condition, node_name, variables, local_variables, True, True, True)
                              + ' : '
                              + ('{' if [case_result.can_success, case_result.can_running, case_result.can_failure].count(True) > 1 else '')
                              + ', '.join([status for (status, possible) in [('success', case_result.can_success), ('running', case_result.can_running), ('failure', case_result.can_failure)] if possible])
                              + ('}' if [case_result.can_success, case_result.can_running, case_result.can_failure].count(True) > 1 else '')
                              + ';' + os.linesep)
                             for case_result in current_node.return_statement.case_results])
                + '\t\t\t\tTRUE : '
                + ('{' if [current_node.return_statement.default_result.can_success,
                           current_node.return_statement.default_result.can_running,
                           current_node.return_statement.default_result.can_failure].count(True) > 1 else '')
                + ', '.join([status for (status, possible) in [('success', current_node.return_statement.default_result.can_success),
                                                               ('running', current_node.return_statement.default_result.can_running),
                                                               ('failure', current_node.return_statement.default_result.can_failure)] if possible])
                + ('}' if [current_node.return_statement.default_result.can_success,
                           current_node.return_statement.default_result.can_running,
                           current_node.return_statement.default_result.can_failure].count(True) > 1 else '')
                + ';' + os.linesep
                + '\t\t\tesac;' + os.linesep
            )
        }
        handle_statements(current_node.post_update_statements, False)

    if nodes[node_name]['category'] == 'leaf':
        pass
    elif nodes[node_name]['category'] == 'decorator':
        # currently there are no decorators. not really.
        walk_tree_recursive(
            current_node.child,
            node_name,
            nodes, node_names,
            variables, local_variables
            )
    else:
        for child in current_node.children:
            walk_tree_recursive(
                child,
                node_name,
                nodes, node_names,
                variables, local_variables
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
    nodes = walk_tree(model, variables, local_variables)
    variables.update(create_environment_variables(model, variables))

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
