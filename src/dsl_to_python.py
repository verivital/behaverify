'''
This module is for internal use with BehaVerify.
It is used to convert .tree files to Python code.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2023-11-03
'''
import argparse
import os
import shutil
import itertools
from behaverify_common import indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type, BTreeException, constant_type
from serene_functions import build_meta_func
from check_grammar import validate_model


def write_files(metamodel_file, model_file, main_name, write_location, serene_print, max_iter, no_var_print, py_tree_print, recursion_limit):
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

    # misc_args variable explained
    # misc_args is a dict {'init' : init, 'loc' : loc, 'indent_level' : indent_level}.
    # init is a boolean. if true, it means we are initializing. if false, we are not.
    # loc is a location. location can be node, blackboard, or environment.
    def create_misc_args(init, loc, indent_level):
        return {'init' : init, 'loc' : loc, 'indent_level' : indent_level}

    def to_python_type(behaverify_type):
        if behaverify_type == 'ENUM':
            return 'str'
        if behaverify_type == 'BOOLEAN':
            return 'bool'
        if behaverify_type == 'INT':
            return 'int'
        raise ValueError(behaverify_type + ' is of an unsupported type. Only ENUM, BOOLEAN, and INT are supported')

    def str_conversion(atom_type, atom):
        if atom_type in ('VARIABLE', 'NODE'):
            return str(atom)
        if atom_type == 'CONSTANT':
            atom_type = constant_type(atom, declared_enumerations)
        return (
            ('\'' + atom + '\'')
            if atom_type == 'ENUM' else
            (
                str(atom)
                if atom_type == 'BOOLEAN' else
                (
                    ('(' + str(atom) + ')')
                    if atom < 0 else
                    str(atom)
                )
            )
        )

    def execute_loop(function_call, to_call, packaged_args, misc_args):
        return_vals = []
        all_domain_values = []
        if function_call.min_val is None:
            for domain_code in function_call.loop_variable_domain:
                for domain_value in execute_code(domain_code):
                    resolved = resolve_potential_reference_no_type(domain_value, declared_enumerations, {}, variables, constants, loop_references)
                    all_domain_values.append(resolved[1])
        else:
            (min_val, max_val) = get_min_max(function_call.min_val, function_call.max_val, declared_enumerations, {}, variables, constants, loop_references)
            all_domain_values = range(min_val, max_val + 1)
        cond_func = build_meta_func(function_call.loop_condition)
        for domain_member in all_domain_values:
            loop_references[function_call.loop_variable] = domain_member
            if cond_func((constants, loop_references))[0]:
                return_vals.extend(to_call(packaged_args, misc_args))
            loop_references.pop(function_call.loop_variable)
        return return_vals

    def execute_code(code):
        cur_func = build_meta_func(code)
        return cur_func((constants, loop_references))

    def format_function_if(_, function_call, misc_args):
        return ['(' + format_code(function_call.values[1], misc_args)[0] + ' if ' + format_code(function_call.values[0], misc_args)[0] + ' else ' + format_code(function_call.values[2], misc_args)[0] + ')']

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, function_call.values[0], misc_args)

    def format_function_before(function_name, function_call, misc_args):
        return [
            function_name + '('
            + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_between(function_name, function_call, misc_args):
        return [
            '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_implies(_, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return ['(' + '(not ' + formatted_values[0] + ') or ' + formatted_values[1] + ')']

    def format_function_division(_, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return ['(int(' + formatted_values[0] + ' / ' + formatted_values[1] + '))']

    def format_function_xnor(_, function_call, misc_args):
        return ['(not (' + function_format['xor'][1](function_format['xor'][0], function_call, misc_args)[0] + '))']

    def format_function_count(_, function_call, misc_args):
        return [
            '('
            + '[' + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values]) + '].count(True)'
            + ')'
        ]

    def format_function_index(_, function_call, misc_args):
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        formatted_variable = format_variable_name_only(variable, misc_args)
        formatted_index = ''
        if function_call.constant_index == 'constant_index':
            index_func = build_meta_func(function_call.values[0])
            index = resolve_potential_reference_no_type(index_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
            formatted_index = str(index)
        else:
            formatted_index = format_code(function_call.values[0], misc_args)[0]
        return [
            (formatted_variable + '(' + formatted_index + ')')
            if variable.model_as == 'DEFINE' else
            (formatted_variable + '[serene_safe_assignment.index_func(' + formatted_index + ', ' + str(variable_array_size_map[variable.name]) + ')]')
        ]

    def format_function(code, misc_args):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def format_variable_name_only(variable, misc_args):
        return (
            (
                ('node.' if is_local(variable) else ('self.' if is_env(variable) else 'self.blackboard.'))
                + variable.name
            )
            if misc_args['loc'] == 'environment'
            else
            (
                (
                    ('blackboard_reader.')
                    if misc_args['loc'] == 'blackboard' else
                    ('self.' + ('' if is_local(variable) else 'blackboard.'))
                )
                + variable.name
            )
        )

    def format_variable(variable, misc_args):
        return format_variable_name_only(variable, misc_args) + ('()' if variable.model_as == 'DEFINE' else '')

    def handle_atom(code, misc_args):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException as bt_e:  # this should be an argument.
            if misc_args['loc'] == 'node':
                return 'self.' + code.atom.reference
            if misc_args['loc'] == 'environment':
                return 'node.' + code.atom.reference
            raise BTreeException([], 'Encountered unknown reference: ' + str(code.atom.reference)) from bt_e
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom, misc_args)

    def format_code(code, misc_args):
        return (
            [handle_atom(code, misc_args)]
            if code.atom is not None else
            (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)]
                if code.code_statement is not None else
                format_function(code, misc_args)
            )
        )

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
                    if serene_print else
                    ''
                )
                + indent(2) + 'self.name = name' + os.linesep
                + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
                + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
                + os.linesep)

    def update_method_check(node):
        return (indent(1) + 'def update(self):' + os.linesep
                + indent(2) + 'return_status = ((py_trees.common.Status.SUCCESS) if ('
                + format_code(node.condition, create_misc_args(False, 'node', 2))[0]
                + ') else (py_trees.common.Status.FAILURE))' + os.linesep
                + (
                    (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                    if serene_print else
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
                    if serene_print else
                    ''
                )
                + indent(2) + 'self.name = name' + os.linesep
                + indent(2) + 'self.environment = environment' + os.linesep
                + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
                + ''.join([(indent(2) + 'self.blackboard.register_key(key = (\'' + variable.name + '\'), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
                + os.linesep)

    def update_method_environment_check(node):
        return (indent(1) + 'def update(self):' + os.linesep
                + indent(2) + 'return_status = ((py_trees.common.Status.SUCCESS) if ('
                + 'self.environment.' + node.name + '(self)'
                + ') else (py_trees.common.Status.FAILURE))' + os.linesep
                + (
                    (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                    if serene_print else
                    ''
                )
                + indent(2) + 'return return_status' + os.linesep)

    def resolve_variable_nondeterminism(values, misc_args):
        formatted_values = []
        for value in values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) == 0:
            raise ValueError('variable had no valid values!')
        if len(formatted_values) == 1:
            return formatted_values[0]
        if len(formatted_values) == 2:
            return '(' + formatted_values[0] + ' if random.choice((True, False)) else ' + formatted_values[1] + ')'
        return  (
            ''.join(
                [
                    '(' + value
                    + (
                        (' if (temp := random.randint(0, ' + str(len(formatted_values) - 1) + ')) else ')
                        if index == 0 else
                        (
                            (' if temp == ' + str(index) + ' else ')
                            if index < len(formatted_values) - 1 else
                            ''
                        )
                    )
                    for (index, value) in enumerate(formatted_values)
                ]
            )
            + ')' * len(formatted_values)
        )

    def handle_assign(assign, misc_args):
        case_results = assign.case_results
        default_result = assign.default_result
        if len(case_results) == 0:
            return resolve_variable_nondeterminism(default_result.values, misc_args)  # NOTE: no linesep at the end!
        return (
            '(' + os.linesep
            + ''.join(
                [
                    (
                        indent(misc_args['indent_level'] + 1 + index)
                        + resolve_variable_nondeterminism(case_result.values, misc_args) + os.linesep
                        + indent(misc_args['indent_level'] + 1 + index) + 'if ' + format_code(case_result.condition, misc_args)[0] + ' else' + os.linesep
                        + indent(misc_args['indent_level'] + 1 + index) + '(' + os.linesep
                     ) for index, case_result in enumerate(case_results)
                ]
            )
            + indent(misc_args['indent_level'] + len(case_results))
            + resolve_variable_nondeterminism(default_result.values, misc_args) + os.linesep
            + indent(misc_args['indent_level']) + (')' * (1 + len(case_results)))  # NOTE: no linesep at the end!
        )

    def handle_loop_array_index(packed_args, misc_args):
        (loop_array_index, constant_index) = packed_args
        if loop_array_index.array_index is not None:
            results = handle_assign(loop_array_index.array_index.assign, misc_args)
            indices = []
            for index_expr in loop_array_index.array_index.index_expr:
                if constant_index:
                    index_func = build_meta_func(index_expr)
                    for index in index_func((constants, loop_references)):
                        new_index = resolve_potential_reference_no_type(index, declared_enumerations, {}, variables, constants, loop_references)[1]
                        indices.append(str(new_index))
                else:
                    for index in format_code(index_expr, misc_args):
                        indices.append(index)
            return [(indices, results)]
        return execute_loop(loop_array_index, handle_loop_array_index, (loop_array_index.loop_array_index, constant_index), misc_args)

    def variable_assignment(variable, assign_value, misc_args, array_mode):
        # i don't think we should be able to have define variables here.
        safety_1 = '' if variable.model_as == 'DEFINE' else ('serene_safe_assignment.' + variable.name + '(')
        safety_2 = '' if variable.model_as == 'DEFINE' else ')'
        return (
            (
                indent(misc_args['indent_level']) + '__temp_var__ = ' + safety_1 + assign_value + safety_2 + os.linesep
                + indent(misc_args['indent_level']) + 'for (index, val) in __temp_var__:' + os.linesep
                + indent(misc_args['indent_level'] + 1) + format_variable_name_only(variable, misc_args) + '[index] = val' + os.linesep
            )
            if array_mode else
            (indent(misc_args['indent_level']) + format_variable_name_only(variable, misc_args) + ' = ' + safety_1 + assign_value + safety_2 + os.linesep)
        )

    def handle_variable_statement(variable_statement, misc_args, assign_to_var):
        # assign_to_var is False ONLY when we're doing shenanigans with read statements.
        variable = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 2)
        if is_array(variable):
            meta_results = []
            for loop_array_index in variable_statement.assigns:
                meta_results.extend(handle_loop_array_index((loop_array_index, variable_statement.constant_index), new_misc_args))
            assign_string = (
                '['
                + ', '.join(
                    [
                        ('(' + index + ', ' + results + ')')
                        for (indices, results) in meta_results
                        for index in indices
                    ]
                )
                + ']'
            )
            return (variable_assignment(variable, assign_string, misc_args, array_mode = True) if assign_to_var else assign_string)
        return (variable_assignment(variable, handle_assign(variable_statement.assign, misc_args), misc_args, array_mode = False) if assign_to_var else handle_assign(variable_statement.assign, misc_args))

    def create_neural_network(variable, misc_args):
        file_prefix = model_file.rsplit('/', 1)[0]
        source_func = build_meta_func(variable.source)
        source_vals = source_func((constants, {}))
        source = source_vals[0]
        source = resolve_potential_reference_no_type(source, declared_enumerations, {}, variables, constants, {})[1]
        shutil.copy(file_prefix + '/' + source, write_location + '/' + source)
        # NOT DONE. Need some way of storing the network
        # current idea: have some variable like variable.name + '__actual__network' which this call.
        # ugh, what a pain.
        return (
            os.linesep + os.linesep
            + indent(misc_args['indent_level']) + 'def ' + variable.name + '(index):' + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'if type(index) is not int:' + os.linesep
            + indent(misc_args['indent_level'] + 2) + "raise TypeError('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'if index < 0 or index >= ' + str(variable_array_size_map[variable.name]) + ':' + os.linesep
            + indent(misc_args['indent_level'] + 2) + "raise ValueError('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
        )

    def create_variable_macro(variable_statement, misc_args):
        variable = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 1)
        if is_array(variable):
            # todo: consider optimizing this for constant index. No reason to compute everything when we know the index.
            default_value = handle_assign(variable_statement.default_value, new_misc_args)
            new_values = handle_variable_statement(variable_statement, new_misc_args, assign_to_var = False)
            return (
                os.linesep
                + os.linesep
                + indent(misc_args['indent_level']) + 'def ' + variable.name + '(index):' + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'if type(index) is not int:' + os.linesep
                + indent(misc_args['indent_level'] + 2) + "raise TypeError('Index must be an int when accessing " + variable.name + ": ' + str(type(index)))" + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'if index < 0 or index >= ' + str(variable_array_size_map[variable.name]) + ':' + os.linesep
                + indent(misc_args['indent_level'] + 2) + "raise ValueError('Index out of bounds when accessing " + variable.name + ": ' + str(index))" + os.linesep
                + indent(misc_args['indent_level'] + 1) + variable.name + ' = [' + default_value + ' for _ in range(' + str(variable_array_size_map[variable.name]) + ')]' + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'seen_indices = set()' + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'for (new_index, new_value) in ' + new_values + ':' + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'if new_index in seen_indices:' + os.linesep
                + indent(misc_args['indent_level'] + 3) + 'continue' + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'seen_indices.add(new_index)' + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'if type(new_index) is not int:' + os.linesep
                + indent(misc_args['indent_level'] + 3) + "raise TypeError('Index must be an int when accessing " + variable.name + ": ' + str(type(new_index)))" + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'if new_index < 0 or new_index >= ' + str(variable_array_size_map[variable.name]) + ':' + os.linesep
                + indent(misc_args['indent_level'] + 3) + "raise ValueError('Index out of bounds when accessing " + variable.name + ": ' + str(new_index))" + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'if type(new_value) is not ' + variable_type_map[variable.name] + ':' + os.linesep
                + indent(misc_args['indent_level'] + 3) + "raise ValueError('Variable " + variable.name + " is type " + variable_type_map[variable.name] + ". Got type(new_value)')" + os.linesep
                + indent(misc_args['indent_level'] + 2) + variable.name + '[new_index] = new_value' + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'return ' + variable.name + '[index]' + os.linesep
                + os.linesep
                + indent(misc_args['indent_level']) + format_variable_name_only(variable, misc_args) + ' = ' + variable.name + os.linesep
            )
        return (
            os.linesep
            + os.linesep
            + indent(misc_args['indent_level']) + 'def ' + variable.name + '():' + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'return ' + handle_assign(variable_statement.assign, new_misc_args) + os.linesep
            + os.linesep
            + indent(misc_args['indent_level']) + format_variable_name_only(variable, misc_args) + ' = ' + variable.name + os.linesep
        )

    def handle_read_statement(read_statement, misc_args):
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 1)
        return (
            indent(misc_args['indent_level']) + 'if ' + 'self.environment.' + read_statement.name + '__condition(self):' + os.linesep
            + (
                variable_assignment(read_statement.condition_variable,
                                    (
                                        '[(' +
                                        (
                                            resolve_potential_reference_no_type(execute_code(read_statement.index_of)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                                            if read_statement.constant_index == 'constant_index' else
                                            format_code(read_statement.index_of, new_misc_args)[0]
                                        )
                                        + ', True)]'
                                    )
                                    if is_array(read_statement.condition_variable) else
                                    'True',
                                    new_misc_args,
                                    array_mode = is_array(read_statement.condition_variable))
                if read_statement.condition_variable is not None else
                ''
            )
            + ''.join(
                [
                    (
                        variable_assignment(read_var_state.variable,
                                            ('self.environment.' + read_statement.name + '__' + str(index) + '(self)'),
                                            misc_args = new_misc_args,
                                            array_mode = is_array(read_var_state.variable))
                    )
                    for index, read_var_state in enumerate(read_statement.variable_statements)
                ]
            )
            + (
                (
                    indent(2) + 'else:' + os.linesep
                    + variable_assignment(read_statement.condition_variable,
                                          (
                                              '[(' +
                                              (
                                                  resolve_potential_reference_no_type(execute_code(read_statement.index_of)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                                                  if read_statement.constant_index == 'constant_index' else
                                                  format_code(read_statement.index_of, new_misc_args)[0]
                                              )
                                              + ', False)]'
                                          )
                                          if is_array(read_statement.condition_variable) else
                                          'False',
                                          misc_args = new_misc_args,
                                          array_mode = is_array(read_statement.condition_variable))
                )
                if read_statement.condition_variable is not None else
                ''
            )
        )

    def handle_write_statement(write_statement, misc_args):
        return ''.join(
            [
                (indent(misc_args['indent_level']) + 'self.environment.' + write_statement.name + '__' + str(index) + '(self)' + os.linesep)
                if update_env.instant else
                (indent(misc_args['indent_level']) + 'self.environment.delay_this_action(' + 'self.environment.' + write_statement.name + '__' + str(index) + ', self)' + os.linesep)
                for index, update_env in enumerate(write_statement.update)
            ]
        )

    def format_returns(status_result):
        return 'py_trees.common.Status.' + status_result.status.upper()

    def handle_return_statement(statement, misc_args):
        variable_name = 'return_status'
        if len(statement.case_results) == 0:
            return indent(misc_args['indent_level']) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep
        return (
            (''.join(
                [
                    (indent(misc_args['indent_level']) + 'elif ' + format_code(case_result.condition, misc_args)[0] + ':' + os.linesep
                     + (indent(misc_args['indent_level'] + 1) + variable_name + ' = ' + format_returns(case_result) + os.linesep)
                     ) for case_result in statement.case_results
                ]
            )).replace('elif', 'if', 1)
            + indent(misc_args['indent_level']) + 'else:' + os.linesep
            + indent(misc_args['indent_level'] + 1) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep
        )

    def init_method_action(node):
        misc_args = create_misc_args(True, 'node', 2)
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
                    if serene_print else
                    ''
                )
                + indent(2) + 'self.name = name' + os.linesep
                + indent(2) + 'self.environment = environment' + os.linesep
                + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
                + ''.join([(indent(2) + 'self.blackboard.register_key(key = (\'' + variable.name + '\'), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
                + ''.join([(indent(2) + 'self.blackboard.register_key(key = (\'' + variable.name + '\'), access = py_trees.common.Access.WRITE)' + os.linesep) for variable in node.write_variables])
                + ''.join(
                    [
                        create_variable_macro(local_variable, misc_args = misc_args)
                        if local_variable.model_as == 'DEFINE' else
                        (
                            (
                                (indent(2) + format_variable_name_only(local_variable, misc_args = misc_args) + ' = [' + handle_assign(local_variable.default_value, misc_args) + ' for _ in range(' + str(variable_array_size_map[local_variable.name]) + ')]'  + os.linesep)
                                if is_array(local_variable) else
                                ''
                            )
                            + handle_variable_statement(local_variable, misc_args = misc_args, assign_to_var = True)
                        )
                        for local_variable in node.local_variables if local_variable not in [statement.variable for statement in node.init_statements]
                    ]
                )
                + ''.join(
                    [
                        create_variable_macro(statement, misc_args = misc_args)
                        if statement.variable.model_as == 'DEFINE' else
                        (
                            (
                                (indent(2) + format_variable_name_only(statement.variable, misc_args = misc_args) + ' = [' + handle_assign(statement.default_value, misc_args) + ' for _ in range(' + str(variable_array_size_map[statement.variable.name]) + ')]'  + os.linesep)
                                if is_array(statement.variable) else
                                ''
                            )
                            + handle_variable_statement(statement, misc_args = misc_args, assign_to_var = True)
                        )
                        for statement in node.init_statements
                    ]
                )
                + os.linesep)

    def handle_statement(statement, misc_args):
        return (
            handle_variable_statement(statement.variable_statement, misc_args, assign_to_var = True)
            if statement.variable_statement is not None else
            (
                handle_read_statement(statement.read_statement, misc_args)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, misc_args)
            )
        )

    def update_method_action(node):
        misc_args = create_misc_args(False, 'node', 2)
        return (indent(1) + 'def update(self):' + os.linesep
                + ''.join([handle_statement(statement, misc_args) for statement in node.pre_update_statements])
                + handle_return_statement(node.return_statement, misc_args)
                + (
                    (indent(2) + "self.__serene_print__ = return_status.value" + os.linesep)
                    if serene_print else
                    ''
                )
                + ''.join([handle_statement(statement, misc_args) for statement in node.post_update_statements])
                + indent(2) + 'return return_status' + os.linesep
                )

    def build_check_node(node):
        return (standard_imports
                + os.linesep + os.linesep
                + class_definition(node.name)
                + init_method_check(node)
                + update_method_check(node)
                )

    def build_environment_check_node(node):
        return (standard_imports
                + os.linesep + os.linesep
                + class_definition(node.name)
                + init_method_environment_check(node)
                + update_method_environment_check(node)
                )

    def build_action_node(node):
        return (standard_imports
                + os.linesep + os.linesep
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
                               + (
                                   (
                                       ', '
                                       + ', '.join(
                                           [
                                               ', '.join(
                                                   [
                                                       str_conversion(*resolve_potential_reference_no_type(argument, declared_enumerations, {}, variables, constants, loop_references))
                                                       for argument in execute_code(argument_code)
                                                   ]
                                               )
                                               for argument_code in arguments
                                           ]
                                       )
                                   )
                                   if len(arguments) > 0 else
                                   ''
                               )
                               + ')' + os.linesep)
            if current_node.node_type == 'action':
                variable_print_info[node_name] = current_node.local_variables
            return (node_name, node_names, node_names_map, running_string, variable_print_info)
        if current_node.node_type == 'X_is_Y':
            if current_node.x == current_node.y:
                raise ValueError('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            decorator_type = current_node.x.capitalize() + 'Is' + current_node.y.capitalize()
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
        def create_type_check_function(variable, function_name, indent_level):
            cur_var_type = variable_type_map[variable.name]
            return_string = (
                indent(indent_level) + 'def ' + function_name + '(new_value):' + os.linesep
                + indent(indent_level + 1) + 'if type(new_value) is not ' + cur_var_type + ':' + os.linesep
                + indent(indent_level + 2) + 'raise TypeError(' + "'variable " + variable.name + " expected type " + cur_var_type + " but received type ' + str(type(new_value)))" + os.linesep
            )
            if variable.domain.min_val is not None:
                min_val = resolve_potential_reference_no_type(execute_code(variable.domain.min_val)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                max_val = resolve_potential_reference_no_type(execute_code(variable.domain.max_val)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                return_string += (
                    indent(indent_level + 1) + 'if new_value >= ' + str(min_val) + ' and new_value <= ' + str(max_val) + ':' + os.linesep
                    + indent(indent_level + 2) + 'return new_value' + os.linesep
                    + indent(indent_level + 1) + 'else:' + os.linesep
                    + indent(indent_level + 2) + 'raise ValueError(\'variable ' + variable.name + ' expected value between ' + str(min_val) + ' and ' + str(max_val) + ' inclusive but received value \' + str(new_value))' + os.linesep
                )
            elif variable.domain.boolean is not None or variable.domain.true_int is not None or variable.domain.true_real is not None:
                return_string += indent(indent_level + 1) + 'return new_value' + os.linesep
            else:
                value_list = []
                for domain_code in variable.domain.domain_codes:
                    value_list.extend(execute_code(domain_code))
                value_list = (
                    '['
                    + ', '.join(
                        [
                            str_conversion(*resolve_potential_reference_no_type(value, declared_enumerations, {}, variables, constants, loop_references))
                            for value in value_list
                        ]
                    )
                    + ']'
                )
                return_string += (
                    indent(indent_level + 1) + 'if new_value in ' + value_list
                    + ':' + os.linesep
                    + indent(indent_level + 2) + 'return new_value' + os.linesep
                    + indent(indent_level + 1) + 'else:' + os.linesep
                    + indent(indent_level + 2) + 'raise ValueError("variable ' + variable.name + ' expected value in ' + value_list + ' but received value " + str(new_value))' + os.linesep
                )
            return return_string
        outter_return_string = (
            'def index_func(index, array_size):' + os.linesep
            + indent(1) + 'if type(index) is not int:' + os.linesep
            + indent(2) + 'raise TypeError(\'Array index must be an int\')' + os.linesep
            + indent(1) + 'if index < 0 or index >= array_size:' + os.linesep
            + indent(2) + 'raise ValueError(\'Array index out of bounds\')' + os.linesep
            + indent(1) + 'return index' + os.linesep
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
                    + indent(2) + 'if index < 0 or index >= ' + str(variable_array_size_map[variable.name]) + ':' + os.linesep
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
                + ', \'array_size\' : ' + str(variable_array_size_map[local_var.name] if local_var.name in variable_array_size_map else None) + '}'
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
                if py_tree_print else
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
                if no_var_print else
                (
                    'def print_blackboard():' + os.linesep
                    + indent(1) + 'ret_string = \'blackboard\' + os.linesep' + os.linesep
                    + ''.join(
                        [
                            (
                                (
                                    indent(1) + 'ret_string += indent(1) + \'' + variable.name + ': \' + str([blackboard_reader.' + variable.name
                                    + '(x) for x in range(' + str(variable_array_size_map[variable.name]) + ')]) + os.linesep' + os.linesep
                                )
                                if variable.model_as == 'DEFINE' and is_array(variable) else
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
                                    + '(x) for x in range(' + str(variable_array_size_map[variable.name]) + ')]) + os.linesep' + os.linesep
                                )
                                if variable.model_as == 'DEFINE' and is_array(variable) else
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
                    + os.linesep + os.linesep
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
                if serene_print else
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
                if serene_print else
                ''
            )
            + indent(2) + 'full_tick()' + os.linesep
            + (
                (indent(2) + 'print(tree_printer(root, 0))' + os.linesep)
                if serene_print else
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
            misc_args = create_misc_args(False, 'environment', 2)
            return (
                os.linesep
                + indent(1) + 'def ' + node.name + '(self, node):' + os.linesep
                + indent(2) + "'''" + os.linesep
                + indent(2) + '-- RETURN' + os.linesep
                + indent(2) + 'This method is expected to return True or False.' + os.linesep
                + indent(2) + 'This method is being modeled using the following behavior:' + os.linesep
                + indent(2) + format_code(node.condition, misc_args)[0] + os.linesep
                + indent(2) + '-- SIDE EFFECTS' + os.linesep
                + indent(2) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(2) + "'''" + os.linesep
                + indent(2) + '# below we include an auto generated attempt at implmenting this' + os.linesep
                + indent(2) + 'return ' + format_code(node.condition, misc_args)[0] + os.linesep
            )

        def env_handle_read_statement(statement):
            misc_args = create_misc_args(False, 'environment', 2)
            return (
                os.linesep
                + indent(1) + 'def ' + statement.name + '__condition(self, node):' + os.linesep
                + indent(2) + 'if ' + format_code(statement.condition, misc_args)[0] + ':' + os.linesep
                + indent(3) + 'return '
                + (
                    'random.choice([True, False])'
                    if statement.non_determinism else
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
                            + indent(2) + 'return ' + handle_variable_statement(read_var_state, misc_args, assign_to_var = False) + os.linesep
                        )
                        for index, read_var_state in enumerate(statement.variable_statements)
                    ]
                )
            )

        def env_handle_write_statement(statement):
            misc_args = create_misc_args(False, 'environment', 2)
            return ''.join(
                [
                    (
                        os.linesep
                        + indent(1) + 'def ' + statement.name + '__' + str(index) + '(self, node):' + os.linesep
                        + handle_variable_statement(env_update, misc_args, assign_to_var = True)
                        + indent(2) + 'return' + os.linesep
                    )
                    for index, env_update in enumerate(statement.update)
                ]
            )

        update_misc_args = create_misc_args(False, 'environment', 2)
        initial_misc_args = create_misc_args(True, 'environment', 2)
        to_write = (
            'import random' + os.linesep
            + (('import onnxruntime' + os.linesep) if model.neural else '')
            + 'import serene_safe_assignment' + os.linesep
            + os.linesep + os.linesep
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
                    handle_variable_statement(update, update_misc_args, assign_to_var = True)
                    for update in model.update if update.instant
                ]
            )
            + indent(2) + 'return' + os.linesep
            + os.linesep
            + indent(1) + 'def post_tick_environment_update(self):' + os.linesep
            + ''.join(
                [
                    handle_variable_statement(update, update_misc_args, assign_to_var = True)
                    for update in model.update if not update.instant
                ]
            )
            + indent(2) + 'return' + os.linesep
            + os.linesep
            + indent(1) + 'def check_tick_condition(self):' + os.linesep
            + (
                (indent(2) + 'return True' + os.linesep)
                if model.tick_condition is None else
                (indent(2) + 'return ' + format_code(model.tick_condition, update_misc_args)[0] + os.linesep)
            )
            + os.linesep
            + indent(1) + 'def __init__(self, blackboard):' + os.linesep
            + indent(2) + 'self.blackboard = blackboard' + os.linesep
            + indent(2) + 'self.delayed_action_queue = []' + os.linesep
            + (os.linesep if any(map(is_env, model.variables)) else '')
            + ''.join(
                [
                    create_neural_network(variable, initial_misc_args)
                    if variable.model_as == 'NEURAL' else
                    (
                        create_variable_macro(variable, initial_misc_args)
                        if variable.model_as == 'DEFINE' else
                        (
                            (
                                (indent(2) + format_variable(variable, initial_misc_args) + ' = [' + handle_assign(variable.default_value, initial_misc_args) + ' for _ in range(' + str(variable_array_size_map[variable.name]) + ')]' + os.linesep)
                                if is_array(variable) else
                                ''
                            ) + handle_variable_statement(variable, initial_misc_args, assign_to_var = True)
                        )
                    )
                    for variable in model.variables if is_env(variable)
                ]
            )
        )
        for environment_check in model.environment_checks:
            to_write += env_handle_environment_check(environment_check)
        for action in model.action_nodes:
            for statement in itertools.chain(action.pre_update_statements, action.post_update_statements):
                if statement.variable_statement is not None:
                    continue
                to_write += (
                    env_handle_read_statement(statement.read_statement)
                    if statement.read_statement is not None else
                    env_handle_write_statement(statement.write_statement))
        return to_write

    function_format = {
        'if' : ('', format_function_if),
        'loop' : ('', format_function_loop),
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
        'eq' : ('==', format_function_between),
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

    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit)
    variable_type_map = {
        variable.name : to_python_type(variable_type(variable, declared_enumerations, constants))
        for variable in model.variables
    }
    variable_array_size_map = {
        variable.name : variable_array_size(variable, declared_enumerations, {}, variables, constants, {})
        for variable in model.variables if is_array(variable)
    }
    loop_references = {}

    project_name = main_name
    project_environment_name = main_name + '_environment'

    with open(write_location + 'serene_safe_assignment.py', 'w', encoding = 'utf-8') as write_file:
        write_file.write(create_safe_assignment(model))  # checked. No additional information required.

    for action in model.action_nodes:
        with open(write_location + action.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_action_node(action))
    for check in model.check_nodes:
        with open(write_location + check.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_check_node(check))
    for environment_check in model.environment_checks:
        with open(write_location + environment_check.name + '_file.py', 'w', encoding = 'utf-8') as write_file:
            write_file.write(build_environment_check_node(environment_check))

    (root_name, _, _, running_string, local_print_info) = walk_tree_recursive(model.root, set(), {}, '', {})

    if serene_print:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/tick_overwrite/tick_overwrite.py', 'r', encoding = 'utf-8') as write_file:
            better_ticks = write_file.read()

    initial_misc_args = create_misc_args(True, 'blackboard', 1)
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
                    create_variable_macro(variable, initial_misc_args)
                    if variable.model_as == 'DEFINE' else
                    (
                        (
                            (indent(1) + format_variable_name_only(variable, initial_misc_args) + ' = [' + handle_assign(variable.default_value, initial_misc_args) + ' for _ in range(' + str(variable_array_size_map[variable.name]) + ')]' + os.linesep)
                            if is_array(variable) else
                            ''
                        ) +  handle_variable_statement(variable, initial_misc_args, assign_to_var = True)
                    )
                    for variable in model.variables if is_blackboard(variable)
                ]
            )
            + indent(1) + 'return blackboard_reader' + os.linesep
            + (
                better_ticks
                if serene_print else
                ''
            )
            + os.linesep + os.linesep
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
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    args = arg_parser.parse_args()
    write_files(args.metamodel_file, args.model_file, args.name, args.location, args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print, args.recursion_limit)
