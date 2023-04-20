import textx
import argparse
import os
import itertools
from behaverify_common import indent
import serene_functions


def format_function_before(function_name, code, node_name):
    return (
        function_name + '('
        + ', '.join([format_code(value, node_name) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, node_name):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, node_name) for value in code.function_call.values])
        + ')'
        )


FUNCTION_FORMAT = {
    'abs' : ('abs', format_function_before),
    'max' : ('max', format_function_before),
    'min' : ('min', format_function_before),
    'sin' : ('math.sin', format_function_before),
    'cos' : ('math.cos', format_function_before),
    'tan' : ('math.tan', format_function_before),
    'ln' : ('math.log', format_function_before),
    'not' : ('not ', format_function_before),  # space intentionally added here
    'and' : ('and', format_function_between),
    'or' : ('or', format_function_between),
    'xor' : ('operator.xor', format_function_between),
    'xnor' : ('xnor', format_function_between),
    'implies' : ('->', format_function_between),
    'equivalent' : ('==', format_function_between),
    'equal' : ('==', format_function_between),
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
    'mod' : ('%', format_function_between),
    'count' : ('count', format_function_before)
}


def format_variable_name_only(variable_name, is_local, is_env, node_name):
    # return (((node_name + '.') if is_local else ('blackboard_reader.' if not is_env else '')) + variable_name)
    return ((('') if is_local else ('blackboard_reader.' if not is_env else '')) + variable_name)


def format_variable(variable, is_local, is_env, node_name):
    return (
        ('' if is_local or is_env else 'blackboard_reader.')
        + variable.name
        + ('()' if variable.model_as == 'DEFINE' else '')
    )


# def format_code(code, node_name):
#     return (
#         (str(code.constant).upper() if isinstance(code.constant, bool) else str(handle_constant(code.constant))) if code.constant is not None else (
#             (format_variable(code.variable, (code.mode == 'local'), (code.node_name if hasattr(code, 'node_name') else node_name), (code.mode == 'env'), variables, local_variables, use_stages, use_next, not_next, (code.read_at if hasattr(code, 'read_at') else None))) if code.variable is not None else (
#                 ('(' + format_code(code.code_statement, node_name, variables, local_variables, use_stages, use_next, not_next) + ')') if code.code_statement is not None else (
#                     format_function(code, node_name, variables, local_variables, use_stages, use_next, not_next)
#                 )
#             )
#         )
#     )


def format_code(code, node_name):
    # print(code)
    # print(dir(code))
    # print('constant: ' + str(code.constant))
    # print('variable: ' + str(code.variable))
    return (
        (
            (("'" + handle_constant(code.constant) + "'") if isinstance(handle_constant(code.constant), str) else str(handle_constant(code.constant))) if code.constant is not None else (
                (format_variable(code.variable, code.mode == 'local', code.mode == 'env', node_name)) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, node_name) + ')') if code.code_statement is not None else (
                        FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, node_name)
                    )
                )
            )
        )
    )


def handle_constant(constant):
    global constants
    return (constants[constant] if constant in constants else constant)


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


