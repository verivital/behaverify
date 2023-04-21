import textx
import argparse
import os
import sys
import itertools
from behaverify_common import indent, create_node_name
import serene_functions


def format_function_before(function_name, code, global_init = False):
    return (
        function_name + '('
        + ', '.join([format_code(value, global_init) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, global_init = False):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, global_init) for value in code.function_call.values])
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
    'not' : ('not', format_function_before),
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


def format_variable(variable, is_local, global_init = False):
    return (
        (
            ('blackboard_reader.')
            if global_init else
            ('self.' + ('' if is_local else 'blackboard.'))
        )
        + variable.name
        + ('()' if variable.model_as == 'DEFINE' else '')
    )


def format_code(code, global_init = False):
    return (
        (
            (("'" + handle_constant(code.constant) + "'") if isinstance(handle_constant(code.constant), str) else str(handle_constant(code.constant))) if code.constant is not None else (
                (format_variable(code.variable, code.mode == 'local', global_init)) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, global_init) + ')') if code.code_statement is not None else (
                        FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, global_init)
                    )
                )
            )
        )
    )


def handle_constant(constant):
    global constants
    return (constants[constant] if constant in constants else constant)


def find_local_variables(code):
    return (
        (
            ([]) if code.constant is not None else (
                ([format_variable(code.variable, code.mode == 'local')] if code.mode == 'local' else []) if code.variable is not None else (
                    ('(' + find_local_variables(code.code_statement) + ')') if code.code_statement is not None else (
                        flatten(
                            [
                                find_local_variables(value)
                                for value in code.function_call.values
                            ]
                        )
                    )
                )
            )
        )
    )


def flatten(array_of_array, running_total = []):
    return (
        flatten(array_of_array[1:], running_total + array_of_array[0])
        if len(array_of_array) > 0 else
        running_total
    )


STANDARD_IMPORTS = ('import py_trees' + os.linesep
                    + 'import math' + os.linesep
                    + 'import operator' + os.linesep
                    + 'import random' + os.linesep)


def class_definition(node_name):
    return ('class ' + node_name + '(py_trees.behaviour.Behaviour):' + os.linesep)


