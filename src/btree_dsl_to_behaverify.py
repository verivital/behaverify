import textx
import argparse
import pprint
import os
# import sys
# import itertools
# import copy

from behaverify_common import create_node_name, create_node_template, create_variable_template


def get_variables(model, keep_stage_0):
    return {variable.name :
            create_variable_template(variable.name, 'DEFINE' if (len(variable.model.enums) == 1) else 'VAR',
                                     (None if variable.model.range_minimum is not None else ('{TRUE, FALSE}' if variable.model.is_bool is not None else ('{' + ', '.join(map(str, variable.model.enums)) + '}'))),
                                     0 if variable.model.range_minimum is None else variable.model.range_minimum,
                                     1 if variable.model.range_minimum is None else variable.model.range_maximum,
                                     (None if variable.initial_value is None else (
                                         [('TRUE', (str(variable.initial_value).upper() if isinstance(variable.initial_value, bool) else str(variable.initial_value)))]
                                         )
                                      ),
                                     [], prefix = 'var_', keep_stage_0 = keep_stage_0)
            for variable in model.bbVariables if variable.model is not None}


def make_new_stage(statement, node_name, variables, use_next, not_next):
    return (
        [(format_code(case_result.condition, node_name, variables, use_next, not_next),
          format_code(case_result.update_value, node_name, variables, use_next, not_next))
         for case_result in statement.updates]
        +
        [('TRUE',
          format_code(statement.default_update, node_name, variables, use_next, not_next))]
    )


def is_nondeterministic(code):
    return (
        False if (code.constant is not None or code.variable is not None) else (
            is_nondeterministic(code.CodeStatement) if code.CodeStatement is not None else (
                True if code.function_call.function_name == 'any' else (
                    any([is_nondeterministic(value) for value in code.function_call.values])
                    )
                )
            )
        )


def compute_stage(variable_name, variables, overwrite_stage = None):
    if overwrite_stage is not None:
        return (('_stage_' + str(min(overwrite_stage, len(variables[variable_name]['next_value']))) if overwrite_stage > 0 else (
            '' if overwrite_stage == 0 else (
                '_stage_' + str(len(variables[variable_name]['next_value']))
            ))))
    return (('_stage_' + str(len(variables[variable_name]['next_value']))) if (len(variables[variable_name]['next_value']) > 0) else '')


def format_variable(variable, node_name, variables, use_next, not_next, overwrite_stage = None):
    if len(variables[variable.name]['next_value']) == 0 or overwrite_stage == 0:
        variables[variable.name]['keep_stage_0'] = True
    if use_next and variable.name == not_next:
        return 'LINK_TO_PREVIOUS_FINAL_' + variables[variable.name]['prefix'] + variable.name
    return (('' if not use_next else 'next(')
            + variables[variable.name]['prefix']
            + variable.name
            + compute_stage(variable.name, variables, overwrite_stage)
            + ('' if not use_next else ')'))


def format_function_before(function_name, code, node_name, variables, use_next, not_next):
    return (
        function_name + '('
        + ', '.join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + ')'
    )


def format_function_between(function_name, code, node_name, variables, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + ')'
    )


def format_function_after(function_name, code, node_name, variables, use_next, not_next):
    return (
        '('
        + code.function_call.node_name
        + function_name
        + ')'
    )


def format_function_before_bounded(function_name, code, node_name, variables, use_next, not_next):
    return (
        function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] '  '('
        + ', '.join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + ')'
    )


def format_function_between_bounded(function_name, code, node_name, variables, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] ').join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + ')'
    )


def format_function_before_between(function_name, code, node_name, variables, use_next, not_next):
    return (
        function_name[0] + '('
        + (' ' + function_name[1] + ' ').join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + ')'
    )


