import textx
import argparse
import pprint
import os
# import sys
# import itertools
# import copy

from behaverify_common import create_node_name, create_node_template


def get_variables(model):
    variables = {variable.name : {
        'name' : variable.name,
        'mode' : 'DEFINE' if (len(variable.model.enums) == 1) else 'VAR',
        'custom_value_range' : (None if variable.model.range_minimum is not None else ('{TRUE, FALSE}' if variable.model.is_bool is not None else ('{' + ', '.join(map(str, variable.model.enums)) + '}'))),
        'min_value' : 0 if variable.model.range_minimum is None else variable.model.range_minimum,
        'max_value' : 1 if variable.model.range_minimum is None else variable.model.range_maximum,
        'init_value' : [('TRUE', (str(variable.initial_value).upper() if isinstance(variable.initial_value, bool) else str(variable.initial_value)))],
        # 'always_exist' : True,
        # 'init_exist' : True,
        # 'auto_change' : False,
        'next_value' : [],
        'environment_update' : None
        # 'next_exist' : {},
        # 'use_separate_stages' : True,
        # 'read_by' : [],
        # 'read_by_init' : []
    } for variable in model.bbVariables if variable.model is not None}
    return variables


# def set_define(variables):
#     return {variable['name'] : {
#         'name' : variable['name'],
#         'mode' : 'DEFINE' if (len(variable['read_by']) == 0 and len(variable['next_value']) < 2) else variable['mode'],
#         'custom_value_range' : variable['custom_value_range'],
#         'min_value' : variable['min_value'],
#         'max_value' : variable['max_value'],
#         'init_value' : variable['next_value'][0][1] if (len(variable['read_by']) == 0 and len(variable['next_value']) == 1) else variable['init_value'],
#         'next_value' : [] if (len(variable['read_by']) == 0 and len(variable['next_value']) < 2) else variable['next_value'],
#         'environment_update' : variable['environment_update']
#     } for variable in variables.values()}


def make_new_stage(statement, node_name, variables, use_stages, call_blackboard, use_next):
    return (
        [(format_code(case_result.condition, node_name, variables, use_stages, call_blackboard, use_next),
          format_code(case_result.update_value, node_name, variables, use_stages, call_blackboard, use_next))
         for case_result in statement.updates]
        +
        [('TRUE',
          format_code(statement.default_update, node_name, variables, use_stages, call_blackboard, use_next))]
    )


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
    'mod' : ('mod', 2),
    'any' : (None, 3)
}


def compute_stage(variable_name, variables, use_stages):
    return (('_stage_' + str(len(variables[variable_name]['next_value']))) if (use_stages and len(variables[variable_name]['next_value']) > 0) else (''))


def format_variable(variable, node_name, variables, use_stages, call_blackboard, use_next):
    return (('' if (len(variables[variable.name]['next_value']) == 0 or not use_next) else 'next(')
            + (('blackboard.') if call_blackboard else (''))
            + variable.name
            + compute_stage(variable.name, variables, use_stages)
            + ('' if (len(variables[variable.name]['next_value']) == 0 or not use_next) else ')'))


def format_function(code, node_name, variables, use_stages, call_blackboard, use_next):
    return (
        (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 0 else (
            (FUNCTION_FORMAT[code.function_call.function_name][0] + '(' + format_code(code.function_call.value1, node_name, variables, use_stages, call_blackboard, use_next) + ', ' + format_code(code.function_call.value2, node_name, variables, use_stages, call_blackboard, use_next) + ')') if FUNCTION_FORMAT[code.function_call.function_name][1] == 1 else (
                format_code(code.function_call.value1, node_name, variables, use_stages, call_blackboard, use_next) + ' ' + FUNCTION_FORMAT[code.function_call.function_name][0] + ' ' + format_code(code.function_call.value2, node_name, variables, use_stages, call_blackboard, use_next) if FUNCTION_FORMAT[code.function_call.function_name][1] == 2 else (
                    '{'
                    +
                    ', '.join([format_code(value, node_name, variables, use_stages, call_blackboard, use_next) for value in code.function_call.values])
                    +
                    '}'
                )
            )
        )
    )


def format_code(code, node_name, variables, use_stages, call_blackboard, use_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, node_name, variables, use_stages, call_blackboard, use_next)) if code.variable is not None else (
                ('(' + format_code(code.CodeStatement, node_name, variables, use_stages, call_blackboard, use_next) + ')') if code.CodeStatement is not None else (
                    format_function(code, node_name, variables, use_stages, call_blackboard, use_next)
                )
            )
        )
    )


def walk_tree(metamodel, model, variables):
    nodes = {}
    walk_tree_recursive(metamodel, model.tree.btree, None, nodes, set(), variables)
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
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

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
                                                        + format_variable(check.bbvar, node_name, variables, True, True, False) + ' = ' + str(check.default).upper()
                                                        + ') ? success : failure;' + os.linesep
                                                    ))
        # all checks added in, so now we restore back up to the selector
        node_name = selector_name
        parent_name = decorator_name

    elif textx.textx_isinstance(current_node, metamodel['CheckBTNode']):
        for check in current_node.check:
            node_name = create_node_name(check.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

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
                                                        + format_variable(check.bbvar, node_name, variables, True, True, False) + ' = ' + check.default
                                                        + ') ? success : failure;' + os.linesep
                                                    ))

    elif textx.textx_isinstance(current_node, metamodel['TaskBTNode']):
        for task in current_node.task:
            node_name = create_node_name(task.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'action',
                                                    task.return_status == 'success', task.return_status == 'running', task.return_status == 'failure',
                                                    internal_status_module_name = None,
                                                    internal_status_module_code = None)

            for set_var in task.set_vars:
                variable_name = set_var.variable.name
                variables[variable_name]['next_value'].append((node_name, make_new_stage(set_var, node_name, variables, True, False, True)))

    elif textx.textx_isinstance(current_node, metamodel['MonBTNode']):
        for mon in current_node.mon:
            node_name = create_node_name(mon.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'read_action',
                                                    True, True, False,
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(blackboard)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := blackboard.' + node_name + '_update_success ? success : running;' + os.linesep))
            variables[node_name + '_update_success'] = {
                'name' : node_name + '_update_success',
                'mode' : 'VAR',
                'custom_value_range' : '{TRUE, FALSE}',
                'min_value' : 0,
                'max_value' : 1,
                'init_value' : None,
                'next_value' : [],
                'read_by' : [True],
                'environment_update' : [('TRUE', '{TRUE, FALSE}')]
            }
            if mon.topic_bbvar.name in variables:
                variable = variables[mon.topic_bbvar.name]
                variable['next_value'].append((node_name,
                                               [('TRUE',
                                                 (('{' + ', '.join(map(str, range(variable['min_value'], variable['max_value'] + 1))) + '}') if variable['custom_value_range'] is None else (
                                                     variable['custom_value_range'])))
                                                ]))

            for set_var in mon.set_vars:
                variable_name = set_var.variable.name
                variables[variable_name]['next_value'].append((node_name,
                                                               [('(' + node_name + '_update_success = FALSE)', format_variable(set_var.variable, node_name, variables, True, False, False))]
                                                               + make_new_stage(set_var, node_name, variables, True, False, True)))

    elif textx.textx_isinstance(current_node, metamodel['TimerBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'leaf', 'action',
                                                True, True, False,
                                                internal_status_module_name = None,
                                                internal_status_module_code = None)

    if nodes[node_name]['category'] == 'leaf':
        pass
    else:
        for child in current_node.nodes:
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
