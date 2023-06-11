import argparse
import os
# import sys
import itertools
import textx
from behaverify_common import indent, create_node_name
# import serene_functions
# import dsl_to_environment
from check_model import (validate_model
                         # , constant_type
                         , variable_type
                         , is_local
                         , is_env
                         , is_blackboard
                         # , variable_scope
                         , is_array
                         , build_range_func)


# RANGE_FUNCTION = {
#     'abs' : serene_functions.serene_abs,
#     'max' : serene_functions.serene_max,
#     'min' : serene_functions.serene_min,
#     'sin' : serene_functions.serene_sin,
#     'cos' : serene_functions.serene_cos,
#     'tan' : serene_functions.serene_tan,
#     'ln' : serene_functions.serene_log,
#     'not' : serene_functions.serene_not,
#     'and' : serene_functions.serene_and,
#     'or' : serene_functions.serene_or,
#     'xor' : serene_functions.serene_xor,
#     'xnor' : serene_functions.serene_xnor,
#     'implies' : serene_functions.serene_implies,
#     'equivalent' : serene_functions.serene_eq,
#     'equal' : serene_functions.serene_eq,
#     'not_equal' : serene_functions.serene_ne,
#     'less_than' : serene_functions.serene_lt,
#     'greater_than' : serene_functions.serene_gt,
#     'less_than_or_equal' : serene_functions.serene_lte,
#     'greater_than_or_equal' : serene_functions.serene_gte,
#     'negative' : serene_functions.serene_neg,
#     'addition' : serene_functions.serene_sum,
#     'subtraction' : serene_functions.serene_sub,
#     'multiplication' : serene_functions.serene_mult,
#     'division' : serene_functions.serene_truediv,
#     'mod' : serene_functions.serene_mod,
#     'count' : serene_functions.serene_count
# }


# todo: replace is_local, is_env, by setting metamodel to a global constant and then using textx_isinstance


def format_function_before(function_name, code, init_mode):
    return (
        function_name + '('
        + ', '.join([format_code(value, init_mode) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, init_mode):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, init_mode) for value in code.function_call.values])
        + ')'
        )


def format_function_implies(_, code, init_mode):
    return (
        '('
        + '(not (' + format_code(code.function_call.values[0], init_mode) + '))'
        + ' or '
        + '(' + format_code(code.function_call.values[1], init_mode) + ')'
        + ')'
    )


def format_function_xnor(_, code, init_mode):
    return (
        '('
        + 'not (' + FUNCTION_FORMAT['xor'][1](FUNCTION_FORMAT['xor'][0], code, init_mode) + ')'
        + ')'
    )


def format_function_count(_, code, init_mode):
    return (
        '('
        + '[' + ', '.join([format_code(value, init_mode) for value in code.function_call.values]) + '].count(True)'
        + ')'
        )


def format_function_index(_, code, init_mode):
    return (
        (format_variable_name_only(code.function_call.variable, init_mode) + '(' + format_code(code.function_call.values[0], init_mode) + ')')
        if code.function_call.variable.model_as == 'DEFINE'
        else
        (format_variable(code.function_call.variable, init_mode) + '[' + format_code(code.function_call.values[0], init_mode) + ']')
    )


FUNCTION_FORMAT = {
    'abs' : ('abs', format_function_before),
    'max' : ('max', format_function_before),
    'min' : ('min', format_function_before),
    'sin' : ('math.sin', format_function_before),
    'cos' : ('math.cos', format_function_before),
    'tan' : ('math.tan', format_function_before),
    'ln' : ('math.log', format_function_before),
    'not' : ('not ', format_function_before),  # space intentionally added here.
    'and' : ('and', format_function_between),
    'or' : ('or', format_function_between),
    'xor' : ('^', format_function_between),
    'xnor' : ('xnor', format_function_xnor),
    'implies' : ('->', format_function_implies),
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
    'division' : ('//', format_function_between),
    'mod' : ('%', format_function_between),
    'count' : ('count', format_function_count),
    'index' : ('index', format_function_index)
}


def format_variable_name_only(variable, init_mode):
    global env_mode
    if env_mode:
        return ((('') if is_local(variable) else ('blackboard.' if not is_env(variable) else 'self.')) + variable.name)
    return (
        (
            ('blackboard_reader.')
            if init_mode == 'blackboard' else
            ('self.' + ('' if is_local(variable) else 'blackboard.'))
        )
        + variable.name
    )


def format_variable(variable, init_mode):
    global env_mode
    if env_mode:
        return (
            (
                'node.'
                if is_local(variable)
                else
                (
                    'self.'
                    if is_env(variable)
                    else
                    'self.blackboard.'
                )
            )
            + variable.name
            + ('()' if variable.model_as == 'DEFINE' else '')
        )
    return (
        (
            ('blackboard_reader.')
            if init_mode == 'blackboard' else
            ('self.' + ('' if is_local(variable) else 'blackboard.'))
        )
        + variable.name
        + ('()' if variable.model_as == 'DEFINE' else '')
    )