def format_function_non_determinism(function_name, code, node_name, variables, use_next, not_next):
    return (
        '{'
        + ', '.join([format_code(value, node_name, variables, use_next, not_next) for value in code.function_call.values])
        + '}'
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
    'any' : (None, format_function_non_determinism),
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


def format_function(code, node_name, variables, use_next, not_next):
    (function_name, function_to_call) = FUNCTION_FORMAT[code.function_call.function_name]
    return function_to_call(function_name, code, node_name, variables, use_next, not_next)


def format_code(code, node_name, variables, use_next, not_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, node_name, variables, use_next, not_next, (code.read_at if hasattr(code, 'read_at') else None))) if code.variable is not None else (
                ('(' + format_code(code.CodeStatement, node_name, variables, use_next, not_next) + ')') if code.CodeStatement is not None else (
                    format_function(code, node_name, variables, use_next, not_next)
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
    else:
        node_name = None

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

            variable_name = format_variable(check.bbvar, node_name, variables, False, None)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'check',
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
            node_name = create_node_name(check.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            variable_name = format_variable(check.bbvar, node_name, variables, False, None)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'check',
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
            node_name = create_node_name(task.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            if hasattr(task, 'type'):
                nodes[node_name] = create_node_template(node_name, parent_name,
                                                        'leaf', 'action',
                                                        str(task.type) == 'success', str(task.type) == 'running', str(task.type) == 'failure',
                                                        additional_arguments = [],
                                                        internal_status_module_name = None,
                                                        internal_status_module_code = None)
                continue

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'action',
                                                    task.return_status == 'success', task.return_status == 'running', task.return_status == 'failure',
                                                    additional_arguments = [],
                                                    internal_status_module_name = None,
                                                    internal_status_module_code = None)

            for set_var in task.set_vars:
                variable_name = set_var.variable.name
                keep_stage_0 = variables[variable_name]['keep_stage_0']
                non_determinism = is_nondeterministic(set_var.default_update) or any([is_nondeterministic(update.update_value) for update in set_var.updates])
                keep_stage_0 = keep_stage_0 or (not non_determinism)  # if stage_1 is deterministic, then we keep stage 0.
                if (keep_stage_0 or len(variables[variable_name]['next_value']) > 0):
                    # nothing fancy, just add it
                    variables[variable_name]['next_value'].append((node_name,
                                                                   non_determinism,
                                                                   make_new_stage(set_var, node_name, variables, False, None)))
                else:
                    variables[variable_name]['next_value'].append((node_name,
                                                                   non_determinism,
                                                                   make_new_stage(set_var, node_name, variables, True, variable_name)))
                variables[variable_name]['keep_stage_0'] = keep_stage_0  # reset keep_stage_0 (or properly mark it if non_determinism changed it)

    elif textx.textx_isinstance(current_node, metamodel['MonBTNode']):
        for mon in current_node.mon:
            if mon.ignore_node:
                continue
            node_name = create_node_name(mon.name.replace(' ', ''), node_names)
            node_names.add(node_name)
            if parent_name is not None:
                nodes[parent_name]['children'].append(node_name)

            nodes[node_name] = create_node_template(node_name, parent_name,
                                                    'leaf', 'read_action',
                                                    True, True, False,
                                                    additional_arguments = [node_name + '_update_success'],
                                                    internal_status_module_name = node_name + '_module',
                                                    internal_status_module_code = (
                                                        'MODULE ' + node_name + '_module(' + node_name + '_update_success)' + os.linesep
                                                        + '\tCONSTANTS' + os.linesep
                                                        + '\t\tsuccess, failure, running, invalid;' + os.linesep
                                                        + '\tDEFINE' + os.linesep
                                                        + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                                                        + '\t\tinternal_status := ' + node_name + '_update_success ? success : running;' + os.linesep))

            variables[node_name + '_update_success'] = create_variable_template(node_name + '_update_success', 'VAR',
                                                                                '{TRUE, FALSE}', 0, 1, None,
                                                                                [])

            if (mon.topic_bbvar.name) in variables and (not mon.ignore_topic):
                variable = variables[mon.topic_bbvar.name]
                if variable['keep_stage_0'] or len(variable['next_value']) > 0:
                    variable['next_value'].append((node_name,
                                                   True,  # this is assumed to be non_deterministic
                                                   [(node_name + '_update_success',
                                                     (('{' + ', '.join(map(str, range(variable['min_value'], variable['max_value'] + 1))) + '}') if variable['custom_value_range'] is None else (
                                                         variable['custom_value_range']))),
                                                    ('TRUE',
                                                     format_variable(mon.topic_bbvar, node_name, variables, False, None))
                                                    ]))
                else:
                    variable['next_value'].append((node_name,
                                                   True,  # this is assumed to be non_deterministic
                                                   [('next(' + node_name + '_update_success)',
                                                     (('{' + ', '.join(map(str, range(variable['min_value'], variable['max_value'] + 1))) + '}') if variable['custom_value_range'] is None else (
                                                         variable['custom_value_range']))),
                                                    ('TRUE',
                                                     format_variable(mon.topic_bbvar, node_name, variables, True, mon.topic_bbvar.name))
                                                    ]))
                    variable['keep_stage_0'] = False

            for set_var in mon.set_vars:
                variable_name = set_var.variable.name
                keep_stage_0 = variables[variable_name]['keep_stage_0']
                non_determinism = is_nondeterministic(set_var.default_update) or any([is_nondeterministic(update.update_value) for update in set_var.updates])
                keep_stage_0 = keep_stage_0 or (not non_determinism)  # if stage_1 is deterministic, then we keep stage 0.
                if (keep_stage_0 or len(variables[variable_name]['next_value']) > 0):
                    # nothing fancy, just add it
                    variables[variable_name]['next_value'].append((node_name,
                                                                   non_determinism,
                                                                   make_new_stage(set_var, node_name, variables, False, None)))
                else:
                    variables[variable_name]['next_value'].append((node_name,
                                                                   non_determinism,
                                                                   make_new_stage(set_var, node_name, variables, True, variable_name)))
                variables[variable_name]['keep_stage_0'] = keep_stage_0  # reset keep_stage_0 (or properly mark it if non_determinism changed it)

    elif textx.textx_isinstance(current_node, metamodel['TimerBTNode']):
        nodes[node_name] = create_node_template(node_name, parent_name,
                                                'leaf', 'action',
                                                True, True, False,
                                                internal_status_module_name = None,
                                                internal_status_module_code = None)

    if node_name is None or nodes[node_name]['category'] == 'leaf':
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


def handle_specifications(specifications, variables):
    return [
        (
            specification.spec_type
            + ' '
            + format_code(specification.CodeStatement, '', variables, False, None)
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

    variables = get_variables(model, args.keep_stage_0)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, None, variables, False, None)
    specifications = handle_specifications(model.specifications, variables)  # this included here to ensure we don't erase stage 0 used by specifications.
    nodes = walk_tree(metamodel, model, variables)
    specifications = handle_specifications(model.specifications, variables)

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
