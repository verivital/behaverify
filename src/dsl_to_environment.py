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
    return ((('') if is_local else ('blackboard_reader.' if not is_env else '')) + variable_name)


def format_variable(variable, is_local, is_env, node_name):
    return (
        (
            'node.'
            if is_local
            else
            (
                ''
                if is_env
                else
                'blackboard_reader.'
            )
        )
        + variable.name
        + ('()' if variable.model_as == 'DEFINE' else '')
    )


def format_code(code, node_name):
    return (
        (
            handle_constant_str(code.constant) if code.constant is not None else (
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


def handle_constant_str(constant):
    new_constant = handle_constant(constant)
    return (("'" + new_constant + "'") if isinstance(new_constant, str) else str(new_constant))


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


def create_variable_macro(variable):
    return (
        os.linesep
        + 'def ' + variable.name + '():' + os.linesep
        + format_statement(variable.initial_value, None, 1, '_' + variable.name + '_value_to_return_')
        + indent(1) + 'return _' + variable.name + '_value_to_return_' + os.linesep
    )


def handle_check_env(node):
    return (
        'def '
        + node.name
        + '(node):' + os.linesep
        + indent(1) + "'''" + os.linesep
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


def handle_read_statement(statement, node_name):
    return (
        os.linesep
        + os.linesep
        + 'def ' + statement.name + '__condition(node):' + os.linesep
        + indent(1) + 'return '
        + (
            format_code(statement.condition, node_name)
            if statement.condition_variable is None else
            'random.choice([True, False])'
        )
        + os.linesep
        + ''.join(
            [
                (
                    os.linesep
                    + os.linesep
                    + 'def ' + statement.name + '__' + str(index) + '(node):' + os.linesep
                    + (format_statement(read_var_state, node_name, indent_level = 1, override_variable_name = ('to_return_' + read_var_state.variable.name)))
                    + indent(1) + 'return to_return_' + read_var_state.variable.name + os.linesep
                )
                for index, read_var_state in enumerate(statement.variable_statements)
            ]
        )
    )


def handle_write_statement(statement, node_name):
    def update_is_safe(env_update):
        if env_update.variable.model_as != 'VAR':
            raise Exception('Variable ' + env_update.variable.name + ' is being updated even though it is modeled as ' + env_update.variable.model_as)
        return True
    return (
        ''.join(
            [
                (
                    os.linesep
                    + os.linesep
                    + 'def ' + statement.name + '__' + str(index) + '(node):' + os.linesep
                    + indent(1) + 'global ' + format_variable(env_update.variable, False, True, node_name) + os.linesep
                    + (format_statement(env_update, node_name, indent_level = 1, override_variable_name = ('update_val_' + env_update.variable.name)))
                    + indent(1) + format_variable(env_update.variable, False, True, node_name)
                    + ' = serene_safe_assignment.' + env_update.variable.name + '(update_val_' + env_update.variable.name + ')' + os.linesep
                    + indent(1) + 'return' + os.linesep
                )
                for index, env_update in enumerate(statement.update) if update_is_safe(env_update)
            ]
        )
    )


def default_preamble(blackboard_variables, environment_variables, updates):
    return (
        'import py_trees' + os.linesep
        + 'import random' + os.linesep
        + 'import serene_safe_assignment' + os.linesep
        + os.linesep
        + os.linesep
        + 'delayed_action_queue = []' + os.linesep
        + os.linesep
        + os.linesep
        + 'def delay_this_action(action, node):' + os.linesep
        + indent(1) + 'global delayed_action_queue' + os.linesep
        + indent(1) + 'delayed_action_queue.append((action, node))' + os.linesep
        + os.linesep
        + os.linesep
        + 'def execute_delayed_action_queue():' + os.linesep
        + indent(1) + 'global delayed_action_queue' + os.linesep
        + indent(1) + 'for (delayed_action, node) in delayed_action_queue:' + os.linesep
        + indent(2) + 'delayed_action(node)' + os.linesep
        + indent(1) + 'delayed_action_queue = []' + os.linesep
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
                    format_statement(update, None, indent_level = 1)
                    for update in updates
                ]
            )
        )
        + indent(1) + 'return' + os.linesep
        + os.linesep
        + os.linesep
    )


def write_environment(model, location, const_name):

    global CONSTANT_NAME
    CONSTANT_NAME = const_name

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

    to_write = (
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

    for check_env in model.environment_checks:
        to_write += handle_check_env(check_env)

    for action in model.action_nodes:
        for statement in itertools.chain(action.init_statements, action.pre_update_statements, action.post_update_statements):
            if statement.variable_statement is not None:
                continue
            to_write += (
                handle_read_statement(statement.read_statement, action.name)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, action.name))

    with open(location + CONSTANT_NAME + '_environment.py', 'w') as f:
        f.write(to_write)
    return


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location')
    arg_parser.add_argument('default_file')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    write_environment(model, args.location, args.default_file)


if __name__ == '__main__':
    main()