def variable_assignment(values, node_name, range_mode):
    return (
        (
            'random.choice(['
            + ', '.join([str(value) for value in range(handle_constant(values[0]), handle_constant(values[1]) + 1)
                         if cond_func(value)])
            + '])'
        )
        if (range_mode and ((cond_func := build_range_func(values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
        ('random.choice(['
         + ', '.join([format_code(value, node_name) for value in values])
         + '])')
        if len(values) > 1 else
        format_code(values[0], node_name)
    )


def format_statement(statement, node_name, indent_level = 2, override_variable_name = None):
    variable_name = (
        format_variable(statement.variable, statement.mode == 'local', statement.mode == 'env', node_name)
        if override_variable_name is None else override_variable_name
    )
    if len(statement.case_results) == 0:
        return (indent(indent_level) + variable_name + ' = ' + variable_assignment(statement.default_result.values, node_name, statement.default_result.range_mode) + os.linesep)
    return ((''.join([
        (indent(indent_level) + 'elif ' + format_code(case_result.condition, node_name) + ':' + os.linesep
         + (indent(indent_level + 1) + variable_name + ' = ' + variable_assignment(case_result.values, node_name, case_result.range_mode) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(indent_level) + 'else:' + os.linesep
               + indent(indent_level + 1) + variable_name + ' = ' + variable_assignment(statement.default_result.values, node_name, statement.default_result.range_mode) + os.linesep)
            )


def variable_init(variable):
    return (
        create_variable_macro(variable)
        if variable.model_as == 'DEFINE' else
        format_statement(variable.initial_value, None, 0, format_variable(variable, False, True, None))
    )
    # variable_name = format_variable(variable, False, True, None)
    # variables_initial = {
    #     format_variable(statement.variable, False, True, None) : (format_statement(statement, None, 0) if statement.variable.model_as != 'DEFINE' else create_variable_macro(statement))
    #     for statement in model.initial
    #     }

    # return (variable_name + ' = random.choice(['
    #         + (
    #             ', '.join(map(str, range(variable.domain.min_val, variable.domain.max_val + 1)))
    #             if variable.domain.min_val is not None else (
    #                     'True, False' if variable.domain.boolean is not None else (
    #                         ', '.join(map(str, variable.domain.enums))
    #                     )
    #             )
    #         )
    #         + '])' + os.linesep)


def create_variable_macro(variable):
    return (
        os.linesep
        + 'def ' + variable.name + '():' + os.linesep
        + format_statement(variable.initial_value, None, 1, '_' + variable.name + '_value_to_return_')
        + indent(1) + 'return _' + variable.name + '_value_to_return_' + os.linesep
    )


def flatten(array_of_array, running_total = []):
    return (
        flatten(array_of_array[1:], running_total + array_of_array[0])
        if len(array_of_array) > 0 else
        running_total
    )


def find_local_variables(code, node_name):
    return (
        (
            ([]) if code.constant is not None else (
                ([format_variable(code.variable, code.mode == 'local', code.mode == 'env', node_name)] if code.mode == 'local' else []) if code.variable is not None else (
                    ('(' + find_local_variables(code.code_statement, node_name) + ')') if code.code_statement is not None else (
                        flatten(
                            [
                                find_local_variables(value, node_name)
                                for value in code.function_call.values
                            ]
                        )
                    )
                )
            )
        )
    )


def handle_check_env(node):
    return (node.import_from,
            (
                'def '
                + (
                    node.python_function.split('.')[-1]
                    + '('
                    + ', '.join(sorted(list(set(find_local_variables(node.condition, node.name)))))
                    + '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                # + indent(1) + '-- ARGUMENTS' + os.linesep
                # + ''.join(
                #     [
                #         (indent(1) + '@ arg' + str(x) + ' : ' + format_code(node.args[x], node.name) + os.linesep)
                #         for x in range(len(node.args))
                #     ]
                # )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return True or False.' + os.linesep
                + indent(1) + 'This method is being modeled using the following behavior:' + os.linesep
                + indent(1) + format_code(node.condition, node.name) + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
                + indent(1) + '# below we include an auto generated attempt at implmenting this' + os.linesep
                + indent(1) + 'return (' + os.linesep
                + indent(2) + format_code(node.condition, node.name) + os.linesep
                + indent(1) + ')' + os.linesep
            )
            if node.python_function is not None else '')


def handle_read_statement(statement, node_name):
    function_name = statement.python_function.split('.')[-1]
    return (statement.import_from,
            (
                'def '
                + (
                    function_name
                    + '('
                    + ', '.join(sorted(list(set(
                        find_local_variables(statement.condition, node_name)
                        + flatten(
                            [
                                flatten(
                                    [
                                        (find_local_variables(case_result.condition, node_name)
                                         + ([] if case_result.range_mode else flatten([find_local_variables(value, node_name) for value in case_result.values]))
                                         )
                                        for case_result in variable_statement.case_results
                                    ]
                                )
                                + (
                                    [] if variable_statement.default_result.range_mode else flatten([find_local_variables(value, node_name) for value in variable_statement.default_result.values])
                                )
                                for variable_statement in statement.variable_statements
                            ]
                        )
                    ))))
                    + '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                # + indent(1) + '-- ARGUMENTS' + os.linesep
                # + ''.join(
                #     [
                #         (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x], node_name) + os.linesep)
                #         for x in range(len(statement.args))
                #     ]
                # )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return a tuple.' + os.linesep
                + indent(1) + 'The values in the tuple should be as follows:' + os.linesep
                + indent(2) + '0: True or False. Indicates if other variables will be updated.' + os.linesep
                + indent(2) + 'Modeled using the following behavior:' + os.linesep
                + ((indent(3) + 'modeled nondeterministically. no restriction') if statement.condition_variable is not None else (
                    indent(3) + format_code(statement.condition, node_name)))
                + os.linesep
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + 'to_return_' + statement.variable_statements[x].variable.name
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.variable_statements[x], node_name) + os.linesep
                         )
                        for x in range(len(statement.variable_statements))
                    ])
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
                + indent(1) + '# below we include an auto generated attempt at implmenting this' + os.linesep
                + indent(1) + function_name + '__return_condition = '
                + (
                    format_code(statement.condition, node_name)
                    if statement.condition_variable is None else
                    'random.choice([True, False])'
                )
                + os.linesep
                + indent(1) + 'if ' + function_name + '__return_condition:' + os.linesep
                + ''.join(
                    [
                        (format_statement(variable_statement, node_name, indent_level = 2, override_variable_name = ('to_return_' + variable_statement.variable.name)))
                        for variable_statement in statement.variable_statements
                    ]
                )
                + indent(2) + 'return (True' + (', ' if len(statement.variable_statements) > 0 else '')
                + ', '.join(
                    [
                        'to_return_' + variable_statement.variable.name
                        for variable_statement in statement.variable_statements
                    ]
                )
                + ')' + os.linesep
                + indent(1) + 'else:' + os.linesep
                + indent(2) + 'return (False' + (', None' * len(statement.variable_statements)) + ')' + os.linesep
            )
            if statement.python_function is not None else '')


def handle_write_statement(statement, node_name):
    return (statement.import_from,
            (
                'def '
                + (
                    statement.python_function.split('.')[-1]
                    + '('
                    + ', '.join(sorted(list(set(
                        flatten(
                            [
                                flatten(
                                    [
                                        (find_local_variables(case_result.condition, node_name)
                                         + ([] if case_result.range_mode else flatten([find_local_variables(value, node_name) for value in case_result.values]))
                                         )
                                        for case_result in update.case_results
                                    ]
                                )
                                + (
                                    [] if update.default_result.range_mode else flatten([find_local_variables(value, node_name) for value in update.default_result.values])
                                )
                                for update in statement.update
                            ]
                        )
                    ))))
                    + '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                # + indent(1) + '-- ARGUMENTS' + os.linesep
                # + ''.join(
                #     [
                #         (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x], node_name) + os.linesep)
                #         for x in range(len(statement.args))
                #     ]
                # )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method does not need to return any value (though it may).' + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to effect the environment.' + os.linesep
                + indent(1) + 'The following changes are expected:' + os.linesep
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + format_variable(statement.update[x].variable, False, True, node_name)
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.update[x], node_name) + os.linesep
                         )
                        for x in range(len(statement.update))
                    ])
                + indent(1) + "'''" + os.linesep
                + indent(1) + '# below we include an auto generated attempt at implmenting this' + os.linesep
                + indent(1) + 'global delayed_action_queue'
                + ', '.join(
                    [
                        (format_variable(update.variable, False, True, node_name))
                        for update in statement.update if update.instant
                    ]
                )
                + os.linesep
                + os.linesep
                + ''.join(
                    [
                        (format_statement(update, node_name, 1))
                        for update in statement.update if update.instant
                    ]
                )
                + ''.join(
                    [
                        (indent(1) + 'def delayed_update_for__' + format_variable(update.variable, False, True, node_name) + '():' + os.linesep
                         + indent(2) + 'global ' + format_variable(update.variable, False, True, node_name) + os.linesep
                         + format_statement(update, node_name, 2)
                         + indent(2) + 'return' + os.linesep
                         + indent(1) + 'delayed_action_queue.append(delayed_update_for__' + format_variable(update.variable, False, True, node_name) + ')' + os.linesep
                         + os.linesep)
                        for update in statement.update if not update.instant
                    ]
                )
                + indent(1) + 'return' + os.linesep
            )
            if statement.python_function is not None else '')


def default_preamble(blackboard_variables, environment_variables, updates):
    return (
        'import py_trees' + os.linesep
        + 'import random' + os.linesep
        + os.linesep
        + os.linesep
        + 'delayed_action_queue = []' + os.linesep
        + os.linesep
        + os.linesep
        + 'def execute_delayed_action_queue():' + os.linesep
        + indent(1) + 'global delayed_action_queue' + os.linesep
        + indent(1) + 'for delayed_action in delayed_action_queue:' + os.linesep
        + indent(2) + 'delayed_action()' + os.linesep
        + indent(1) + 'return' + os.linesep
        + os.linesep
        + os.linesep
        + 'blackboard_reader = py_trees.blackboard.Client()' + os.linesep
        + ''.join(
            [
                ('blackboard_reader.register_key(key = ' + "'" + blackboard_variable.name + "'" + ', access = py_trees.common.Access.READ)' + os.linesep)
                for blackboard_variable in blackboard_variables
            ]
        )
        + os.linesep
        + os.linesep
        + 'def between_tick_environment_update():' + os.linesep
        + (
            indent(1) + 'global ' + ', '.join([format_variable(variable, False, True, None) for variable in environment_variables if variable.model_as == 'VAR']) + os.linesep
            + ''.join(
                [
                    format_statement(update, None)
                    for update in updates
                ]
            )
        )
        + indent(1) + 'return' + os.linesep
        + os.linesep
        + os.linesep
    )


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('default_file')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    to_write = {}
    # variables_initial = {
    #     format_variable(statement.variable, False, True, None) : (format_statement(statement, None, 0) if statement.variable.model_as != 'DEFINE' else create_variable_macro(statement))
    #     for statement in model.initial
    #     }
    variables_update = {
        format_variable_name_only(variable_name, False, True, None) : (
            ''.join(
                [
                    ('# ' + format_statement(statement, None).replace(os.linesep, os.linesep + '# ').rstrip() + os.linesep)
                    for statement in group
                ])
        )
        for variable_name, group in itertools.groupby(
                sorted(model.update, key = (lambda x : x.variable.name)),
                key = (lambda x : x.variable.name))
        }

    to_write[args.default_file] = {
        None : (
            default_preamble(model.blackboard_variables, model.environment_variables, model.update)
            + (os.linesep).join(
                [
                    (
                        variable_init(variable)
                        # + os.linesep
                        + (
                            os.linesep
                            if variable.model_as == 'DEFINE' else
                            (
                                ('# this variable is a constant. do not change it' + os.linesep)
                                if variable.model_as == 'FROZENVAR' else
                                (('# this variable develops in the following way between ticks.' + os.linesep + variables_update[format_variable(variable, False, True, None)])
                                 if format_variable(variable, False, True, None) in variables_update else
                                 ('# this variable does not change between ticks' + os.linesep
                                  + '# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it' + os.linesep))
                            )
                        )
                    )
                    for variable in model.environment_variables
                ]
            )
        )
    }

    for check_env in model.environment_checks:
        (file_name, function_name, function_body) = handle_check_env(check_env)
        if file_name is None:
            print('WARNING: a check environment node had no import.')
            print('Node name is : ' + check_env.name)
            file_name = args.defualt_file
        if file_name in to_write:
            if function_name in to_write[file_name]:
                to_write[file_name][function_name] += function_body
            else:
                to_write[file_name][function_name] = function_body
        else:
            to_write[file_name] = {function_name : function_body}

    for action in model.action_nodes:
        for statement in itertools.chain(action.init_statements, action.pre_update_statements, action.post_update_statements):
            if statement.variable_statement is not None:
                continue
            (file_name, function_name, function_body) = (
                handle_read_statement(statement.read_statement, action.name)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, action.name))
            if file_name is None:
                print('WARNING: a statement in an action node had no import.')
                print('Node name is : ' + action.name)
                file_name = args.defualt_file
            if file_name in to_write:
                if function_name in to_write[file_name]:
                    to_write[file_name][function_name] += function_body
                else:
                    to_write[file_name][function_name] = function_body
            else:
                to_write[file_name] = {function_name : function_body}

    for file_name in to_write:
        with open(args.location + file_name + '.py', 'w') as f:
            f.write(
                (os.linesep + os.linesep).join(
                    [
                        (
                            ('' if function_name is None else function_name)
                            + to_write[file_name][function_name]
                            # + ('' if function_name is None else (indent(1) + 'pass' + os.linesep))
                        )
                        for function_name in to_write[file_name]
                    ]
                )
            )
    return


if __name__ == '__main__':
    main()