def init_method_check(node):
    return (indent(1) + 'def __init__(self, name):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + os.linesep)


def update_method_check(node):
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return ((py_trees.common.Status.SUCCESS) if ('
            + format_code(node.condition)
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep
            + os.linesep)


def init_method_check_env(node):
    return init_method_check(node)
    # return (indent(1) + 'def __init__(self, name):' + os.linesep
    #         + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
    #         + indent(2) + 'self.name = name' + os.linesep
    #         + os.linesep)


def update_method_check_env(node):
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return ((py_trees.common.Status.SUCCESS) if ('
            + ('' if node.python_function is None else (
                ((node.import_from + '.') if node.import_from is not None else '') + node.python_function
                + '('
                + ', '.join(sorted(list(set(find_local_variables(node.condition)))))
                + ')'
            ))
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep
            + os.linesep)


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


def variable_assignment(values, range_mode, global_init = False):
    return (
        (
            'random.choice(['
            + ', '.join([str(value) for value in range(handle_constant(values[0]), handle_constant(values[1]) + 1)
                         if cond_func(value)])
            + '])'
        )
        if (range_mode and ((cond_func := build_range_func(values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
        ('random.choice(['
         + ', '.join([format_code(value, global_init) for value in values])
         + '])')
        if len(values) > 1 else
        format_code(values[0], global_init)
    )


def handle_variable_statement(statement, indent_level = 2, global_init = False, override_variable_name = None):
    variable_name = (format_variable(statement.variable, statement.mode == 'local', global_init) if override_variable_name is None else override_variable_name)
    if len(statement.case_results) == 0:
        return (indent(indent_level) + variable_name + ' = ' + variable_assignment(statement.default_result.values, statement.default_result.range_mode, global_init) + os.linesep)
    return ((''.join([
        (indent(indent_level) + 'elif ' + format_code(case_result.condition, global_init) + ':' + os.linesep
         + (indent(indent_level + 1) + variable_name + ' = ' + variable_assignment(case_result.values, case_result.range_mode, global_init) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(indent_level) + 'else:' + os.linesep
               + indent(indent_level + 1) + variable_name + ' = ' + variable_assignment(statement.default_result.values, statement.default_result.range_mode, global_init) + os.linesep)
            )


def create_variable_macro(statement, function_name, variable_name, indent_level = 2, global_init = False):
    return (
        os.linesep
        + os.linesep
        + indent(indent_level) + 'def ' + function_name + '():' + os.linesep
        + handle_variable_statement(statement, indent_level + 1, global_init, function_name + '_return_val')
        + indent(indent_level + 1) + 'return ' + function_name + '_return_val' + os.linesep
        + os.linesep
        + indent(indent_level) + variable_name.replace('(', '').replace(')', '') + ' = ' + function_name + os.linesep
    )


def handle_read_statement(statement):
    if statement.python_function is None:
        if statement.condition_variable is not None:
            return (indent(2) + format_variable(statement.condition_variable, True) + ' = random.choice([True, False]);' + os.linesep)
        return ''
    # return (indent(2) + '('
    #         + ', '.join(
    #             ([] if statement.condition_variable is None else [format_variable(statement.condition_variable, True)])
    #             +
    #             [format_variable(var_statement.variable, var_statement.is_local) for var_statement in statement.variable_statements])
    #         + ') = ' + statement.python_function + os.linesep)
    return (indent(2) + 'temp_vals = ' +
            (
                ((statement.import_from + '.') if statement.import_from is not None else '') + statement.python_function
                + '('
                + ', '.join(sorted(list(set(
                    find_local_variables(statement.condition)
                    + flatten(
                        [
                            flatten(
                                [
                                    (find_local_variables(case_result.condition)
                                     + ([] if case_result.range_mode else flatten([find_local_variables(value) for value in case_result.values]))
                                     )
                                    for case_result in variable_statement.case_results
                                ]
                            )
                            + (
                                    [] if variable_statement.default_result.range_mode else flatten([find_local_variables(value) for value in variable_statement.default_result.values])
                            )
                            for variable_statement in statement.variable_statements
                        ]
                    )
                ))))
                + ')'
                + os.linesep
            )
            + indent(2) + 'if temp_vals[0]:' + os.linesep
            + indent(3) + '('
            + ', '.join(
                (['_'] if statement.condition_variable is None else [format_variable(statement.condition_variable, True)])
                +
                [format_variable(var_statement.variable, var_statement.mode == 'local') for var_statement in statement.variable_statements])
            + ') = temp_vals' + os.linesep
            + (
                (indent(2) + 'else:' + os.linesep
                 + indent(3) + format_variable(statement.condition_variable, True) + ' = False' + os.linesep)
                if statement.condition_variable is not None else '')
            )


def handle_write_statement(statement):
    return (
        (
            indent(2)
            + ((statement.import_from + '.') if statement.import_from is not None else '') + statement.python_function
            + '('
            + ', '.join(sorted(list(set(
                flatten(
                    [
                        flatten(
                            [
                                (find_local_variables(case_result.condition)
                                 + ([] if case_result.range_mode else flatten([find_local_variables(value) for value in case_result.values]))
                                 )
                                for case_result in update.case_results
                            ]
                                )
                        + (
                            [] if update.default_result.range_mode else flatten([find_local_variables(value) for value in update.default_result.values])
                        )
                        for update in statement.update
                    ]
                )
            ))))
            + ')'
            + os.linesep
        )
        if statement.python_function is not None else '')


def format_returns(status_result):
    return 'py_trees.common.Status.' + status_result.status.upper()


def handle_return_statement(statement):
    variable_name = 'return_status'
    if len(statement.case_results) == 0:
        return (indent(2) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
    return ((''.join([
        (indent(2) + 'elif ' + format_code(case_result.condition) + ':' + os.linesep
         + (indent(3) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(2) + 'else:' + os.linesep
               + indent(3) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
            )


def init_method_action(node):
    return (indent(1) + 'def __init__(self, name):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.WRITE)' + os.linesep) for variable in node.write_variables])
            + ''.join(
                [
                    (
                        create_variable_macro(local_variable.initial_value, local_variable.name, format_variable(local_variable, True, False), 2, False)
                        if local_variable.model_as == 'DEFINE' else
                        handle_variable_statement(local_variable.initial_value, indent_level = 2, global_init = False, override_variable_name = format_variable(local_variable, True, False))
                    )
                    for local_variable in node.local_variables if local_variable not in
                    [
                        statement.variable for statement in node.init_statements
                    ]
                ]
            )
            + ''.join([handle_statement(statement) for statement in node.init_statements])
            + os.linesep)


def handle_statement(statement):
    return (
        handle_variable_statement(statement.variable_statement) if statement.variable_statement is not None else (
            handle_read_statement(statement.read_statement) if statement.read_statement is not None else (
                handle_write_statement(statement.write_statement)
                )
            )
        )


def update_method_action(node):
    return (indent(1) + 'def update(self):' + os.linesep
            + ''.join([handle_statement(statement) for statement in node.pre_update_statements])
            + handle_return_statement(node.return_statement)
            + ''.join([handle_statement(statement) for statement in node.post_update_statements])
            + indent(2) + 'return return_status' + os.linesep
            )


def custom_imports(node):
    return ((('import ' + (os.linesep + 'import ').join(node.imports) + os.linesep) if node.imports is not None and len(node.imports) > 0 else '')
            + os.linesep + os.linesep)


def build_check_node(node):
    return (STANDARD_IMPORTS
            # + custom_imports(node)
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_check(node)
            + update_method_check(node)
            )


def build_check_environment_node(node):
    return (STANDARD_IMPORTS
            + custom_imports(node)
            + class_definition(node.name)
            + init_method_check_env(node)
            + update_method_check_env(node)
            )


def build_action_node(node):
    return (STANDARD_IMPORTS
            + custom_imports(node)
            + class_definition(node.name)
            + init_method_action(node)
            + update_method_action(node)
            )


def walk_tree(model, file_name):
    return walk_tree_recursive(model.root, set(), file_name)


def walk_tree_recursive(current_node, node_names, file_name):
    while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
        if hasattr(current_node, 'leaf'):
            current_node = current_node.leaf
        else:
            # print(dir(current_node))
            current_node = current_node.sub_root

    node_name = create_node_name(current_node.name.replace(' ', ''), node_names)
    node_names.add(node_name)

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    print(current_node.node_type)
    if current_node.node_type == 'check' or current_node.node_type == 'check_environment' or current_node.node_type == 'action':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = ' + current_node.name + '_file.' + current_node.name + '(' + "'" + node_name + "'" + ')' + os.linesep)
        return node_name
    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            sys.exit()
        decorator_type = (current_node.x.capitalize()
                          + 'Is'
                          + current_node.y.capitalize())
        child = walk_tree_recursive(current_node.child, node_names, file_name)
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                    + 'name = ' + "'" + node_name + "'" + ', child = ' + child + ')' + os.linesep)
        return node_name
    elif current_node.node_type == 'inverter':
        decorator_type = ('Inverter')
        child = walk_tree_recursive(current_node.child, node_names, file_name)
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                    + 'name = ' + "'" + node_name + "'" + ', child = ' + child + ')' + os.linesep)
        return node_name

    # so at this point, we're in composite node territory

    if current_node.node_type == 'sequence':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Sequence(' + "'" + node_name + "'" + ', ' + str(current_node.memory) + ')' + os.linesep)
    elif current_node.node_type == 'selector':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Selector(' + "'" + node_name + "'" + ', ' + str(current_node.memory) + ')' + os.linesep)
    elif current_node.node_type == 'parallel':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Parallel(' + "'" + node_name + "'" + ', py_trees.common.ParallelPolicy.'
                    + (('SuccessOnAll(' + str(current_node.memory) + ')') if current_node.parallel_policy == 'success_on_all' else ('SuccessOnOne()'))
                    + ')' + os.linesep)

    children = '[' + ', '.join([walk_tree_recursive(child, node_names, file_name) for child in current_node.children]) + ']'

    with open(file_name, 'a') as f:
        f.write(indent(1) + node_name + '.add_children('
                + children
                + ')'
                + os.linesep)
    return node_name


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('output_file', default = 'main.py')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    for action in model.action_nodes:
        with open(args.location + action.name + '_file.py', 'w') as f:
            f.write(build_action_node(action))
    for check in model.check_nodes:
        with open(args.location + check.name + '_file.py', 'w') as f:
            f.write(build_check_node(check))
    for check_env in model.environment_checks:
        print(check_env)
        with open(args.location + check_env.name + '_file.py', 'w') as f:
            f.write(build_check_environment_node(check_env))

    with open(args.location + args.output_file, 'w') as f:
        f.write(''.join([('import ' + node.name + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
                + 'import py_trees' + os.linesep
                + os.linesep + os.linesep
                + 'def create_tree():' + os.linesep
                + indent(1) + 'blackboard_reader = py_trees.blackboard.Client()' + os.linesep
                + ''.join(
                    [
                        (indent(1) + 'blackboard_reader.register_key(key = ' + "'" + blackboard_variable.name + "'" + ', access = py_trees.common.Access.WRITE)' + os.linesep)
                        for blackboard_variable in model.blackboard_variables
                    ]
                )
                + ''.join(
                    [
                        (
                            create_variable_macro(blackboard_variable.initial_value, blackboard_variable.name, format_variable(blackboard_variable, False, True), 1, True)
                            if blackboard_variable.model_as == 'DEFINE' else
                            handle_variable_statement(blackboard_variable.initial_value, indent_level = 1, global_init = True, override_variable_name = format_variable(blackboard_variable, False, True))
                        )
                        for blackboard_variable in model.blackboard_variables
                    ]
                )
                + os.linesep
                )
    root_name = walk_tree(model, args.location + args.output_file)

    with open(args.location + args.output_file, 'a') as f:
        f.write(indent(1) + 'return ' + root_name + os.linesep)

    return


if __name__ == '__main__':
    main()
