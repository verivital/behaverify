'''
This module is for internal use with BehaVerify.
It is used to convert .tree files to Python code.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2023-09-22
'''
import argparse
import os
import itertools
import textx
from behaverify_common import indent, create_node_name
from check_model import (validate_model,
                         variable_type,
                         is_local,
                         is_env,
                         is_blackboard,
                         is_array,
                         build_range_func)


def write_files(metamodel_file, model_file, main_name, write_location, serene_print, max_iter, no_var_print, py_tree_print):
    '''
    Used to write all the files.
    @metamodel_file ::> points to the file with the metamodel
    @model_file ::> points to the file with the model
    @main_name ::> main name to be used for files
    @write_location ::> where to write files
    @serene_print ::> boolean, should we use custom printing?
    @max_iter ::> how many iterations
    @no_var_print ::> turns off printing vars
    @py_tree_print ::> turns on PyTree printing
    '''

    # format_mode variable explained
    # format_mode is a dict {'init' : init, 'loc' : loc).
    # init is a boolean. if true, it means we are initializing. if false, we are not.
    # loc is a location. location can be node, blackboard, or environment.

    def format_function_before(function_name, code, format_mode):
        return (
            function_name + '('
            + ', '.join([format_code(value, format_mode) for value in code.function_call.values])
            + ')'
            )

    def format_function_between(function_name, code, format_mode):
        return (
            '('
            + (' ' + function_name + ' ').join([format_code(value, format_mode) for value in code.function_call.values])
            + ')'
            )

    def format_function_implies(_, code, format_mode):
        return (
            '('
            + '(not (' + format_code(code.function_call.values[0], format_mode) + '))'
            + ' or '
            + '(' + format_code(code.function_call.values[1], format_mode) + ')'
            + ')'
        )

    def format_function_division(_, code, format_mode):
        return (
            '(int('
            + '(' + format_code(code.function_call.values[0], format_mode) + ')'
            + '/ '
            + '(' + format_code(code.function_call.values[1], format_mode) + ')'
            + '))'
        )

    def format_function_xnor(_, code, format_mode):
        return (
            '('
            + 'not (' + function_format['xor'][1](function_format['xor'][0], code, format_mode) + ')'
            + ')'
        )

    def format_function_count(_, code, format_mode):
        return (
            '('
            + '[' + ', '.join([format_code(value, format_mode) for value in code.function_call.values]) + '].count(True)'
            + ')'
            )

    def format_function_index(_, code, format_mode):
        return (
            (format_variable_name_only(code.function_call.variable, format_mode) + '(' + format_code(code.function_call.values[0], format_mode) + ')')
            if code.function_call.variable.model_as == 'DEFINE'
            else
            (format_variable_name_only(code.function_call.variable, format_mode) + '[serene_safe_assignment.index_func(' + format_code(code.function_call.values[0], format_mode) + ', ' + handle_constant_str(code.function_call.variable.array_size) + ')]')
            # (format_variable_name_only(code.function_call.variable, format_mode) + '[' + format_code(code.function_call.values[0], format_mode) + ']')
        )

    def format_variable_name_only(variable, format_mode):
        return (
            (
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
            )
            if format_mode['loc'] == 'environment'
            else
            (
                (
                    ('blackboard_reader.')
                    if format_mode['loc'] == 'blackboard' else
                    ('self.' + ('' if is_local(variable) else 'blackboard.'))
                )
                + variable.name
            )
        )

    def format_variable(variable, format_mode):
        return format_variable_name_only(variable, format_mode) + ('()' if variable.model_as == 'DEFINE' else '')

    def format_code(code, format_mode):
        return (
            (
                handle_constant_str(code.constant) if code.constant is not None else (
                    format_variable(code.variable, format_mode) if code.variable is not None else (
                        ('(' + format_code(code.code_statement, format_mode) + ')') if code.code_statement is not None else (
                            function_format[code.function_call.function_name][1](function_format[code.function_call.function_name][0], code, format_mode)
                        )
                    )
                )
            )
        )

    def handle_constant(constant):
        if constant in argument_pairs:
            return argument_pairs[constant]
        return (constants['serene_index'][-1] if constant == 'serene_index' else (constants[constant] if constant in constants else constant))

    def handle_constant_str(constant):
        if constant in argument_pairs:
            return argument_pairs[constant]
        new_constant = handle_constant(constant)
        return (("'" + new_constant + "'") if isinstance(new_constant, str) else str(new_constant))

    def class_definition(node_name):
        return 'class ' + node_name + '(py_trees.behaviour.Behaviour):' + os.linesep

    def init_method_check(node):
        return (indent(1) + 'def __init__(self, name' + ((', ' + ', '.join(map(lambda arg_pair: arg_pair.argument_name, node.arguments))) if len(node.arguments) > 0 else '') + '):' + os.linesep
                + ''.join(
                    [
                        (indent(2) + 'self.' + arg_pair.argument_name + ' = ' + arg_pair.argument_name + os.linesep)
                        for arg_pair in node.arguments
                    ]
                )
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

    def update_method_check(node):
        return (indent(1) + 'def update(self):' + os.linesep
                + indent(2) + 'return_status = ((py_trees.common.Status.SUCCESS) if ('
                + format_code(node.condition, format_mode = {'init': False, 'loc' : 'node'})
                + ') else (py_trees.common.Status.FAILURE))' + os.linesep
                + (
                    (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                    if serene_print
                    else
                    ''
                )
                + indent(2) + 'return return_status' + os.linesep)

    def init_method_environment_check(node):
        return (indent(1) + 'def __init__(self, name, environment' + ((', ' + ', '.join(map(lambda arg_pair: arg_pair.argument_name, node.arguments))) if len(node.arguments) > 0 else '') + '):' + os.linesep
                + ''.join(
                    [
                        (indent(2) + 'self.' + arg_pair.argument_name + ' = ' + arg_pair.argument_name + os.linesep)
                        for arg_pair in node.arguments
                    ]
                )
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

    def update_method_environment_check(node):
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

    def resolve_variable_nondeterminism(values, range_mode, format_mode):
        # TODO: rework this to be more efficient.
        # currently, each possibility is computed, even though only one will be used.
        if range_mode:
            cond_func = build_range_func(values[2], constants)
            vals = list(map(str, filter(cond_func, range(handle_constant(values[0]), handle_constant(values[1]) + 1))))
            if len(vals) == 0:
                raise ValueError('variable had no valid values!')
            if len(vals) == 1:
                return vals[0]
            return (
                'random.choice(['
                + ', '.join(vals)
                + '])'
            )
        if len(values) == 0:
            raise ValueError('variable had no valid values!')
        if len(values) == 1:
            return format_code(values[0], format_mode)
        return ('random.choice([' + ', '.join([format_code(value, format_mode) for value in values]) + '])')

    def variable_assignment(variable, assign_value, indent_level, format_mode, array_mode):
        safety_1 = '' if variable.model_as == 'DEFINE' else ('serene_safe_assignment.' + variable.name + '(')
        safety_2 = '' if variable.model_as == 'DEFINE' else ')'
        return (
            (
                indent(indent_level) + '__temp_var__ = ' + safety_1 + assign_value + safety_2 + os.linesep
                + indent(indent_level) + 'for (index, val) in __temp_var__:' + os.linesep
                + indent(indent_level + 1) + format_variable_name_only(variable, format_mode) + '[index] = val' + os.linesep
            )
            if array_mode
            else
            (indent(indent_level) + format_variable_name_only(variable, format_mode) + ' = ' + safety_1 + assign_value + safety_2 + os.linesep)
        )

    def handle_assign(assign, indent_level, format_mode):
        case_results = assign.case_results
        default_result = assign.default_result
        if len(case_results) == 0:
            return resolve_variable_nondeterminism(default_result.values, default_result.range_mode, format_mode)  # NOTE: no linesep at the end!
        return (
            '(' + os.linesep
            + ''.join(
                [
                    (
                        indent(indent_level + 1 + index)
                        + resolve_variable_nondeterminism(case_result.values, case_result.range_mode, format_mode) + os.linesep
                        + indent(indent_level + 1 + index) + 'if ' + format_code(case_result.condition, format_mode) + ' else' + os.linesep
                        + indent(indent_level + 1 + index) + '(' + os.linesep
                     ) for index, case_result in enumerate(case_results)
                ]
            )
            + indent(indent_level + len(case_results))
            + resolve_variable_nondeterminism(default_result.values, default_result.range_mode, format_mode) + os.linesep
            + indent(indent_level) + (')' * (1 + len(case_results)))  # NOTE: no linesep at the end!
        )

    def handle_variable_statement(statement, assign_var, indent_level, format_mode, assign_to_var):
        if is_array(assign_var):
            assign_string = []
            if statement.array_mode == 'range':
                serene_indices = []
                if format_mode['init'] or len(statement.values) == 0:
                    serene_indices = list(range(handle_constant(assign_var.array_size)))
                else:
                    cond_func = build_range_func(statement.values[2], constants)
                    min_val = handle_constant(statement.values[0])
                    max_val = handle_constant(statement.values[1])
                    serene_indices = list(filter(cond_func, range(min_val, max_val + 1)))
                for index in serene_indices:
                    constants['serene_index'].append(index)
                    array_index = (
                        str(index)
                        if format_mode['init']
                        else
                        (
                            handle_constant_str(statement.assign.index_expr)
                            if statement.constant_index == 'constant_index'
                            else
                            format_code(statement.assign.index_expr, format_mode)
                        )
                    )
                    assign_string.append(
                        (array_index
                         , handle_assign(statement.assign if format_mode['init'] else statement.assign.assign, indent_level, format_mode))
                    )
                    constants['serene_index'].pop()
            else:
                for index, assign in enumerate(statement.assigns):
                    array_index = (
                        str(index)
                        if format_mode['init']
                        else
                        (
                            handle_constant_str(assign.index_expr)
                            if statement.constant_index == 'constant_index'
                            else
                            format_code(assign.index_expr, format_mode)
                        )
                    )
                    assign_string.append(
                        (array_index
                         , handle_assign(assign if format_mode['init'] else assign.assign, indent_level, format_mode))
                    )
            if assign_to_var:
                return variable_assignment(
                    assign_var
                    , ('[' + ', '.join(map(lambda x : '(' + x[0] + ', ' + x[1] + ')', assign_string)) + ']')
                    , indent_level
                    , format_mode
                    , array_mode = True
                )
            return '[' + ', '.join(map(lambda x : '(' + x[0] + ', ' + x[1] + ')', assign_string)) + ']'
        if assign_to_var:
            return variable_assignment(
                assign_var
                , handle_assign(statement.assign, indent_level = indent_level, format_mode = format_mode)
                , indent_level
                , format_mode
                , array_mode = False
            )
        return handle_assign(statement.assign, indent_level = indent_level, format_mode = format_mode)

    def create_variable_macro(assign, range_mode, variable, indent_level, format_mode):
        if is_array(variable):
            case_string = ''
            if range_mode:
                for index in range(handle_constant(handle_constant(variable.array_size))):
                    constants['serene_index'].append(index)
                    case_string += (
                        indent(indent_level + 1) + ('if' if index == 0 else 'elif') + ' index == ' + str(index) + ':' + os.linesep
                        + indent(indent_level + 2) + 'return ' + handle_assign(assign, indent_level + 2, format_mode) + os.linesep
                    )
                    constants['serene_index'].pop()
            else:
                assign_list = assign
                for index, assign_ in enumerate(assign_list):
                    case_string += (
                        indent(indent_level + 1) + ('if' if index == 0 else 'elif') + ' index == ' + str(index) + ':' + os.linesep
                        + indent(indent_level + 2) + 'return ' + handle_assign(assign_, indent_level + 2, format_mode) + os.linesep
                    )
            return (
                os.linesep
                + os.linesep
                + indent(indent_level) + 'def ' + variable.name + '(index):' + os.linesep
                + indent(indent_level + 1) + 'if type(index) is not int:' + os.linesep
                + indent(indent_level + 2) + "raise TypeError('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
                + indent(indent_level + 1) + 'if index < 0 or index >= ' + handle_constant_str(variable.array_size) + ':' + os.linesep
                + indent(indent_level + 2) + "raise ValueError('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
                + case_string
                + indent(indent_level + 1) + "raise RuntimeError('Reached unreachable state when accessing " + variable.name + ": ' + str(index))" + os.linesep
                + os.linesep
                + indent(indent_level) + format_variable_name_only(variable, format_mode) + ' = ' + variable.name + os.linesep
            )
        return (
            os.linesep
            + os.linesep
            + indent(indent_level) + 'def ' + variable.name + '():' + os.linesep
            + indent(indent_level + 1) + 'return ' + handle_assign(assign, indent_level + 1, format_mode) + os.linesep
            + os.linesep
            + indent(indent_level) + format_variable_name_only(variable, format_mode) + ' = ' + variable.name + os.linesep
        )

    def handle_read_statement(statement, indent_level, format_mode):
        return (
            indent(indent_level) + 'if ' + 'self.environment.' + statement.name + '__condition(self):' + os.linesep
            + (
                variable_assignment(statement.condition_variable
                                    , ('[(' + (format_code(statement.index_of, format_mode) if statement.is_const == 'index_of' else handle_constant_str(statement.is_const)) + ', True)]') if is_array(statement.condition_variable) else 'True'
                                    , indent_level = indent_level + 1
                                    , format_mode = format_mode
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
                                            , format_mode = format_mode
                                            , array_mode = is_array(read_var_state.variable))
                    )
                    for index, read_var_state in enumerate(statement.variable_statements)
                ]
            )
            + (
                (
                    indent(2) + 'else:' + os.linesep
                    + variable_assignment(statement.condition_variable
                                          , ('[(' + format_code(statement.index_of, format_mode) + ', False)]') if is_array(statement.condition_variable) else 'True'
                                          , indent_level = indent_level + 1
                                          , format_mode = format_mode
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
            return indent(indent_level) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep
        return ((''.join(
            [
                (indent(indent_level) + 'elif ' + format_code(case_result.condition, format_mode = {'init' : False, 'loc' : 'node'}) + ':' + os.linesep
                 + (indent(indent_level + 1) + variable_name + ' = ' + format_returns(case_result) + os.linesep)
                 ) for case_result in statement.case_results])).replace('elif', 'if', 1)
                + (indent(indent_level) + 'else:' + os.linesep
                   + indent(indent_level + 1) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
                )

    def init_method_action(node):
        return (indent(1) + 'def __init__(self, name, environment' + ((', ' + ', '.join(map(lambda arg_pair: arg_pair.argument_name, node.arguments))) if len(node.arguments) > 0 else '') + '):' + os.linesep
                + ''.join(
                    [
                        (indent(2) + 'self.' + arg_pair.argument_name + ' = ' + arg_pair.argument_name + os.linesep)
                        for arg_pair in node.arguments
                    ]
                )
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
                            (indent(2) + format_variable_name_only(local_variable, format_mode = {'init': True, 'loc': 'node'}) + ' = [None] * ' + handle_constant_str(local_variable.array_size) + os.linesep)
                            if is_array(local_variable)
                            else
                            ''
                        )
                        for local_variable in node.local_variables if local_variable.model_as != 'DEFINE'  # no need to initialize an empty array for define variables.
                    ]
                )
                + ''.join(
                    [
                        (
                            create_variable_macro(local_variable.assigns if len(local_variable.assigns) > 0 else local_variable.assign
                                                  , (local_variable.array_mode == 'range')
                                                  , local_variable
                                                  , indent_level = 2
                                                  , format_mode = {'init': True, 'loc' : 'node'})
                            if local_variable.model_as == 'DEFINE' else
                            handle_variable_statement(local_variable, local_variable, indent_level = 2, format_mode = {'init': True, 'loc' : 'node'}, assign_to_var = True)
                        )
                        for local_variable in node.local_variables if local_variable not in
                        [
                            statement.variable for statement in node.init_statements
                        ]
                    ]
                )
                + ''.join(
                    [
                        (
                            create_variable_macro(statement.assigns if len(statement.assigns) > 0 else statement.assign
                                                  , (statement.array_mode == 'range')
                                                  , statement.variable
                                                  , indent_level = 2
                                                  , format_mode = {'init': True, 'loc' : 'node'})
                            if statement.variable.model_as == 'DEFINE' else
                            handle_variable_statement(statement, statement.variable, indent_level = 2, format_mode = {'init': True, 'loc' : 'node'}, assign_to_var = True)
                        )
                        for statement in node.init_statements
                    ]
                )
                + os.linesep)

    def handle_statement(statement, indent_level, format_mode, assign_to_var):
        return (
            handle_variable_statement(statement.variable_statement, statement.variable_statement.variable, indent_level, format_mode, assign_to_var) if statement.variable_statement is not None else (
                handle_read_statement(statement.read_statement, indent_level, format_mode) if statement.read_statement is not None else (
                    handle_write_statement(statement.write_statement, indent_level)
                    )
                )
            )

    def update_method_action(node):
        return (indent(1) + 'def update(self):' + os.linesep
                + ''.join([handle_statement(statement, indent_level = 2, format_mode = {'init': False, 'loc' : 'node'}, assign_to_var = True) for statement in node.pre_update_statements])
                + handle_return_statement(node.return_statement, indent_level = 2)
                + (
                    (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                    if serene_print
                    else
                    ''
                )
                + ''.join([handle_statement(statement, indent_level = 2, format_mode = {'init': False, 'loc' : 'node'}, assign_to_var = True) for statement in node.post_update_statements])
                + indent(2) + 'return return_status' + os.linesep
                )

    def build_check_node(node):
        return (standard_imports
                + os.linesep
                + os.linesep
                + class_definition(node.name)
                + init_method_check(node)
                + update_method_check(node)
                )

    def build_environment_check_node(node):
        return (standard_imports
                + os.linesep
                + os.linesep
                + class_definition(node.name)
                + init_method_environment_check(node)
                + update_method_environment_check(node)
                )

    def build_action_node(node):
        return (standard_imports
                + os.linesep
                + os.linesep
                + class_definition(node.name)
                + init_method_action(node)
                + update_method_action(node)
                )

    def walk_tree_recursive(current_node, node_names, node_names_map, running_string, variable_print_info):
        while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
            if hasattr(current_node, 'leaf'):
                arguments = current_node.arguments
                current_node = current_node.leaf
            else:
                current_node = current_node.sub_root
        # next, we get the name of this node, and correct for duplication
        new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        node_names.add(node_name)
        node_names_map[node_name] = modifier

        if current_node.node_type in ('check', 'environment_check', 'action'):
            running_string += (indent(1) + node_name + ' = ' + current_node.name + '_file.' + current_node.name + '(' + "'" + node_name + "'"
                               + ('' if current_node.node_type == 'check' else ', environment')
                               + ((', ' + ', '.join(map(handle_constant_str, arguments))) if len(arguments) > 0 else '')
                               + ')' + os.linesep)
            if current_node.node_type == 'action':
                variable_print_info[node_name] = current_node.local_variables
            return (node_name, node_names, node_names_map, running_string, variable_print_info)
        if current_node.node_type == 'X_is_Y':
            if current_node.x == current_node.y:
                raise ValueError('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            decorator_type = (current_node.x.capitalize()
                              + 'Is'
                              + current_node.y.capitalize())
            (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(current_node.child, node_names, node_names_map, running_string, variable_print_info)
            running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                               + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
            if serene_print:
                running_string += (indent(1) + node_name + '.tick = decorator_better_tick.__get__(' + node_name + ', py_trees.decorators.Decorator)' + os.linesep)
            return (node_name, node_names, node_names_map, running_string, variable_print_info)
        if current_node.node_type == 'inverter':
            decorator_type = 'Inverter'
            (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(current_node.child, node_names, node_names_map, running_string, variable_print_info)
            running_string += (indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                               + 'name = ' + "'" + node_name + "'" + ', child = ' + child_name + ')' + os.linesep)
            if serene_print:
                running_string += (indent(1) + node_name + '.tick = decorator_better_tick.__get__(' + node_name + ', py_trees.decorators.Decorator)' + os.linesep)
            return (node_name, node_names, node_names_map, running_string, variable_print_info)

        # so at this point, we're in composite node territory
        children = []
        for child in current_node.children:
            (child_name, node_names, node_names_map, running_string, variable_print_info) = walk_tree_recursive(child, node_names, node_names_map, running_string, variable_print_info)
            children.append(child_name)
        children_names = '[' + ', '.join(children) + ']'

        if current_node.memory == 'with_true_memory':
            raise NotImplementedError('ERROR: true memory not supported in PyTrees. Only partial memory is supported.')

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
                return build_range_func(variable.domain.condition, constants)
            return None

        def create_type_check_function(variable, function_name, indent_level):
            cur_var_type = variable_type(variable, constants)
            cur_var_type = ('int' if cur_var_type == 'INT'
                            else ('bool' if cur_var_type == 'BOOLEAN'
                                  else ('str')))
            return_string = (
                indent(indent_level) + 'def ' + function_name + '(new_value):' + os.linesep
                + indent(indent_level + 1) + 'if type(new_value) is not ' + cur_var_type + ':' + os.linesep
                + indent(indent_level + 2) + 'raise TypeError(' + "'variable " + variable.name + " expected type " + cur_var_type + " but received type ' + str(type(new_value)))" + os.linesep
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
                        + indent(indent_level + 2) + 'raise ValueError(' + "'variable " + variable.name + " expected value in " + value_list + " but received value ' + str(new_value))" + os.linesep
                    )
                else:
                    return_string += (
                        indent(indent_level + 1) + 'if new_value >= ' + handle_constant_str(variable.domain.min_val) + ' and new_value <= ' + handle_constant_str(variable.domain.max_val) + ':' + os.linesep
                        + indent(indent_level + 2) + 'return new_value' + os.linesep
                        + indent(indent_level + 1) + 'else:' + os.linesep
                        + indent(indent_level + 2) + 'raise ValueError(' + "'variable " + variable.name + " expected value between " + handle_constant_str(variable.domain.min_val) + " and " + handle_constant_str(variable.domain.max_val) + " inclusive but received value ' + str(new_value))" + os.linesep
                    )
            elif variable.domain.boolean is not None or variable.domain.true_int is not None:
                return_string += indent(indent_level + 1) + 'return new_value' + os.linesep
            else:
                value_list = '[' + ', '.join(map(handle_constant_str, variable.domain.enums)) + ']'
                return_string += (
                    indent(indent_level + 1) + 'if new_value in ' + value_list
                    + ':' + os.linesep
                    + indent(indent_level + 2) + 'return new_value' + os.linesep
                    + indent(indent_level + 1) + 'else:' + os.linesep
                    + indent(indent_level + 2) + 'raise ValueError(' + '"variable ' + variable.name + ' expected value in ' + value_list + ' but received value \'" + new_value + "\'")' + os.linesep
                )
            return return_string
        outter_return_string = (
            # 'class SereneAssignmentException(Exception):' + os.linesep
            # + indent(1) + 'def __init__(self, message):' + os.linesep
            # + indent(2) + 'super().__init__(message)' + os.linesep
            # + os.linesep
            # + os.linesep
            'def index_func(index, array_size):' + os.linesep
            + indent(1) + 'if type(index) is not int:' + os.linesep
            + indent(2) + 'raise TypeError(\'Array index must be an int\')' + os.linesep
            + indent(1) + 'if index < 0 or index >= array_size:' + os.linesep
            + indent(2) + 'raise ValueError(\'Array index out of bounds\')' + os.linesep
            + indent(1) + 'return index' + os.linesep
            # + indent(1) + 'return max(0, min(array_size - 1, index))' + os.linesep
            + os.linesep
        )
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
                    + indent(2) + 'if type(index) is not int:' + os.linesep
                    + indent(3) + "raise ValueError('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
                    + indent(2) + 'if index < 0 or index >= ' + handle_constant_str(variable.array_size) + ':' + os.linesep
                    + indent(3) + "raise ValueError('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
                    + indent(2) + 'checked_value = ' + variable.name + '__internal_type_check(new_value)' + os.linesep
                    + indent(2) + 'if index not in seen_indices:' + os.linesep
                    + indent(3) + 'seen_indices.add(index)' + os.linesep
                    + indent(3) + 'return_pairs.append((index, checked_value))' + os.linesep
                    + indent(1) + 'return return_pairs' + os.linesep
                )
            else:
                outter_return_string += create_type_check_function(variable, variable.name, 0)
        return outter_return_string

    def create_runner(blackboard_variables, environment_variables, local_print_info):
        def map_local_to_info(local_var):
            return (
                '{\'name\' : \'' + local_var.name + '\''
                + ', \'is_func\' : ' + str(local_var.model_as == 'DEFINE')
                + ', \'array_size\' : ' + str(local_var.array_size) + '}'
            )
        return (
            'import os' + os.linesep
            + 'import py_trees' + os.linesep
            + 'import ' + project_name + os.linesep
            + 'import ' + project_environment_name + os.linesep
            + os.linesep
            + 'blackboard_reader = ' + project_name + '.create_blackboard()' + os.linesep
            + 'environment = ' + project_environment_name + '.' + project_environment_name + '(blackboard_reader)' + os.linesep
            + 'root = ' + project_name + '.create_tree(environment)' + os.linesep
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
                    + indent(1) + 'return indent(1) + node.name + \'_DOT_\' + local_var[\'name\'] + \' : [\' + \', \'.join(map(str, map(var_attr, range(local_var[\'array_size\'] - 1)))) + \']\' + os.linesep'
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
            + 'def indent(n):' + os.linesep
            + indent(1) + "return '  '*n" + os.linesep
            + os.linesep
            + os.linesep
            + (
                (
                    'def tree_printer(node, indent_level):' + os.linesep
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
            + "print('------------------------')" + os.linesep
            + "print('Initial State')" + os.linesep
            + 'print(print_blackboard())' + os.linesep
            + 'print(print_local())' + os.linesep
            + 'print(print_environment())' + os.linesep
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

    def write_environment(model):
        def env_handle_environment_check(node):
            return (
                os.linesep
                + indent(1) + 'def '
                + node.name
                + '(self, node):' + os.linesep
                + indent(2) + "'''" + os.linesep
                + indent(2) + '-- RETURN' + os.linesep
                + indent(2) + 'This method is expected to return True or False.' + os.linesep
                + indent(2) + 'This method is being modeled using the following behavior:' + os.linesep
                + indent(2) + format_code(node.condition, format_mode = {'init': False, 'loc' : 'environment'}) + os.linesep
                + indent(2) + '-- SIDE EFFECTS' + os.linesep
                + indent(2) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(2) + "'''" + os.linesep
                + indent(2) + '# below we include an auto generated attempt at implmenting this' + os.linesep
                + indent(2) + 'return ' + format_code(node.condition, format_mode = {'init': False, 'loc' : 'environment'}) + os.linesep
            )

        def env_handle_read_statement(statement):
            return (
                os.linesep
                + indent(1) + 'def ' + statement.name + '__condition(self, node):' + os.linesep
                + indent(2) + 'if ' + format_code(statement.condition, format_mode = {'init': False, 'loc' : 'environment'}) + ':' + os.linesep
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
                            + indent(2) + 'return ' + handle_variable_statement(read_var_state, read_var_state.variable, 2, format_mode = {'init': False, 'loc' : 'environment'}, assign_to_var = False) + os.linesep
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
                            + handle_variable_statement(env_update, env_update.variable, indent_level = 2, format_mode = {'init': False, 'loc' : 'environment'}, assign_to_var = True)
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
            + 'class ' + project_environment_name + '():' + os.linesep
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
                    handle_variable_statement(update, update.variable, indent_level = 2, format_mode = {'init': False, 'loc' : 'environment'}, assign_to_var = True)
                    for update in model.update if update.instant
                ]
            )
            + indent(2) + 'return' + os.linesep
            + os.linesep
            + indent(1) + 'def post_tick_environment_update(self):' + os.linesep
            + ''.join(
                [
                    handle_variable_statement(update, update.variable, indent_level = 2, format_mode = {'init': False, 'loc' : 'environment'}, assign_to_var = True)
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
                (indent(2) + 'return ' + format_code(model.tick_condition, format_mode = {'init': False, 'loc' : 'environment'}) + os.linesep)
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
                                          , format_mode = {'init': True, 'loc' : 'environment'})
                    for variable in model.variables if is_env(variable) and variable.model_as == 'DEFINE'
                ]
            )
            + ''.join(
                [
                    (
                        ((indent(2) + format_variable(variable, format_mode = {'init': True, 'loc' : 'environment'}) + ' = [None] * ' + handle_constant_str(variable.array_size) + os.linesep)
                         if is_array(variable)
                         else
                         '')
                        + handle_variable_statement(variable, variable, indent_level = 2, format_mode = {'init': True, 'loc' : 'environment'}, assign_to_var = True)
                    )
                    for variable in model.variables if is_env(variable) and variable.model_as != 'DEFINE'
                ]
            )
        )
        nonlocal argument_pairs
        for environment_check in model.environment_checks:
            argument_pairs = {arg_pair.argument_name: 'node.' + arg_pair.argument_name for arg_pair in environment_check.arguments}
            to_write += env_handle_environment_check(environment_check)
            argument_pairs = {}
        for action in model.action_nodes:
            argument_pairs = {arg_pair.argument_name: 'node.' + arg_pair.argument_name for arg_pair in action.arguments}
            for statement in itertools.chain(action.pre_update_statements, action.post_update_statements):
                if statement.variable_statement is not None:
                    continue
                to_write += (
                    env_handle_read_statement(statement.read_statement)
                    if statement.read_statement is not None else
                    env_handle_write_statement(statement.write_statement))
            argument_pairs = {}
        return to_write

    function_format = {
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
        'imply' : ('->', format_function_implies),
        'equiv' : ('==', format_function_between),
        'equal' : ('==', format_function_between),
        'neq' : ('!=', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('<=', format_function_between),
        'gte' : ('>=', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('*', format_function_between),
        # 'division' : ('//', format_function_between),  # this rounds to negative infinity, we want rounds to 0.
        'idiv' : ('division', format_function_division),
        'mod' : ('%', format_function_between),
        'rdiv' : ('/', format_function_between),
        'floor' : ('math.floor', format_function_before),
        'count' : ('count', format_function_count),
        'index' : ('index', format_function_index)
    }
    standard_imports = ('import py_trees' + os.linesep
                        + 'import math' + os.linesep
                        + 'import operator' + os.linesep
                        + 'import random' + os.linesep
                        + 'import serene_safe_assignment' + os.linesep)

    metamodel = textx.metamodel_from_file(metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(model_file)

    project_name = main_name
    project_environment_name = main_name + '_environment'
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }
    argument_pairs = {}
    validate_model(model, constants)
    constants['serene_index'] = []

    with open(write_location + 'serene_safe_assignment.py', 'w', encoding = 'utf-8') as write_file:
        write_file.write(create_safe_assignment(model))  # checked. No additional information required.

    for action in model.action_nodes:
        argument_pairs = {arg_pair.argument_name: 'self.' + arg_pair.argument_name for arg_pair in action.arguments}
        with open(write_location + action.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_action_node(action))
        argument_pairs = {}
    for check in model.check_nodes:
        argument_pairs = {arg_pair.argument_name: 'self.' + arg_pair.argument_name for arg_pair in check.arguments}
        with open(write_location + check.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_check_node(check))
        argument_pairs = {}
    for environment_check in model.environment_checks:
        argument_pairs = {arg_pair.argument_name: 'self.' + arg_pair.argument_name for arg_pair in environment_check.arguments}
        with open(write_location + environment_check.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_environment_check_node(environment_check))
        argument_pairs = {}

    (root_name, _, _, running_string, local_print_info) = walk_tree_recursive(model.root, set(), {}, '', {})

    if serene_print:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/tick_overwrite/tick_overwrite.py', 'r', encoding = 'utf-8') as write_file:
            better_ticks = write_file.read()

    with open(write_location + project_name + '.py', 'w', encoding = 'utf-8') as write_file:
        write_file.write(
            ''.join([('import ' + node.name + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
            + 'import py_trees' + os.linesep
            + 'import serene_safe_assignment' + os.linesep
            + 'import random' + os.linesep
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
                            (indent(1) + format_variable_name_only(variable, format_mode = {'init': True, 'loc' : 'blackboard'}) + ' = [None] * ' + handle_constant_str(variable.array_size) + os.linesep)
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
                                                  , format_mode = {'init': True, 'loc' : 'blackboard'})
                            if variable.model_as == 'DEFINE' else
                            handle_variable_statement(variable, variable, indent_level = 1, format_mode = {'init': True, 'loc' : 'blackboard'}, assign_to_var = True)
                        )
                    )
                    for variable in model.variables if is_blackboard(variable)
                ]
            )
            + indent(1) + 'return blackboard_reader' + os.linesep
            + (
                better_ticks
                if serene_print
                else
                ''
            )
            + os.linesep
            + os.linesep
            + 'def create_tree(environment):' + os.linesep
            + running_string
            + indent(1) + 'return ' + root_name + os.linesep
        )
    with open(write_location + project_name + '_runner.py', 'w', encoding = 'utf-8') as write_file:
        write_file.write(create_runner(list(filter(is_blackboard, model.variables)), list(filter(is_env, model.variables)), local_print_info))
    with open(write_location + project_environment_name + '.py', 'w', encoding = 'utf-8') as write_file:
        write_file.write(write_environment(model))
    return


if __name__ == '__main__':

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
    write_files(args.metamodel_file, args.model_file, args.name, args.location, args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print)