def format_code(code, init_mode):
    return (
        (
            handle_constant_str(code.constant) if code.constant is not None else (
                format_variable(code.variable, init_mode) if code.variable is not None else (
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


STANDARD_IMPORTS = ('import py_trees' + os.linesep
                    + 'import math' + os.linesep
                    + 'import operator' + os.linesep
                    + 'import random' + os.linesep
                    + 'import serene_safe_assignment' + os.linesep)


def class_definition(node_name):
    return ('class ' + node_name + '(py_trees.behaviour.Behaviour):' + os.linesep)


def init_method_check(node, serene_print):
    return (indent(1) + 'def __init__(self, name):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + (
                (indent(2) + "self.__serene_print__ = 'INVALID'" + os.linesep)
                if serene_print
                else
                ''
            )
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + os.linesep)


def update_method_check(node, serene_print):
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return_status = ((py_trees.common.Status.SUCCESS) if ('
            + format_code(node.condition, 'node')
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep
            + (
                (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                if serene_print
                else
                ''
            )
            + indent(2) + 'return return_status' + os.linesep)


def init_method_check_env(node, serene_print):
    return (indent(1) + 'def __init__(self, name, environment):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + (
                (indent(2) + "self.__serene_print__ = 'INVALID'" + os.linesep)
                if serene_print
                else
                ''
            )
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.environment = environment' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + os.linesep)


def update_method_check_env(node, serene_print):
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return_status = ((py_trees.common.Status.SUCCESS) if ('
            + 'self.environment.' + node.name + '(self)'
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep
            + (
                (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                if serene_print
                else
                ''
            )
            + indent(2) + 'return return_status' + os.linesep)


def resolve_variable_nondeterminism(values, range_mode, init_mode):
    # TODO: rework this to be more efficient.
    # currently, each possibility is computed, even though only one will be used.
    if range_mode:
        cond_func = build_range_func(values[2])
        vals = list(map(str, filter(cond_func, range(handle_constant(values[0]), handle_constant(values[1]) + 1))))
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


def variable_assignment(variable, assign_value, indent_level, init_mode, array_mode):
    # if init_mode is None and (variable.model_as == 'FROZENVAR' or variable.model_as == 'DEFINE'):
    #     raise Exception('ERROR: variable ' + variable.name + ' is a ' + variable.model_as + ' but is being updated.')
    # if init_mode == 'node' and not is_local and (variable.model_as == 'FROZENVAR' or variable.model_as == 'DEFINE'):
    #     raise Exception('ERROR: variable ' + variable.name + ' is a ' + variable.model_as + ' but is being updated.')
    # these checks are being handled in check_model
    safety_1 = '' if variable.model_as == 'DEFINE' else ('serene_safe_assignment.' + variable.name + '(')
    safety_2 = '' if variable.model_as == 'DEFINE' else ')'
    return (
        (
            indent(indent_level) + '__temp_var__ = ' + safety_1 + assign_value + safety_2 + os.linesep
            + indent(indent_level) + 'for (index, val) in __temp_var__:' + os.linesep
            + indent(indent_level + 1) + format_variable_name_only(variable, init_mode) + '[index] = val' + os.linesep
        )
        if array_mode
        else
        (indent(indent_level) + format_variable_name_only(variable, init_mode) + ' = ' + safety_1 + assign_value + safety_2 + os.linesep)
    )


def handle_assign(assign, indent_level, init_mode):
    case_results = assign.case_results
    default_result = assign.default_result
    if len(case_results) == 0:
        return resolve_variable_nondeterminism(default_result.values, default_result.range_mode, init_mode)  # NOTE: no linesep at the end!
    return (
        '(' + os.linesep
        + ''.join(
            [
                (
                    indent(indent_level + 1 + index)
                    + resolve_variable_nondeterminism(case_result.values, case_result.range_mode, init_mode) + os.linesep
                    + indent(indent_level + 1 + index) + 'if ' + format_code(case_result.condition, init_mode) + ' else' + os.linesep
                    + indent(indent_level + 1 + index) + '(' + os.linesep
                 ) for index, case_result in enumerate(case_results)
            ]
        )
        + indent(indent_level + len(case_results))
        + resolve_variable_nondeterminism(default_result.values, default_result.range_mode, init_mode) + os.linesep
        + indent(indent_level) + (')' * (1 + len(case_results)))  # NOTE: no linesep at the end!
    )


def handle_variable_statement(statement, assign_var, indent_level, init_mode, assign_to_var):
    # assign_var = statement.variable
    if is_array(assign_var):
        global constants
        assign_string = []
        if statement.array_mode == 'range':
            serene_indices = []
            if init_mode is not None or len(statement.values) == 0:
                serene_indices = list(range(handle_constant(assign_var.array_size)))
            else:
                cond_func = build_range_func(statement.values[2])
                min_val = handle_constant(statement.values[0])
                max_val = handle_constant(statement.values[1])
                serene_indices = list(filter(cond_func, range(min_val, max_val + 1)))
            for index in serene_indices:
                constants['serene_index'] = index
                array_index = (
                    (
                        handle_constant_str(statement.assign.index_expr)
                        if statement.constant_index == 'constant_index'
                        else
                        format_code(statement.assign.index_expr, init_mode)
                    )
                    if init_mode is None
                    else
                    str(index)
                )
                assign_string.append(
                    (array_index
                     , handle_assign(statement.assign.assign if init_mode is None else statement.assign, indent_level, init_mode))
                )
            constants.pop('serene_index')
        else:
            for index, assign in enumerate(statement.assigns):
                array_index = (
                    (
                        handle_constant_str(assign.index_expr)
                        if statement.constant_index == 'constant_index'
                        else
                        format_code(assign.index_expr, init_mode)
                    )
                    if init_mode is None
                    else
                    str(index)
                )
                assign_string.append(
                    (array_index
                     , handle_assign(assign.assign if init_mode is None else assign, indent_level, init_mode))
                )
        if assign_to_var:
            return variable_assignment(
                assign_var
                , ('[' + ', '.join(map(lambda x : '(' + x[0] + ', ' + x[1] + ')', assign_string)) + ']')
                , indent_level
                , init_mode
                , array_mode = True
            )
        return ('[' + ', '.join(map(lambda x : '(' + x[0] + ', ' + x[1] + ')', assign_string)) + ']')
    else:
        if assign_to_var:
            return variable_assignment(
                assign_var
                , handle_assign(statement.assign, indent_level = indent_level, init_mode = init_mode)
                , indent_level
                , init_mode
                , array_mode = False
            )
        return handle_assign(statement.assign, indent_level = indent_level, init_mode = init_mode)


def create_variable_macro(assign, range_mode, variable, indent_level, init_mode):
    if is_array(variable):
        case_string = ''
        if range_mode:
            global constants
            for index in range(handle_constant(handle_constant(variable.array_size))):
                constants['serene_index'] = index
                case_string += (
                    indent(indent_level + 1) + ('if' if index == 0 else 'elif') + ' index == ' + str(index) + ':' + os.linesep
                    + indent(indent_level + 2) + 'return ' + handle_assign(assign, indent_level + 2, init_mode) + os.linesep
                )
            constants.pop('serene_index')
        else:
            assign_list = assign
            for index, assign in enumerate(assign_list):
                case_string += (
                    indent(indent_level + 1) + ('if' if index == 0 else 'elif') + ' index == ' + str(index) + ':' + os.linesep
                    + indent(indent_level + 2) + 'return ' + handle_assign(assign, indent_level + 2, init_mode) + os.linesep
                )
        return (
            os.linesep
            + os.linesep
            + indent(indent_level) + 'def ' + variable.name + '(index):' + os.linesep
            + indent(indent_level + 1) + 'if not isinstance(index, int):' + os.linesep
            + indent(indent_level + 2) + "raise Exception('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
            + indent(indent_level + 1) + 'if index < 0 or index >= ' + handle_constant_str(variable.array_size) + ':' + os.linesep
            + indent(indent_level + 2) + "raise Exception('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
            + case_string
            + indent(indent_level + 1) + "raise Exception('Reached unreachable state when accessing " + variable.name + ": ' + str(index))" + os.linesep
            + os.linesep
            + indent(indent_level) + format_variable_name_only(variable, init_mode) + ' = ' + variable.name + os.linesep
        )
    else:
        return (
            os.linesep
            + os.linesep
            + indent(indent_level) + 'def ' + variable.name + '():' + os.linesep
            + indent(indent_level + 1) + 'return ' + handle_assign(assign, indent_level + 1, init_mode) + os.linesep
            + os.linesep
            + indent(indent_level) + format_variable_name_only(variable, init_mode) + ' = ' + variable.name + os.linesep
        )
    return


def handle_read_statement(statement, indent_level, init_mode):
    return (
        indent(indent_level) + 'if ' + 'self.environment.' + statement.name + '__condition(self):' + os.linesep
        + (
            variable_assignment(statement.condition_variable
                                , ('[(' + (format_code(statement.index_of, init_mode) if statement.is_const == 'index_of' else handle_constant_str(statement.is_const)) + ', True)]') if is_array(statement.condition_variable) else 'True'
                                , indent_level = indent_level + 1
                                , init_mode = init_mode
                                , array_mode = is_array(statement.condition_variable))
            if statement.condition_variable is not None
            else
            ''
        )
        + ''.join(
            [
                (
                    variable_assignment(read_var_state.variable
                                        , ('self.environment.' + statement.name + '__' + str(index) + '(self)')
                                        , indent_level = indent_level + 1
                                        , init_mode = init_mode
                                        , array_mode = is_array(read_var_state.variable))
                )
                for index, read_var_state in enumerate(statement.variable_statements)
            ]
        )
        + (
            (
                indent(2) + 'else:' + os.linesep
                + variable_assignment(statement.condition_variable
                                      , ('[(' + format_code(statement.index_of, init_mode) + ', False)]') if is_array(statement.condition_variable) else 'True'
                                      , indent_level = indent_level + 1
                                      , init_mode = init_mode
                                      , array_mode = is_array(statement.condition_variable))
            )
            if statement.condition_variable is not None
            else
            ''
        )
    )


def handle_write_statement(statement, indent_level):
    return (
        ''.join(
            [
                (
                    indent(indent_level) + 'self.environment.' + statement.name + '__' + str(index) + '(self)' + os.linesep
                )
                if update_env.instant
                else
                (
                    indent(indent_level) + 'self.environment.delay_this_action(' + 'self.environment.' + statement.name + '__' + str(index) + ', self)' + os.linesep
                )
                for index, update_env in enumerate(statement.update)
            ]
        )
    )


def format_returns(status_result):
    return 'py_trees.common.Status.' + status_result.status.upper()


def handle_return_statement(statement, indent_level):
    variable_name = 'return_status'
    if len(statement.case_results) == 0:
        return (indent(indent_level) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
    return ((''.join(
        [
            (indent(indent_level) + 'elif ' + format_code(case_result.condition, None) + ':' + os.linesep
             + (indent(indent_level + 1) + variable_name + ' = ' + format_returns(case_result) + os.linesep)
             ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(indent_level) + 'else:' + os.linesep
               + indent(indent_level + 1) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
            )


def init_method_action(node, serene_print):
    return (indent(1) + 'def __init__(self, name, environment):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + (
                (indent(2) + "self.__serene_print__ = 'INVALID'" + os.linesep)
                if serene_print
                else
                ''
            )
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.environment = environment' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.WRITE)' + os.linesep) for variable in node.write_variables])
            + ''.join(
                [
                    (
                        (indent(2) + format_variable_name_only(local_variable, 'node') + ' = [None] * ' + handle_constant_str(local_variable.array_size) + os.linesep)
                        if is_array(local_variable)
                        else
                        ''
                    )
                    for local_variable in node.local_variables
                ]
            )
            + ''.join(
                [
                    (
                        create_variable_macro(local_variable.assigns if len(local_variable.assigns) > 0 else local_variable.assign
                                              , (local_variable.array_mode == 'range')
                                              , local_variable
                                              , indent_level = 2
                                              , init_mode = 'node')
                        if local_variable.model_as == 'DEFINE' else
                        handle_variable_statement(local_variable, local_variable, indent_level = 2, init_mode = 'node', assign_to_var = True)
                    )
                    for local_variable in node.local_variables if local_variable not in
                    [
                        statement.variable for statement in node.init_statements
                    ]
                ]
            )
            + ''.join([handle_variable_statement(statement, statement.variable, indent_level = 2, init_mode = 'node', assign_to_var = True) for statement in node.init_statements])
            + os.linesep)


def handle_statement(statement, indent_level, init_mode, assign_to_var):
    return (
        handle_variable_statement(statement.variable_statement, statement.variable_statement.variable, indent_level, init_mode, assign_to_var) if statement.variable_statement is not None else (
            handle_read_statement(statement.read_statement, indent_level, init_mode) if statement.read_statement is not None else (
                handle_write_statement(statement.write_statement, indent_level)
                )
            )
        )


def update_method_action(node, serene_print):
    return (indent(1) + 'def update(self):' + os.linesep
            + ''.join([handle_statement(statement, indent_level = 2, init_mode = None, assign_to_var = True) for statement in node.pre_update_statements])
            + handle_return_statement(node.return_statement, indent_level = 2)
            + (
                (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                if serene_print
                else
                ''
            )
            + ''.join([handle_statement(statement, indent_level = 2, init_mode = None, assign_to_var = True) for statement in node.post_update_statements])
            + indent(2) + 'return return_status' + os.linesep
            )


# def custom_imports(node):
#     global PROJECT_ENVIRONMENT_NAME
#     return 'import ' + PROJECT_ENVIRONMENT_NAME + os.linesep


def build_check_node(node, serene_print):
    return (STANDARD_IMPORTS
            # + custom_imports(node)
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_check(node, serene_print)
            + update_method_check(node, serene_print)
            )


def build_check_environment_node(node, serene_print):
    return (STANDARD_IMPORTS
            # + custom_imports(node)
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_check_env(node, serene_print)
            + update_method_check_env(node, serene_print)
            )


def build_action_node(node, serene_print):
    return (STANDARD_IMPORTS
            # + custom_imports(node)
            + os.linesep
            + os.linesep
            + class_definition(node.name)
            + init_method_action(node, serene_print)
            + update_method_action(node, serene_print)
            )


def walk_tree(model, serene_print):
    return walk_tree_recursive(model.root, serene_print, set(), {}, '', {})


def walk_tree_recursive(current_node, serene_print, node_names, node_names_map, running_string, variable_print_info):
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
        running_string += indent(1) + node_name + ' = ' + current_node.name + '_file.' + current_node.name + '(' + "'" + node_name + "'" + ('' if current_node.node_type == 'check' else ', environment') + ')' + os.linesep
        if current_node.node_type == 'action':
            variable_print_info[node_name] = current_node.local_variables
        return (node_name, node_names, node_names_map, running_string, variable_print_info)
    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            raise Exception('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
        decorator_type = (current_node.x.capitalize()
                          + 'Is'
                          + current_node.y.capitalize())
        (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(current_node.child, serene_print, node_names, node_names_map, running_string, variable_print_info)
        running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                           + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
        if serene_print:
            running_string += (indent(1) + node_name + '.tick = decorator_better_tick.__get__(' + node_name + ', py_trees.decorators.Decorator)' + os.linesep)
        return (node_name, node_names, node_names_map, running_string, variable_print_info)
    elif current_node.node_type == 'inverter':
        decorator_type = ('Inverter')
        (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(current_node.child, serene_print, node_names, node_names_map, running_string, variable_print_info)
        running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                           + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
        if serene_print:
            running_string += (indent(1) + node_name + '.tick = decorator_better_tick.__get__(' + node_name + ', py_trees.decorators.Decorator)' + os.linesep)
        return (node_name, node_names, node_names_map, running_string, variable_print_info)

    # so at this point, we're in composite node territory
    children = []
    for child in current_node.children:
        (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(child, serene_print, node_names, node_names_map, running_string, variable_print_info)
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
        if serene_print:
            running_string += (indent(1) + node_name + '.tick = sequence_better_tick.__get__(' + node_name + ', py_trees.composites.Sequence)' + os.linesep)
    elif current_node.node_type == 'selector':
        running_string += (indent(1) + node_name + ' = py_trees.composites.Selector('
                           + 'name = ' + "'" + node_name + "'"
                           + ', memory = ' + ('False' if current_node.memory == '' else 'True')
                           + ', children = ' + children_names
                           + ')' + os.linesep)
        if serene_print:
            running_string += (indent(1) + node_name + '.tick = selector_better_tick.__get__(' + node_name + ', py_trees.composites.Selector)' + os.linesep)
    elif current_node.node_type == 'parallel':
        running_string += (indent(1) + node_name + ' = py_trees.composites.Parallel('
                           + 'name = ' + "'" + node_name + "'"
                           + ', policy = py_trees.common.ParallelPolicy.'
                           + (('SuccessOnAll(' + ('False' if current_node.memory == '' else 'True') + ')') if current_node.parallel_policy == 'success_on_all' else ('SuccessOnOne()'))
                           + ', children = ' + children_names
                           + ')' + os.linesep)
        if serene_print:
            running_string += (indent(1) + node_name + '.tick = parallel_better_tick.__get__(' + node_name + ', py_trees.composites.Parallel)' + os.linesep)
    return (node_name, node_names, node_names_map, running_string, variable_print_info)


def create_safe_assignment(model):
    def conditional_for_variable(variable):
        if variable.domain.condition is not None:
            return build_range_func(variable.domain.condition)
        return None

    def create_type_check_function(variable, function_name, indent_level):
        cur_var_type = variable_type(variable)
        cur_var_type = ('int' if cur_var_type == 'INT'
                        else ('bool' if cur_var_type == 'BOOLEAN'
                              else ('str')))
        return_string = (
            indent(indent_level) + 'def ' + function_name + '(new_value):' + os.linesep
            + indent(indent_level + 1) + 'if not isinstance(new_value, ' + cur_var_type + '):' + os.linesep
            + indent(indent_level + 2) + 'raise Exception(' + "'variable " + variable.name + " expected type " + cur_var_type + " but received type ' + str(type(new_value)))" + os.linesep
        )
        if variable.domain.min_val is not None:
            if variable.domain.condition is not None:
                cond_func = conditional_for_variable(variable)
                value_list = '[' + ', '.join(map(str, filter(cond_func, range(handle_constant(variable.domain.min_val), handle_constant(variable.domain.max_val) + 1)))) + ']'
                return_string += (
                    indent(indent_level + 1) + 'if new_value in ' + value_list
                    + ':' + os.linesep
                    + indent(indent_level + 2) + 'return new_value' + os.linesep
                    + indent(indent_level + 1) + 'else:' + os.linesep
                    + indent(indent_level + 2) + 'raise Exception(' + "'variable " + variable.name + " expected value in " + value_list + " but received value ' + str(new_value))" + os.linesep
                )
            else:
                return_string += (
                    indent(indent_level + 1) + 'if new_value >= ' + handle_constant_str(variable.domain.min_val) + ' and new_value <= ' + handle_constant_str(variable.domain.max_val) + ':' + os.linesep
                    + indent(indent_level + 2) + 'return new_value' + os.linesep
                    + indent(indent_level + 1) + 'else:' + os.linesep
                    + indent(indent_level + 2) + 'raise Exception(' + "'variable " + variable.name + " expected value between " + handle_constant_str(variable.domain.min_val) + " and " + handle_constant_str(variable.domain.max_val) + " inclusive but received value ' + str(new_value))" + os.linesep
                )
        elif variable.domain.boolean is not None:
            return_string += indent(indent_level + 1) + 'return new_value' + os.linesep
        else:
            value_list = '[' + ', '.join(map(handle_constant_str, variable.domain.enums)) + ']'
            return_string += (
                indent(indent_level + 1) + 'if new_value in ' + value_list
                + ':' + os.linesep
                + indent(indent_level + 2) + 'return new_value' + os.linesep
                + indent(indent_level + 1) + 'else:' + os.linesep
                + indent(indent_level + 2) + 'raise Exception(' + '"variable ' + variable.name + ' expected value in ' + value_list + ' but received value \'" + new_value + "\'")' + os.linesep
            )
        return return_string
    outter_return_string = ''
    for variable in model.variables:
        if variable.model_as == 'DEFINE':
            continue
        outter_return_string += os.linesep + os.linesep
        if is_array(variable):
            outter_return_string += (
                'def ' + variable.name + '(new_values):' + os.linesep
                + create_type_check_function(variable, variable.name + '__internal_type_check', 1)
                + os.linesep
                + indent(1) + 'return_pairs = []' + os.linesep
                + indent(1) + 'seen_indices = set()' + os.linesep
                + indent(1) + 'for (index, new_value) in new_values:' + os.linesep
                + indent(2) + 'if not isinstance(index, int):' + os.linesep
                + indent(3) + "raise Exception('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
                + indent(2) + 'if index < 0 or index >= ' + handle_constant_str(variable.array_size) + ':' + os.linesep
                + indent(3) + "raise Exception('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
                + indent(2) + 'checked_value = ' + variable.name + '__internal_type_check(new_value)' + os.linesep
                + indent(2) + 'if index not in seen_indices:' + os.linesep
                + indent(3) + 'seen_indices.add(index)' + os.linesep
                + indent(3) + 'return_pairs.append((index, checked_value))' + os.linesep
                + indent(1) + 'return return_pairs' + os.linesep
            )
        else:
            outter_return_string += create_type_check_function(variable, variable.name, 0)
    return outter_return_string


def create_runner(blackboard_variables, environment_variables, local_print_info, max_iter, serene_print, no_var_print, py_tree_print):
    global PROJECT_NAME, PROJECT_ENVIRONMENT_NAME

    def map_local_to_info(local_var):
        return (
            '{\'name\' : \'' + local_var.name + '\''
            + ', \'is_func\' : ' + str(local_var.model_as == 'DEFINE')
            + ', \'array_size\' : ' + str(local_var.array_size) + '}'
        )
    return (
        'import os' + os.linesep
        + 'import py_trees' + os.linesep
        + 'import ' + PROJECT_NAME + os.linesep
        + 'import ' + PROJECT_ENVIRONMENT_NAME + os.linesep
        + os.linesep
        + 'blackboard_reader = ' + PROJECT_NAME + '.create_blackboard()' + os.linesep
        + 'environment = ' + PROJECT_ENVIRONMENT_NAME + '.' + PROJECT_ENVIRONMENT_NAME + '(blackboard_reader)' + os.linesep
        + 'root = ' + PROJECT_NAME + '.create_tree(environment)' + os.linesep
        + 'tree = py_trees.trees.BehaviourTree(root)' + os.linesep
        + (
            (
                'visualizer = py_trees.visitors.DisplaySnapshotVisitor()' + os.linesep
                + 'tree.add_visitor(visualizer)' + os.linesep
            )
            if py_tree_print
            else
            ''
        )
        + os.linesep
        + os.linesep
        + 'def full_tick():' + os.linesep
        + indent(1) + 'environment.pre_tick_environment_update()' + os.linesep
        + indent(1) + 'tree.tick()' + os.linesep
        + indent(1) + 'environment.execute_delayed_action_queue()' + os.linesep
        + indent(1) + 'environment.post_tick_environment_update()' + os.linesep
        + indent(1) + 'return' + os.linesep
        + os.linesep
        + os.linesep
        + (
            ''
            if no_var_print
            else
            (
                'def print_blackboard():' + os.linesep
                + indent(1) + 'ret_string = \'blackboard\' + os.linesep' + os.linesep
                + ''.join(
                    [
                        (
                            (
                                indent(1) + 'ret_string += indent(1) + \'' + variable.name + ': \' + str([blackboard_reader.' + variable.name
                                + '(x) for x in range(' + handle_constant_str(variable.array_size) + ')]) + os.linesep' + os.linesep
                            )
                            if variable.model_as == 'DEFINE' and is_array(variable)
                            else
                            (
                                indent(1) + 'ret_string += indent(1) + \'' + variable.name + ': \' + str(blackboard_reader.' + variable.name
                                + ('()' if variable.model_as == 'DEFINE' else '')
                                + ') + os.linesep' + os.linesep
                            )
                        )
                        for variable in blackboard_variables
                    ]
                )
                + indent(1) + 'return ret_string' + os.linesep
                + os.linesep
                + os.linesep
                + 'def print_environment():' + os.linesep
                + indent(1) + 'ret_string = \'environment\' + os.linesep' + os.linesep
                + ''.join(
                    [
                        (
                            (
                                indent(1) + 'ret_string += indent(1) + \'' + variable.name + ': \' + str([environment.' + variable.name
                                + '(x) for x in range(' + handle_constant_str(variable.array_size) + ')]) + os.linesep' + os.linesep
                            )
                            if variable.model_as == 'DEFINE' and is_array(variable)
                            else
                            (
                                indent(1) + 'ret_string += indent(1) + \'' + variable.name + ': \' + str(environment.' + variable.name
                                + ('()' if variable.model_as == 'DEFINE' else '')
                                + ') + os.linesep' + os.linesep
                            )
                        )
                        for variable in environment_variables
                    ]
                )
                + indent(1) + 'return ret_string' + os.linesep
                + os.linesep
                + os.linesep
                + 'node_to_locals = {' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '\'' + node_name + '\' : ['
                         + ', '.join(map(map_local_to_info, local_vars))
                         + '],' + os.linesep)
                        for (node_name, local_vars) in local_print_info.items()
                    ]
                )
                + '}' + os.linesep
                + os.linesep
                + os.linesep
                + 'def print_local_in_node(node, local_var):' + os.linesep
                + indent(1) + 'var_attr = getattr(node, local_var[\'name\'])' + os.linesep
                + indent(1) + 'if not local_var[\'is_func\']:' + os.linesep
                + indent(2) + 'return indent(1) + node.name + \'_DOT_\' + local_var[\'name\'] + \' : \' + str(var_attr) + os.linesep' + os.linesep
                + indent(1) + 'if local_var[\'array_size\'] is None:' + os.linesep
                + indent(2) + 'return indent(1) + node.name + \'_DOT_\' + local_var[\'name\'] + \' : \' + str(var_attr()) + os.linesep' + os.linesep
                + indent(1) + 'return indent(1) + node.name + \'_DOT_\' + local_var[\'name\'] + \' : [\' + \', \'.join(map(var_attr, range(local_var[\'array_size\'] - 1))) + \']\''
                + os.linesep
                + os.linesep
                + 'def print_locals_in_node(node, local_vars):' + os.linesep
                + indent(1) + "return ''.join(map(lambda var: print_local_in_node(node, var), local_vars))" + os.linesep
                + os.linesep
                + os.linesep
                + 'def _print_local_(node):' + os.linesep
                + indent(1) + 'if node.name in node_to_locals:' + os.linesep
                + indent(2) + 'return print_locals_in_node(node, node_to_locals[node.name])' + os.linesep
                + indent(1) + 'return \'\'.join(map(_print_local_, node.children))' + os.linesep
                + os.linesep
                + os.linesep
                + 'def print_local():' + os.linesep
                + indent(1) + 'return \'local\' + os.linesep + _print_local_(root)' + os.linesep
            )
        )
        + os.linesep
        + os.linesep
        + (
            (
                'def indent(n):' + os.linesep
                + indent(1) + "return '  '*n" + os.linesep
                + os.linesep
                + os.linesep
                + 'def tree_printer(node, indent_level):' + os.linesep
                + indent(1) + 'return (' + os.linesep
                + indent(2) + "indent(indent_level) + node.name + ' -> ' + node.__serene_print__ + os.linesep" + os.linesep
                + indent(2) + "+ ''.join(map(lambda child: tree_printer(child, indent_level + 1), node.children))" + os.linesep
                + indent(1) + ')' + os.linesep
                + os.linesep
                + os.linesep
                + 'def reset_serene_tree_print(node):' + os.linesep
                + indent(1) + "node.__serene_print__ = 'INVALID'" + os.linesep
                + indent(1) + 'for child in node.children:' + os.linesep
                + indent(2) + 'reset_serene_tree_print(child)' + os.linesep
                + indent(1) + 'return' + os.linesep
            )
            if serene_print
            else
            ''
        )
        + os.linesep
        + os.linesep
        + 'for count in range(' + str(max_iter) + '):' + os.linesep
        + indent(1) + "print('------------------------')" + os.linesep
        + indent(1) + "print('State after tick: ' + str(count + 1))" + os.linesep
        + indent(1) + 'if environment.check_tick_condition():' + os.linesep
        + (
            (indent(2) + 'reset_serene_tree_print(root)' + os.linesep)
            if serene_print
            else
            ''
        )
        + indent(2) + 'full_tick()' + os.linesep
        + (
            (indent(2) + 'print(tree_printer(root, 0))' + os.linesep)
            if serene_print
            else
            ''
        )
        + indent(2) + 'print(print_blackboard())' + os.linesep
        + indent(2) + 'print(print_local())' + os.linesep
        + indent(2) + 'print(print_environment())' + os.linesep
        + indent(1) + 'else:' + os.linesep
        + indent(2) + "print('after ' + str(count) + ' ticks, tick_condition no longer holds. Printing blackboard and environment, then exiting')" + os.linesep
        + indent(2) + 'print(print_blackboard())' + os.linesep
        + indent(2) + 'print(print_local())' + os.linesep
        + indent(2) + 'print(print_environment())' + os.linesep
        + indent(2) + 'break' + os.linesep
    )


def write_environment(model, location, const_name):
    global PROJECT_NAME, PROJECT_ENVIRONMENT_NAME, constants, env_mode
    env_mode = True

    def env_handle_check_env(node):
        return (
            os.linesep
            + indent(1) + 'def '
            + node.name
            + '(self, node):' + os.linesep
            + indent(2) + "'''" + os.linesep
            + indent(2) + '-- RETURN' + os.linesep
            + indent(2) + 'This method is expected to return True or False.' + os.linesep
            + indent(2) + 'This method is being modeled using the following behavior:' + os.linesep
            + indent(2) + format_code(node.condition, init_mode = None) + os.linesep
            + indent(2) + '-- SIDE EFFECTS' + os.linesep
            + indent(2) + 'This method is expected to have no side effects (for the tree).' + os.linesep
            + indent(2) + "'''" + os.linesep
            + indent(2) + '# below we include an auto generated attempt at implmenting this' + os.linesep
            + indent(2) + 'return ' + format_code(node.condition, init_mode = None) + os.linesep
        )

    def env_handle_read_statement(statement):
        return (
            os.linesep
            + indent(1) + 'def ' + statement.name + '__condition(self, node):' + os.linesep
            + indent(2) + 'if ' + format_code(statement.condition, init_mode = None) + ':' + os.linesep
            + indent(3) + 'return '
            + (
                'random.choice([True, False])'
                if statement.non_determinism
                else
                'True'
            ) + os.linesep
            + indent(2) + 'else:' + os.linesep
            + indent(3) + 'return False' + os.linesep
            + os.linesep
            + ''.join(
                [
                    (
                        os.linesep
                        + indent(1) + 'def ' + statement.name + '__' + str(index) + '(self, node):' + os.linesep
                        + indent(2) + 'return ' + handle_variable_statement(read_var_state, read_var_state.variable, 2, None, False) + os.linesep
                    )
                    for index, read_var_state in enumerate(statement.variable_statements)
                ]
            )
        )

    def env_handle_write_statement(statement):
        return (
            ''.join(
                [
                    (
                        os.linesep
                        + indent(1) + 'def ' + statement.name + '__' + str(index) + '(self, node):' + os.linesep
                        + handle_variable_statement(env_update, env_update.variable, indent_level = 2, init_mode = None, assign_to_var = True)
                        + indent(2) + 'return' + os.linesep
                    )
                    for index, env_update in enumerate(statement.update)
                ]
            )
        )

    to_write = (
        'import random' + os.linesep
        + 'import serene_safe_assignment' + os.linesep
        + os.linesep
        + os.linesep
        + 'class ' + PROJECT_ENVIRONMENT_NAME + '():' + os.linesep
        + indent(1) + 'def delay_this_action(self, action, node):' + os.linesep
        + indent(2) + 'self.delayed_action_queue.append((action, node))' + os.linesep
        + os.linesep
        + indent(1) + 'def execute_delayed_action_queue(self):' + os.linesep
        + indent(2) + 'for (delayed_action, node) in self.delayed_action_queue:' + os.linesep
        + indent(3) + 'delayed_action(node)' + os.linesep
        + indent(2) + 'self.delayed_action_queue = []' + os.linesep
        + indent(2) + 'return' + os.linesep
        + os.linesep
        + indent(1) + 'def pre_tick_environment_update(self):' + os.linesep
        + ''.join(
            [
                handle_variable_statement(update, update.variable, indent_level = 2, init_mode = None, assign_to_var = True)
                for update in model.update if update.instant
            ]
        )
        + indent(2) + 'return' + os.linesep
        + os.linesep
        + indent(1) + 'def post_tick_environment_update(self):' + os.linesep
        + ''.join(
            [
                handle_variable_statement(update, update.variable, indent_level = 2, init_mode = None, assign_to_var = True)
                for update in model.update if not update.instant
            ]
        )
        + indent(2) + 'return' + os.linesep
        + os.linesep
        + indent(1) + 'def check_tick_condition(self):' + os.linesep
        + (
            (indent(2) + 'return True' + os.linesep)
            if model.tick_condition is None
            else
            (indent(2) + 'return ' + format_code(model.tick_condition, None) + os.linesep)
        )
        + os.linesep
        + indent(1) + 'def __init__(self, blackboard):' + os.linesep
        + indent(2) + 'self.blackboard = blackboard' + os.linesep
        + indent(2) + 'self.delayed_action_queue = []' + os.linesep
        + (os.linesep if any(map(is_env, model.variables)) else '')
        + ''.join(
            [
                create_variable_macro(variable.assigns if len(variable.assigns) > 0 else variable.assign
                                      , variable.array_mode == 'range'
                                      , variable
                                      , indent_level = 2
                                      , init_mode = 'environment')
                for variable in model.variables if is_env(variable) and variable.model_as == 'DEFINE'
            ]
        )
        + ''.join(
            [
                (
                    ((indent(2) + format_variable(variable, 'environment') + ' = [None] * ' + handle_constant_str(variable.array_size) + os.linesep)
                     if is_array(variable)
                     else
                     '')
                    + handle_variable_statement(variable, variable, indent_level = 2, init_mode = 'environment', assign_to_var = True)
                )
                for variable in model.variables if is_env(variable) and variable.model_as != 'DEFINE'
            ]
        )
    )

    for check_env in model.environment_checks:
        to_write += env_handle_check_env(check_env)

    # todo: below is probably wrong. fix it. likely uses methods incorrectly.
    for action in model.action_nodes:
        for statement in itertools.chain(action.pre_update_statements, action.post_update_statements):
            if statement.variable_statement is not None:
                continue
            to_write += (
                env_handle_read_statement(statement.read_statement)
                if statement.read_statement is not None else
                env_handle_write_statement(statement.write_statement))

    with open(location + PROJECT_ENVIRONMENT_NAME + '.py', 'w') as f:
        f.write(to_write)
    return


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location')
    arg_parser.add_argument('name')
    arg_parser.add_argument('--max_iter', default = 100)
    arg_parser.add_argument('--no_var_print', action = 'store_true')
    arg_parser.add_argument('--serene_print', action = 'store_true')
    arg_parser.add_argument('--py_tree_print', action = 'store_true')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global PROJECT_NAME, PROJECT_ENVIRONMENT_NAME, constants, env_mode
    PROJECT_NAME = args.name
    PROJECT_ENVIRONMENT_NAME = args.name + '_environment'
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }
    env_mode = False
    validate_model(model, constants, metamodel)

    with open(args.location + 'serene_safe_assignment.py', 'w') as f:
        f.write(create_safe_assignment(model))

    for action in model.action_nodes:
        with open(args.location + action.name + '_file.py', 'w') as f:
            f.write(build_action_node(action, args.serene_print))
    for check in model.check_nodes:
        with open(args.location + check.name + '_file.py', 'w') as f:
            f.write(build_check_node(check, args.serene_print))
    for check_env in model.environment_checks:
        with open(args.location + check_env.name + '_file.py', 'w') as f:
            f.write(build_check_environment_node(check_env, args.serene_print))

    (root_name, _, _, running_string, local_print_info) = walk_tree(model, args.serene_print)

    if args.serene_print:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/tick_overwrite/tick_overwrite.py', 'r') as f:
            better_ticks = f.read()

    with open(args.location + PROJECT_NAME + '.py', 'w') as f:
        f.write(''.join([('import ' + node.name + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
                + 'import py_trees' + os.linesep
                + 'import serene_safe_assignment' + os.linesep
                + os.linesep + os.linesep
                + 'def create_blackboard():' + os.linesep
                + indent(1) + 'blackboard_reader = py_trees.blackboard.Client()' + os.linesep
                + ''.join(
                    [
                        (indent(1) + 'blackboard_reader.register_key(key = ' + "'" + blackboard_variable.name + "'" + ', access = py_trees.common.Access.WRITE)' + os.linesep)
                        for blackboard_variable in model.variables if is_blackboard(blackboard_variable)
                    ]
                )
                + ''.join(
                    [
                        (
                            (
                                (indent(1) + format_variable_name_only(variable, 'blackboard') + ' = [None] * ' + handle_constant_str(variable.array_size) + os.linesep)
                                if is_array(variable)
                                else
                                ''
                            )
                            +
                            (
                                create_variable_macro(variable.assigns if len(variable.assigns) > 0 else variable.assign
                                                      , variable.array_mode == 'range'
                                                      , variable
                                                      , indent_level = 1
                                                      , init_mode = 'blackboard')
                                if variable.model_as == 'DEFINE' else
                                handle_variable_statement(variable, variable, indent_level = 1, init_mode = 'blackboard', assign_to_var = True)
                            )
                        )
                        for variable in model.variables if is_blackboard(variable)
                    ]
                )
                + indent(1) + 'return blackboard_reader' + os.linesep
                + (
                    better_ticks
                    if args.serene_print
                    else
                    ''
                )
                + os.linesep
                + os.linesep
                + 'def create_tree(environment):' + os.linesep
                + running_string
                + indent(1) + 'return ' + root_name + os.linesep
                )
    write_environment(model, args.location, PROJECT_NAME)
    with open(args.location + PROJECT_NAME + '_runner.py', 'w') as f:
        f.write(create_runner(list(filter(is_blackboard, model.variables)), list(filter(is_env, model.variables)), local_print_info, args.max_iter, args.serene_print, args.no_var_print, args.py_tree_print))
    return


if __name__ == '__main__':
    main()
