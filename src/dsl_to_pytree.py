import textx
import argparse
import os
# import sys
import itertools
from behaverify_common import indent, create_node_name
import serene_functions
import dsl_to_environment
from check_model import validate_model


# todo: replace is_local, is_env, by setting metamodel to a global constant and then using textx_isinstance


def format_function_before(function_name, code, init_mode = None):
    return (
        function_name + '('
        + ', '.join([format_code(value, init_mode) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, init_mode = None):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, init_mode) for value in code.function_call.values])
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


def format_variable_name_only(variable, is_local, init_mode = None):
    return (
        (
            ('blackboard_reader.')
            if init_mode == 'blackboard' else
            ('self.' + ('' if is_local else 'blackboard.'))
        )
        + variable.name
    )


def format_variable(variable, is_local, init_mode = None):
    return (
        (
            ('blackboard_reader.')
            if init_mode == 'blackboard' else
            ('self.' + ('' if is_local else 'blackboard.'))
        )
        + variable.name
        + ('()' if variable.model_as == 'DEFINE' else '')
    )


def format_code(code, init_mode = None):
    return (
        (
            handle_constant_str(code.constant) if code.constant is not None else (
                (format_variable(code.variable, code.mode == 'local', init_mode)) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, init_mode) + ')') if code.code_statement is not None else (
                        FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, init_mode)
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
                    + 'import random' + os.linesep
                    + 'import serene_safe_assignment' + os.linesep)


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
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep)


def init_method_check_env(node):
    return init_method_check(node)


