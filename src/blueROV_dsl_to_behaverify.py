import textx
import argparse
import pprint
import os
import sys
import itertools
import copy

from behaverify_common import create_node_name, create_node_template


def get_variables(model):
    variables = {variable.name : {
        'name' : variable.name,
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
    } for variable in model.variables}
    return variables


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
    return (('' if (len(variables[variable.name]['next_value']) == 0 or not use_next) else 'next(')
            + (('blackboard.') if call_blackboard else (''))
            + variable.name
            + compute_stage(variable.name, variables, use_stages)
            + ('' if (len(variables[variable.name]['next_value']) == 0 or not use_next) else ')'))


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


def walk_tree(metamodel, model, variables):
    nodes = {}
    walk_tree_recursive(metamodel, model.root, None, nodes, {}, variables)
    return nodes


def walk_tree_recursive(metamodel, current_node, parent_name, nodes, node_names, variables):
    if hasattr(current_node, 'name'):
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
    if textx.textx_isinstance(current_node, metamodel['SeqBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'composite', 'sequence_with_memory',
                                                True, True, True)
    elif textx.textx_isinstance(current_node, metamodel['SelBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'composite', 'selector_without_memory',
                                                True, True, True)
    elif textx.textx_isinstance(current_node, metamodel['ParBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'composite', 'parallel_success_on_all_without_memory',
                                                True, True, True)

    elif textx.textx_isinstance(current_node, metamodel['SIFBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'decorator', 'X_is_Y',
                                                False, True, True,
                                                additional_arguments = ['success', 'failure'])

        # ok, we've added the decorator. now we add in the selector node
        parent_name = node_name
        # selector is going to use the same name as the decorator.
        # next, we get the name of this node, and correct for duplication
        node_name = create_node_name(current_node.name.replace(' ', ''), node_names)
        node_names.add(node_name)

        if parent_name is not None:
            nodes[parent_name]['children'].append(node_name)
            # update parent's list of children
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'composite', 'selector_without_memory',
                                                True, True, True)
        # selector added
        selector_name = node_name  # store this. we will restore it after adding the checks in
        decorator_name = parent_name

        parent_name = node_name
        # ok, now we add all the checks, which are here for some reason.
        for check in current_node.checks:
            node_name = create_node_name(check.name.replace(' ', ''), node_names)
            node_names.add(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'check',
                                                    True, False, True,
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ('
                                                        + 'blackboard.' + check.bbvar.name + ' = ' + check.default
                                                        + ') ? success : failure;' + os.linesep
                                                    ))
        # all checks added in, so now we restore back up to the selector
        node_name = selector_name
        parent_name = decorator_name

    elif textx.textx_isinstance(current_node, metamodel['CheckBTNode']):
        for check in current_node.check:
            node_name = create_node_name(check.name.replace(' ', ''), node_names)
            node_names.add(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'check',
                                                    True, False, True,
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ('
                                                        + 'blackboard.' + check.bbvar.name + ' = ' + check.default
                                                        + ') ? success : failure;' + os.linesep
                                                    ))

    elif textx.textx_isinstance(current_node, metamodel['TaskBTNode']):
        for task in current_node.task:
            node_name = create_node_name(task.name.replace(' ', ''), node_names)
            node_names.add(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'check',
                                                    task.return_status == 'success', task.return_status == 'running', task.return_status == 'failure',
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ('
                                                        + 'blackboard.' + check.bbvar.name + ' = ' + check.default
                                                        + ') ? success : failure;' + os.linesep
                                                    ))

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
                new_stage = make_new_stage(statement, node_name, variables, not (init_statement), False, True)
                variable_name = format_variable(statement.variable, statement.is_local, node_name, variables, False, False, False)
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
            'return_possibilities' : {
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
            metamodel,
            current_node.child,
            node_name,
            nodes, node_names,
            variables
            )
    else:
        for child in current_node.children:
            walk_tree_recursive(
                metamodel,
                child,
                node_name,
                nodes, node_names,
                variables
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

    variables = get_variables(model)
    nodes = walk_tree(metamodel, model, variables)

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