def update_method_check_env(node):
    global PROJECT_ENVIRONMENT_NAME
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return ((py_trees.common.Status.SUCCESS) if ('
            + PROJECT_ENVIRONMENT_NAME + '.' + node.name + '(self)'
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep)


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


def resolve_variable_nondeterminism(values, range_mode, init_mode = None):
    # TODO: rework this to be more efficient.
    # currently, each possibility is computed, even though only one will be used.
    if range_mode:
        cond_func = build_range_func(values[2])
        vals = [map(str, filter(cond_func, range(handle_constant(values[0]), handle_constant(values[1]) + 1)))]
        if len(vals) == 0:
            raise Exception('variable had no valid values!')
        elif len(vals) == 1:
            return vals[0]
        else:
            return (
                'random.choice(['
                + ', '.join(vals)
                + '])'
            )
    else:
        if len(values) == 0:
            raise Exception('variable had no valid values!')
        elif len(values) == 1:
            return format_code(values[0], init_mode)
        else:
            return ('random.choice(['
                    + ', '.join([format_code(value, init_mode) for value in values])
                    + '])')


def variable_assignment(variable, variable_name, is_local, assign_value, indent_level = 2, init_mode = None):
    if init_mode is None and (variable.model_as == 'FROZENVAR' or variable.model_as == 'DEFINE'):
        raise Exception('ERROR: variable ' + variable.name + ' is a ' + variable.model_as + ' but is being updated.')
    if init_mode == 'node' and not is_local and (variable.model_as == 'FROZENVAR' or variable.model_as == 'DEFINE'):
        raise Exception('ERROR: variable ' + variable.name + ' is a ' + variable.model_as + ' but is being updated.')
    safety_1 = '' if variable.model_as == 'DEFINE' else ('serene_safe_assignment.' + variable.name + '(')
    safety_2 = '' if variable.model_as == 'DEFINE' else ')'
    return (
        indent(indent_level) + variable_name + ' = ' + safety_1 + assign_value + safety_2 + os.linesep
    )


def handle_case_result(case_results, default_result, variable, is_local, indent_level = 2, init_mode = None, override_variable_name = None):
    variable_name = (format_variable(variable, is_local, init_mode) if override_variable_name is None else override_variable_name)
    if len(case_results) == 0:
        return variable_assignment(
            variable,
            variable_name,
            is_local,
            resolve_variable_nondeterminism(default_result.values, default_result.range_mode, init_mode),
            indent_level,
            init_mode
        )
    return (
        ''.join(
            [
                (
                    (
                        (indent(indent_level) + 'elif ' + format_code(case_result.condition, init_mode) + ':' + os.linesep)
                        if index > 0
                        else
                        (indent(indent_level) + 'if ' + format_code(case_result.condition, init_mode) + ':' + os.linesep)
                    )
                    + variable_assignment(
                        variable,
                        variable_name,
                        is_local,
                        resolve_variable_nondeterminism(case_result.values, case_result.range_mode, init_mode),
                        indent_level + 1,
                        init_mode
                    )
                 ) for index, case_result in enumerate(case_results)
            ]
        )
        + indent(indent_level) + 'else:' + os.linesep
        + variable_assignment(
            variable,
            variable_name,
            is_local,
            resolve_variable_nondeterminism(default_result.values, default_result.range_mode, init_mode),
            indent_level + 1,
            init_mode
        )
    )


def handle_variable_statement(statement, indent_level = 2, init_mode = None, override_variable_name = None):
    return handle_case_result(statement.case_results, statement.default_result, statement.variable, statement.mode == 'local', indent_level, init_mode, override_variable_name)


def create_variable_macro(case_default, variable, is_local, indent_level = 2, init_mode = None):
    return (
        os.linesep
        + os.linesep
        + indent(indent_level) + 'def ' + variable.name + '():' + os.linesep
        + handle_case_result(case_default.case_results, case_default.default_result, variable, is_local, indent_level + 1, init_mode, override_variable_name = (variable.name + '_return_val'))
        + indent(indent_level + 1) + 'return ' + variable.name + '_return_val' + os.linesep
        + os.linesep
        + indent(indent_level) + format_variable_name_only(variable, is_local, init_mode) + ' = ' + variable.name + os.linesep
    )


def handle_read_statement(statement):
    global PROJECT_ENVIRONMENT_NAME
    if statement.condition_variable is not None:
        if statement.condition_variable.domain != 'BOOLEAN':
            raise Exception('Variable ' + statement.condition_variable.name + ' is being used as a condition variable but is not a boolean')
    return (
        indent(2) + 'if ' + PROJECT_ENVIRONMENT_NAME + '.' + statement.name + '__condition(self):' + os.linesep
        + (
            variable_assignment(statement.condition_variable, format_variable(statement.condition_variable, True, init_mode = None), True, 'True', indent_level = 3, init_mode = None)
            if statement.condition_variable is not None
            else
            ''
        )
        + ''.join(
            [
                (
                    variable_assignment(read_var_state.variable, format_variable(read_var_state.variable, read_var_state.mode == 'local', init_mode = None),
                                        read_var_state.mode == 'local',
                                        (
                                            PROJECT_ENVIRONMENT_NAME + '.' + statement.name + '__' + str(index) + '(self)'
                                        ),
                                        indent_level = 3, init_mode = None)
                )
                for index, read_var_state in enumerate(statement.variable_statements)
            ]
        )
        + (
            (
                indent(2) + 'else:' + os.linesep
                + variable_assignment(statement.condition_variable, format_variable(statement.condition_variable, True, init_mode = None), True, 'False', indent_level = 3, init_mode = None)
            )
            if statement.condition_variable is not None
            else
            ''
        )
    )


def handle_write_statement(statement):
    global PROJECT_ENVIRONMENT_NAME
    return (
        ''.join(
            [
                (
                    indent(2) + PROJECT_ENVIRONMENT_NAME + '.' + statement.name + '__' + str(index) + '(self)' + os.linesep
                )
                if update_env.instant
                else
                (
                    indent(2) + PROJECT_ENVIRONMENT_NAME + '.delay_this_action(' + PROJECT_ENVIRONMENT_NAME + '.' + statement.name + '__' + str(index) + ', self)' + os.linesep
                )
                for index, update_env in enumerate(statement.update)
            ]
        )
    )


def format_returns(status_result):
    return 'py_trees.common.Status.' + status_result.status.upper()


def handle_return_statement(statement):
    variable_name = 'return_status'
    if len(statement.case_results) == 0:
        return (indent(2) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
    return ((''.join(
        [
            (indent(2) + 'elif ' + format_code(case_result.condition) + ':' + os.linesep
             + (indent(3) + variable_name + ' = ' + format_returns(case_result) + os.linesep)
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
                        create_variable_macro(local_variable.initial_value, local_variable.name, True, indent_level = 2, init_mode = 'node')
                        if local_variable.model_as == 'DEFINE' else
                        handle_case_result(local_variable.initial_value.case_results, local_variable.initial_value.default_result, local_variable, True, indent_level = 2, init_mode = 'node', override_variable_name = None)
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
    global PROJECT_ENVIRONMENT_NAME
    return 'import ' + PROJECT_ENVIRONMENT_NAME + os.linesep


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
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_check_env(node)
            + update_method_check_env(node)
            )


def build_action_node(node):
    return (STANDARD_IMPORTS
            + custom_imports(node)
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_action(node)
            + update_method_action(node)
            )


def walk_tree(model):
    return walk_tree_recursive(model.root, set(), {}, '')


def walk_tree_recursive(current_node, node_names, node_names_map, running_string):
    while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
        if hasattr(current_node, 'leaf'):
            current_node = current_node.leaf
        else:
            current_node = current_node.sub_root
    # next, we get the name of this node, and correct for duplication

    new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
    node_name = new_name[0]
    modifier = new_name[1]

    node_names.add(node_name)
    node_names_map[node_name] = modifier

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    if current_node.node_type == 'check' or current_node.node_type == 'check_environment' or current_node.node_type == 'action':
        running_string += indent(1) + node_name + ' = ' + current_node.name + '_file.' + current_node.name + '(' + "'" + node_name + "'" + ')' + os.linesep
        return (node_name, node_names, node_names_map, running_string)
    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            raise Exception('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
        decorator_type = (current_node.x.capitalize()
                          + 'Is'
                          + current_node.y.capitalize())
        (child_name, node_names, node_names_map, running_string) = walk_tree_recursive(current_node.child, node_names, node_names_map, running_string)
        running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                           + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
        return (node_name, node_names, node_names_map, running_string)
    elif current_node.node_type == 'inverter':
        decorator_type = ('Inverter')
        (child_name, node_names, node_names_map, running_string) = walk_tree_recursive(current_node.child, node_names, node_names_map, running_string)
        running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                           + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
        return (node_name, node_names, node_names_map, running_string)

    # so at this point, we're in composite node territory
    children = []
    for child in current_node.children:
        (child_name, node_names, node_names_map, running_string) = walk_tree_recursive(child, node_names, node_names_map, running_string)
        children.append(child_name)
    children_names = '[' + ', '.join(children) + ']'

    if current_node.memory == 'with_true_memory':
        raise Exception('ERROR: true memory not supported in py-trees. Only partial memory is supported.')

    if current_node.node_type == 'sequence':
        running_string += (indent(1) + node_name + ' = py_trees.composites.Sequence('
                           + 'name = ' + "'" + node_name + "'"
                           + ', memory = ' + ('False' if current_node.memory == '' else 'True')
                           + ', children = ' + children_names
                           + ')' + os.linesep)
    elif current_node.node_type == 'selector':
        running_string += (indent(1) + node_name + ' = py_trees.composites.Selector('
                           + 'name = ' + "'" + node_name + "'"
                           + ', memory = ' + ('False' if current_node.memory == '' else 'True')
                           + ', children = ' + children_names
                           + ')' + os.linesep)
    elif current_node.node_type == 'parallel':
        running_string += (indent(1) + node_name + ' = py_trees.composites.Parallel('
                           + 'name = ' + "'" + node_name + "'"
                           + ', policy = py_trees.common.ParallelPolicy.'
                           + (('SuccessOnAll(' + ('False' if current_node.memory == '' else 'True') + ')') if current_node.parallel_policy == 'success_on_all' else ('SuccessOnOne()'))
                           + ', children = ' + children_names
                           + ')' + os.linesep)
    return (node_name, node_names, node_names_map, running_string)


def variable_type(variable):
    return (
        (
            'int'
            if variable.domain == 'INT'
            else
            (
                'str'
                if variable.domain == 'ENUM'
                else
                'bool'
            )
        )
        if variable.model_as == 'DEFINE'
        else
        (
            'bool'
            if variable.domain.boolean is not None
            else
            (
                (
                    'str'
                    if isinstance(handle_constant(variable.domain.enums[0]), str)
                    else
                    'int'
                )
                if variable.domain.min_val is None
                else
                'int'
            )
        )
    )


def create_safe_assignment(model):
    def conditional_for_variable(variable):
        if variable.domain.condition is not None:
            return build_range_func(variable.domain.condition)
        return None
    return_string = ''
    for variable in itertools.chain(model.blackboard_variables, model.local_variables, model.environment_variables):
        if variable.model_as == 'DEFINE':
            continue
        cur_var_type = variable_type(variable)
        return_string += (
            os.linesep
            + os.linesep
            + 'def ' + variable.name + '(new_value):' + os.linesep
            + indent(1) + 'if not isinstance(new_value, ' + cur_var_type + '):' + os.linesep
            + indent(2) + 'raise Exception(' + "'variable " + variable.name + " expected type " + cur_var_type + " but received type ' + str(type(new_value)))" + os.linesep
        )
        if variable.domain.min_val is not None:
            if variable.domain.condition is not None:
                cond_func = conditional_for_variable(variable)
                value_list = '[' + ', '.join(map(str, filter(cond_func, range(handle_constant(variable.domain.min_val), handle_constant(variable.domain.max_val) + 1)))) + ']'
                return_string += (
                    indent(1) + 'if new_value in ' + value_list
                    + ':' + os.linesep
                    + indent(2) + 'return new_value' + os.linesep
                    + indent(1) + 'else:' + os.linesep
                    + indent(2) + 'raise Exception(' + "'variable " + variable.name + " expected value in " + value_list + " but received value ' + str(new_value))" + os.linesep
                )
            else:
                return_string += (
                    indent(1) + 'if new_value >= ' + handle_constant_str(variable.domain.min_val) + ' and new_value <= ' + handle_constant_str(variable.domain.max_val) + ':' + os.linesep
                    + indent(2) + 'return new_value' + os.linesep
                    + indent(1) + 'else:' + os.linesep
                    + indent(2) + 'raise Exception(' + "'variable " + variable.name + " expected value between " + handle_constant_str(variable.domain.min_val) + " and " + handle_constant_str(variable.domain.max_val) + " inclusive but received value ' + str(new_value))" + os.linesep
                )
        elif variable.domain.boolean is not None:
            return_string += indent(1) + 'return new_value' + os.linesep
        else:
            value_list = '[' + ', '.join(map(handle_constant_str, variable.domain.enums)) + ']'
            return_string += (
                indent(1) + 'if new_value in ' + value_list
                + ':' + os.linesep
                + indent(2) + 'return new_value' + os.linesep
                + indent(1) + 'else:' + os.linesep
                + indent(2) + 'raise Exception(' + '"variable ' + variable.name + ' expected value in ' + value_list + ' but received value \'" + new_value + "\'")' + os.linesep
            )
    return return_string


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location')
    arg_parser.add_argument('name')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global PROJECT_NAME, PROJECT_ENVIRONMENT_NAME
    PROJECT_NAME = args.name
    PROJECT_ENVIRONMENT_NAME = args.name + '_environment'

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }
    validate_model(model, constants, metamodel)

    with open(args.location + 'serene_safe_assignment.py', 'w') as f:
        f.write(create_safe_assignment(model))

    for action in model.action_nodes:
        with open(args.location + action.name + '_file.py', 'w') as f:
            f.write(build_action_node(action))
    for check in model.check_nodes:
        with open(args.location + check.name + '_file.py', 'w') as f:
            f.write(build_check_node(check))
    for check_env in model.environment_checks:
        with open(args.location + check_env.name + '_file.py', 'w') as f:
            f.write(build_check_environment_node(check_env))

    (root_name, _, _, running_string) = walk_tree(model)

    with open(args.location + PROJECT_NAME + '.py', 'w') as f:
        f.write(''.join([('import ' + node.name + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
                + 'import py_trees' + os.linesep
                + 'import serene_safe_assignment' + os.linesep
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
                            create_variable_macro(blackboard_variable.initial_value, blackboard_variable, False, indent_level = 1, init_mode = 'blackboard')
                            if blackboard_variable.model_as == 'DEFINE' else
                            handle_case_result(blackboard_variable.initial_value.case_results, blackboard_variable.initial_value.default_result, blackboard_variable, False, indent_level = 1, init_mode = 'blackboard', override_variable_name = None)
                        )
                        for blackboard_variable in model.blackboard_variables
                    ]
                )
                + os.linesep
                + running_string
                + indent(1) + 'return ' + root_name + os.linesep
                )
    dsl_to_environment.write_environment(model, args.location, PROJECT_NAME)
    return


if __name__ == '__main__':
    main()
