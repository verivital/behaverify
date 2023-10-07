'''
This module is for internal use with BehaVerify.
It is used to create Haskell code from BehaVerify DSL for Behavior Trees.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2023-10-03
'''
import argparse
import os
import shutil
import itertools
import textx
from behaverify_common import haskell_indent as indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type
from serene_functions import build_meta_func
from check_model import validate_model


def dsl_to_haskell():
    '''
    this function is used to convert the dsl to haskell code
    '''
    def to_haskell_type(behaverify_type):
        if behaverify_type == 'ENUM':
            return 'String'
        if behaverify_type == 'BOOLEAN':
            return 'Bool'
        if behaverify_type == 'INT':
            return 'Integer'
        raise ValueError(behaverify_type + ' is of an unsupported type. Only ENUM, BOOLEAN, and INT are supported')

    def str_conversion(atom_type, atom):
        return (
            ('"' + atom + '"')
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

    def pascal_case(variable_name):
        '''removes underscores, capitalizes'''
        return ''.join(
            map(
                lambda x: x[:1].upper() + x[1:]
                ,
                variable_name.split('_')
            )
        )

    def camel_case(variable_name):
        '''removes underscores, capitalizes, does not capitalize first word'''
        return ''.join(
            map(
                lambda x:
                (
                    ((x[1][:1].lower()) + x[1][1:])
                    if x[0] == 0
                    else
                    ((x[1][:1].upper()) + x[1][1:])
                )
                ,
                enumerate(variable_name.split('_'))
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
        return ['(if ' + format_code(function_call.values[0], misc_args)[0] + ' then ' + format_code(function_call.values[1], misc_args)[0] + ' else ' + format_code(function_call.values[2], misc_args)[0] + ')']

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, function_call.values[0], misc_args)

    def format_function_before(function_name, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return [
            ' '.join([('(' + function_name + ' ' + formatted_value) for formatted_value in formatted_values[0:-2]])
            + '(' + function_name + ' ' + formatted_values[-2] + ' ' + formatted_values[-1] + ')'
            + ')'*(len(formatted_values[0:-2]))
        ]

    def format_function_between(function_name, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return [
            ' '.join([('(' + ' ' + formatted_value + function_name) for formatted_value in formatted_values[0:-2]])
            + '(' + formatted_values[-2] + ' ' + function_name + ' ' + formatted_values[-1] + ')'
            + ')'*(len(formatted_values[0:-2]))
        ]

    def format_function_count(function_name, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) == 1:
            return ['(if ' + formatted_values + ' then 1 else 0)']
        return [
            ' '.join([('(' + function_name + ' ' + formatted_value) for formatted_value in formatted_values[0:-2]])
            + '(' + function_name + ' ' + formatted_values[-2] + ' ' + formatted_values[-1] + ')'
            + ')'*(len(formatted_values[0:-2]))
        ]

    def format_function_index(_, function_call, misc_args):
        variable = resolve_potential_reference_no_type(execute_code(function_call.to_index)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        if function_call.constant_index == 'constant_index':
            index = str(resolve_potential_reference_no_type(execute_code(function_call.values[0])[0], declared_enumerations, {}, variables, constants, loop_references)[1])
        else:
            index = format_code(function_call.values[0], misc_args)[0]
        return [
            '(indexInto' + pascal_case(variable.name)
            + (('Location' + str(variable_stages['nodeLocation'])) if is_local(variable) else '')
            + ' ' + index + ' ' + format_variable(variable, misc_args)+ ')'
        ]

    def format_function(code, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.'''
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def create_misc_args(init_mode, indent_level):
        return {
            'init_mode' : init_mode,  # 'env', 'board', or 'none'
            'indent_level' : indent_level
        }

    def format_variable(variable, misc_args):
        node_location = variable_stages['nodeLocation']
        if is_local(variable):
            new_name = variable.name + 'Location' + str(node_location)
            if new_name in variable_stages:
                return 'newVal' + str(variable_stages[new_name] - 1) + pascal_case(variable.name) + 'Location' + str(node_location)
        elif variable.name in variable_stages:
            return 'newVal' + str(variable_stages[variable.name] - 1) + pascal_case(variable.name)
        if variable.model_as == 'DEFINE':
            # here we will handle all the strange arguments.
            arguments = ' '.join([format_variable(depended_on, misc_args) for depended_on in macro_depends_on[(variable.name, node_location)]])
        else:
            arguments = 'environment' if is_env(variable) else 'blackboard'
        return (
            ('(localBoard' + pascal_case(variable.name) + 'Location' + str(node_location) + ' ' + arguments + ')')
            if is_local(variable)
            else
            (
                ('(env' + pascal_case(variable.name) + ' ' + arguments + ')')
                if is_env(variable)
                else
                ('(board' + pascal_case(variable.name) + ' ' + arguments + ')')
            )
        )

    def format_variable_next(variable, misc_args):
        if is_local(variable):
            node_location = variable_stages['nodeLocation']
            new_name = variable.name + 'Location' + str(node_location)
            return 'newVal' + str(variable_stages[new_name] if new_name in variable_stages else 1) + pascal_case(variable.name) + 'Location' + str(node_location)
        return 'newVal' + str(variable_stages[variable.name] if variable.name in variable_stages else 1) + pascal_case(variable.name)

    def update_variable_in_variable_stage(variable, misc_args):
        if is_local(variable):
            node_location = variable_stages['nodeLocation']
            new_name = variable.name + 'Location' + str(node_location)
            variable_stages[new_name] = (variable_stages[new_name] if new_name in variable_stages else 1) + 1
        else:
            variable_stages[variable.name] = (variable_stages[variable.name] if variable.name in variable_stages else 1) + 1

    def handle_atom(code, misc_args):
        (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom, misc_args)

    def format_code(code, misc_args):
        return (
            [handle_atom(code, misc_args)] if code.atom is not None else (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)] if code.code_statement is not None else (
                    format_function(code, misc_args)
                )
            )
        )

    def handle_case_result(case_result, converted_variable_type, var_is_env, misc_args):
        condition_string = format_code(case_result.condition, misc_args)[0] if hasattr(case_result, 'condition') else 'otherwise'
        where_string = ''
        value_string = ''
        formatted_values = []
        random_length = 1
        for value in case_result.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) == 1:
            value_string = formatted_values[0]
            return (condition_string, value_string, where_string, None, random_length)
        random_length = len(formatted_values)
        value_string = ''
        random_number_pair_name = ('env' if var_is_env else 'board') + 'RandomNumberPair' + str(variable_stages[(var_is_env, 'randomNumberPair')] if (var_is_env, 'randomNumberPair') in variable_stages else 1)
        indent_level = misc_args['indent_level']
        function_name = 'randomNumberToResult' + str(variable_stages['randomNumberToResult'] if 'randomNumberToResult' in variable_stages else 1)
        value_string = function_name + ' (fst ' + random_number_pair_name  + ')'
        post_string = (
            indent(indent_level) + function_name + ' :: Integer -> ' + converted_variable_type + os.linesep
            + ''.join([
                (indent(indent_level) + function_name + str(index) + ' = ' + value + os.linesep)
                for (index, value) in formatted_values
            ])
            + (indent(indent_level) + function_name + ' _ = error "' + function_name + ' illegal value"' + os.linesep)
        )
        variable_stages[(var_is_env, 'randomNumberPair')] = (variable_stages[(var_is_env, 'randomNumberPair')] if (var_is_env, 'randomNumberPair') in variable_stages else 1) + 1
        variable_stages['randomNumberToResult'] = (variable_stages['randomNumberToResult'] if 'randomNumberToResult' in variable_stages else 1) + 1
        return (condition_string, value_string, post_string, variable_stages[(var_is_env, 'randomNumberPair')] - 1, random_length)

    def handle_assign(assign, converted_variable_type, var_is_env, misc_args):
        return [handle_case_result(case_result, converted_variable_type, var_is_env, misc_args) for case_result in assign.case_results] + [handle_case_result(assign.default_result, converted_variable_type, var_is_env, misc_args)]

    def handle_loop_array_index(packed_args, misc_args):
        (loop_array_index, converted_variable_type, var_is_env, constant_index) = packed_args
        indent_level = misc_args['indent_level']
        if loop_array_index.array_index is not None:
            results = handle_assign(loop_array_index.array_index.assign, converted_variable_type, var_is_env, create_misc_args(misc_args['init_mode'], indent_level))
            indices = []
            for index_expr in loop_array_index.array_index:
                if constant_index:
                    index_func = build_meta_func(index_expr)
                    for index in index_func((constants, loop_references)):
                        new_index = resolve_potential_reference_no_type(index, declared_enumerations, {}, variables, constants, loop_references)[1]
                        indices.append(str(new_index))
                else:
                    for index in format_code(index_expr, misc_args):
                        indices.append(index)
            return [(indices, results)]
        return execute_loop(loop_array_index, handle_loop_array_index, (loop_array_index.loop_array_index, converted_variable_type, var_is_env, constant_index), misc_args)

    def handle_formatted_results(new_name, previous_name, read_condition, results, indent_level, random_number_pair_base):
        return_string = indent(indent_level) + new_name + os.linesep
        post_string = ''
        random_string = ''
        if read_condition is not None:
            return_string = return_string + indent(indent_level + 1) + '| not (' + read_condition + ') = ' + previous_name + os.linesep
        for (condition, value, post, random_number_pair_num, random_length) in results:
            return_string = return_string + indent(indent_level + 1) + '| ' + condition + ' = ' + value + os.linesep
            post_string = post_string + post
            if random_length > 1:
                random_string = indent(indent_level) + random_number_pair_base + str(random_number_pair_num) + ' = getRandomInteger (snd ' + random_number_pair_base + str(random_number_pair_num - 1) + ') ' + str(random_length) + os.linesep
        if len(results) == 1 and read_condition is None:
            return_string = (indent(indent_level) + new_name + ' = ' + results[0][1] + os.linesep)
        return return_string + post_string + random_string

    def handle_variable_statement(variable_statement, read_condition, misc_args):
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        converted_variable_type = to_haskell_type(variable_type(assign_var, declared_enumerations, constants))
        var_is_env = is_env(assign_var)
        random_number_pair_base = ('env' if var_is_env else 'board') + 'RandomNumberPair'
        indent_level = misc_args['indent_level']
        new_name = format_variable_next(assign_var, misc_args)
        previous_name = format_variable(assign_var, misc_args)
        if is_array(assign_var):
            meta_results = []
            constant_index = variable_statement.constant_index
            for loop_array_index in variable_statement.assigns:
                meta_results.extend(handle_loop_array_index((loop_array_index, converted_variable_type, constant_index), misc_args))
            update_variable_in_variable_stage(assign_var, misc_args)
            update_pair_strings = []
            return_string = ''
            for (num, (indices, results)) in enumerate(meta_results):
                update_value_name = new_name + 'Update' + str(num)
                return_string = return_string + handle_formatted_results(update_value_name, None, None, results, indent_level, random_number_pair_base)
                for index in indices:
                    update_pair_strings.append('(' + index + ', ' + update_value_name + ')')
            return (
                (return_string + indent(indent_level) + new_name + ' = newArray' + pascal_case(assign_var.name) + (('Location' + str(variable_stages['nodeLocation'])) if is_local(assign_var) else '') + ' ' + previous_name + ' [' + ', '.join(update_pair_strings) + ']' + os.linesep)
                if read_condition is None else
                (return_string + indent(indent_level) + new_name + ' = if ' + read_condition + ' then ' + previous_name + ' else (newArray' + pascal_case(assign_var.name) + (('Location' + str(variable_stages['nodeLocation'])) if is_local(assign_var) else '') + ' ' + previous_name + ' [' + ', '.join(update_pair_strings) + '])' + os.linesep)
            )
        results = handle_assign(variable_statement.assign, converted_variable_type, var_is_env, misc_args)
        update_variable_in_variable_stage(assign_var, misc_args)
        return handle_formatted_results(new_name, previous_name, read_condition, results, indent_level, random_number_pair_base)

    def handle_read_statement(read_statement, misc_args):
        indent_level = misc_args['indent_level']
        return_string = ''
        cond_var = read_statement.condition_variable
        condition = format_code(read_statement.condition, misc_args)[0]
        condition_name = 'readCondition' + str(variable_stages['readCondition'] if 'readCondition' in variable_stages else 1)
        variable_stages['readCondition'] = (variable_stages['readCondition'] if 'readCondition' in variable_stages else 1) + 1
        if read_statement.non_determinism == 'non_determinism':
            return_string = (
                return_string
                + indent(indent_level) + 'envRandomNumberPair' + str(variable_stages[(True, 'RandomNumberPair')] if (True, 'RandomNumberPair') in variable_stages else 1) + ' = getRandomInteger (snd envRandomNumberPair' + str((variable_stages[(True, 'RandomNumberPair')] if (True, 'RandomNumberPair') in variable_stages else 1) - 1) + ' 1)' + os.linesep
                + indent(indent_level) + condition_name + ' = (' + condition + ') && ((fst envRandomNumberPair' + str(variable_stages[(True, 'RandomNumberPair')] if (True, 'RandomNumberPair') in variable_stages else 1) + ') == 1)' + os.linesep
            )
            variable_stages[(True, 'RandomNumberPair')] = (variable_stages[(True, 'RandomNumberPair')] if (True, 'RandomNumberPair') in variable_stages else 1) + 1
        else:
            return_string = return_string + indent(indent_level) + condition_name + ' = ' + condition + os.linesep
        if cond_var is not None:
            return_string = return_string + indent(indent_level) + 'newVal' + str(variable_stages[cond_var.name] if cond_var.name in variable_stages else 1) + pascal_case(cond_var.name) + ' = ' + condition_name
            variable_stages[cond_var.name] = (variable_stages[cond_var.name] if cond_var.name in variable_stages else 1) + 1
        for variable_statement in read_statement.variable_statements:
            return_string += handle_variable_statement(variable_statement, condition_name, misc_args)
        return return_string

    def handle_write_statement(write_statement, misc_args):
        return_string = ''
        delay_queue = []
        for variable_statement in write_statement.update:
            if variable_statement.intant:
                return_string += handle_variable_statement(variable_statement, None, misc_args)
            else:
                delay_queue.append(variable_statement)
        return (return_string, delay_queue)

    def format_returns(status_result):
        return status_result.status.capitalize()

    def handle_return_statement(return_statement, misc_args):
        indent_level = misc_args['indent_level']
        if len(return_statement.case_results) == 0:
            return indent(indent_level) + 'returnStatus = ' + format_returns(return_statement.default_result) + os.linesep
        return (
            indent(indent_level) + 'returnStatus' + os.linesep
            + ''.join(
                [
                    (indent(indent_level + 1) + '| ' + format_code(case_result.condition, None) + ' = ' + format_returns(case_result) + os.linesep)
                    for case_result in return_statement.case_results
                ]
            )
            + indent(indent_level + 1) + '| otherwise = ' + format_returns(return_statement.default_result) + os.linesep
        )

    def handle_statement(statement, misc_args):
        return (
            (handle_variable_statement(statement.variable_statement, None, misc_args), [])
            if statement.variable_statement is not None else
            (
                (handle_read_statement(statement.read_statement, misc_args), [])
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, misc_args)
            )
        )

    def module_declaration(node_name):
        return 'module BTree' + pascal_case(node_name) + ' where' + os.linesep

    def check_function(node, node_location):
        variable_stages.clear()
        variable_stages['nodeLocation'] = node_location
        indent_modifier = 2 if len(node.arguments) > 0 else 0
        return (
            (
                (
                    'bTreeFunctionCreator' + pascal_case(node.name) + ' :: '
                    + ' -> '.join(map(lambda arg_pair: to_haskell_type(arg_pair.argument_type), node.arguments))
                    + ' -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)' + os.linesep
                    + 'bTreeFunctionCreator' + pascal_case(node.name) + ' '
                    + ' '.join(map(lambda arg_pair: arg_pair.argument_name, node.arguments))
                    + ' = bTreeFunction' + pascal_case(node.name) + os.linesep
                    + indent(1) + 'where' + os.linesep
                )
                if len(node.arguments) > 0
                else
                ''
            )
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' _ nodeLocation _ _ _ _ blackboard environment futureChanges' + os.linesep
            + indent(1 + indent_modifier) + '| ' + format_code(node.condition, None) + ' = (Success, [], [], blackboard, environment, futureChanges)' + os.linesep
            + indent(1 + indent_modifier) + '| otherwise = (Failure, [], [], blackboard, environment, futureChanges)'
        )

    def format_blackboard_creation(init_mode):
        misc_args = create_misc_args(init_mode, 0)
        if init_mode is None:
            return (
                'createBlackboadAtLocation nodeLocation (snd boardRandomNumberPair' + str(variable_stages[(False, 'RandomNumberPair')] - 1) + ') '
                + ' '.join([format_variable(variable, misc_args) for (variable, _) in blackboard_order_node_location])
            )
        formatted_variables = []
        for (variable, node_locations) in blackboard_order:
            for node_location in node_locations:
                variable_stages['nodeLocation'] = node_location
                formatted_variables.append(format_variable(variable, misc_args))
        return 'createBlackboad (snd boardRandomNumberPair' + str(variable_stages[(False, 'RandomNumberPair')] - 1) + ') ' + ' '.join(formatted_variables)

    def format_environment_creation(init_mode):
        misc_args = create_misc_args(init_mode, 0)
        return (
            'createEnvironment (snd envRandomNumberPair' + str(variable_stages[(False, 'RandomNumberPair')] - 1) + ') '
            + ' '.join([format_variable(variable, misc_args) for (variable, _) in environment_order_node_location])
        )

    def format_blackboard_and_environment_creation(misc_args):
        indent_level = misc_args['indent_level']
        needs_new_board = False
        needs_new_env = False
        return_string = ''
        for variable in variables:
            if variable.name in variable_stages:
                if is_env(variable):
                    needs_new_env = True
                else:
                    needs_new_board = True
            if needs_new_board and needs_new_env:
                break
        if needs_new_board:
            return_string += (
                indent(indent_level) + 'newBlackboard = ' + format_blackboard_creation(misc_args['init_mode']) + os.linesep
            )
        else:
            return_string += indent(indent_level) + 'newBlackboard = blackboard' + os.linesep
        if needs_new_env:
            return_string += (
                indent(indent_level) + 'newEnvironment = ' + format_environment_creation(misc_args['init_mode']) + os.linesep
            )
        else:
            return_string += indent(indent_level) + 'newEnvironment = environment' + os.linesep
        return return_string

    def action_function(node, node_location):
        variable_stages.clear()
        variable_stages['nodeLocation'] = node_location
        variable_stages[(False, 'RandomNumberPair')] = 1
        variable_stages[(True, 'RandomNumberPair')] = 1
        indent_modifier = 2 if len(node.arguments) > 0 else 0
        return_string = ''
        return_string += indent(2 + indent_modifier) + 'boardRandomNumberPair0 = (-1, sereneBoardGenerator blackboard)' + os.linesep
        return_string += indent(2 + indent_modifier) + 'envRandomNumberPair0 = (-1, sereneEnvGenerator environment)' + os.linesep
        delay_updates = []
        for statement in node.pre_update_statements:
            temp = handle_statement(statement, create_misc_args(None, 2 + indent_modifier))
            return_string += temp[0]
            delay_updates.extend(temp[1])
        return_string += handle_return_statement(node.return_statement, create_misc_args(None, 2 + indent_modifier))
        for statement in node.post_update_statements:
            temp = handle_statement(statement, create_misc_args(None, 2 + indent_modifier))
            return_string += temp[0]
            delay_updates.extend(temp[1])
        return_string += format_blackboard_and_environment_creation(2 + indent_modifier)
        for (index, delayed) in enumerate(delay_updates):
            variable_stages.clear()  # clear variables again.
            return_string += (
                indent(2 + indent_modifier) + 'futureChanges' + str(index) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                + indent(2 + indent_modifier) + 'futureChanges' + str(index) + ' (blackboard, environment) = (newBlackboard, newEnvironment)' + os.linesep
                + indent(3 + indent_modifier) + 'where' + os.linesep
                + handle_variable_statement(delayed, None, create_misc_args(None, 4 + indent_modifier))
                + format_blackboard_and_environment_creation(4 + indent_modifier)
            )
        return (
            (
                (
                    'bTreeFunctionCreator' + pascal_case(node.name) + ' :: '
                    + ' -> '.join(map(lambda arg_pair: to_haskell_type(arg_pair.argument_type), node.arguments))
                    + ' -> ([BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput)' + os.linesep
                    + 'bTreeFunctionCreator' + pascal_case(node.name) + ' '
                    + ' '.join(map(lambda arg_pair: arg_pair.argument_name, node.arguments))
                    + ' = bTreeFunction' + pascal_case(node.name) + os.linesep
                    + indent(1) + 'where' + os.linesep
                )
                if len(node.arguments) > 0 else
                ''
            )
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)' + os.linesep
            + indent(1 + indent_modifier) + 'where' + os.linesep
            + return_string
            + indent(2 + indent_modifier) + 'newFutureChanges = ' + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, reversed(range(delay))))) + (' : ' if delay > 0 else '') + 'futureChanges' + os.linesep
        )

    def build_check_node(node, node_location):
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + check_function(node, node_location)
                )

    def build_environment_check_node(node, node_location):
        return build_check_node(node, node_location)

    def build_action_node(node, node_location):
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + action_function(node, node_location)
                )

    def create_runner(model, name, max_iter):
        '''creates the runner for haskell code'''
        current_node = model.root
        while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            else:
                current_node = current_node.sub_root
        root_name = current_node.name
        return (
            'module Main where' + os.linesep
            + 'import ' + pascal_case(name) + os.linesep
            + 'import BehaviorTreeCore' + os.linesep
            + 'import BehaviorTreeEnvironment' + os.linesep
            + 'import BehaviorTreeBlackboard' + os.linesep
            + 'import System.Environment (getArgs)' + os.linesep
            + os.linesep + os.linesep
            + 'executeFromSeeds :: Integer -> Integer -> Integer -> [(BTreeBlackboard, BTreeEnvironment)]' + os.linesep
            + 'executeFromSeeds seed1 seed2 maxIteration = eachBoardEnv' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'initBoard = initialBlackboard seed1' + os.linesep
            + indent(2) + 'initEnv = initialEnvironment seed2 initBoard' + os.linesep
            + indent(2) + 'treeRoot = bTreeNode' + pascal_case(root_name) + os.linesep
            + indent(2) + 'executionChain :: Integer -> TrueMemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]' + os.linesep
            + indent(2) + 'executionChain count memory partial blackboard environment' + os.linesep
            + indent(3) + '| count >= maxIteration = [(blackboard, environment)]' + os.linesep
            + indent(3) + '| not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]' + os.linesep
            + indent(3) + '| otherwise = (blackboard, environment) : executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv' + os.linesep
            + indent(3) + 'where' + os.linesep
            + indent(4) + '(_, nextMemory, nextPartial, tempBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment' + os.linesep
            + indent(4) + '(nextBoard, nextEnv) = betweenTickUpdate (applyFutureChanges futureChanges (tempBoard, tempEnv))' + os.linesep
            + indent(2) + 'eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv'+ os.linesep
            + os.linesep
            + 'boardEnvToString :: (BTreeBlackboard, BTreeEnvironment) -> String' + os.linesep
            + 'boardEnvToString (blackboard, environment) = "(" ++ fromBTreeBlackboardToString blackboard ++ ", " ++ fromBTreeEnvironmentToString blackboard environment ++ ")"' + os.linesep
            + os.linesep
            + 'main :: IO ()' + os.linesep
            + 'main =' + os.linesep
            + indent(1) + 'do {' + os.linesep
            + indent(2) + 'args <- getArgs' + os.linesep
            + indent(2) + '; let (seed1, seed2) = seedFromArgs args in mapM_ putStrLn (map boardEnvToString (executeFromSeeds seed1 seed2 ' + str(int(max_iter) + 1) + '))' + os.linesep
            + indent(1) + '}' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'seedFromArgs :: [String] -> (Integer, Integer)' + os.linesep
            + indent(2) + 'seedFromArgs [] = (0, 0)' + os.linesep
            + indent(2) + 'seedFromArgs curArgs' + os.linesep
            + indent(3) + '| null (tail curArgs) = (read (head curArgs), 0)' + os.linesep
            + indent(3) + '| otherwise = (read (head curArgs), read (head (tail curArgs)))' + os.linesep
        )

    def create_tree(model, name):
        '''walks the tree to find stuff'''
        def node_function(node):
            if node.node_type in {'selector', 'sequence'}:
                return (
                    node.node_type
                    + (
                        'PartialMemory'
                        if node.memory == 'with_partial_memory' else
                        (
                            'TrueMemory'
                            if node.memory == 'with_true_memory' else
                            ''
                        )
                    )
                    + 'Func'
                )
            if node.node_type == 'parallel':
                return (
                    '('
                    + 'parallel'
                    + (
                        'PartialMemory'
                        if node.memory == 'with_partial_memory' else
                        (
                            'TrueMemory'
                            if node.memory == 'with_true_memory' else
                            ''
                        )
                    )
                    + 'Creator '
                    + (
                        'successOnAllFailureOne'
                        if node.parallel_policy == 'success_on_all' else
                        (
                            'successOnOneFailureOne'
                            if node.parallel_policy == 'success_on_one' else
                            'NOT DONE'
                        )
                    )
                    + ')'
                )
            return (
                '(decoratorCreator '
                + (
                    'inverterCreator'
                    if node.node_type == 'inverter' else
                    (
                        '('
                        + 'xISyCreator '
                        + str(node.x).capitalize()
                        + ' '
                        + str(node.y).capitalize()
                        + ')'
                    )
                )
                + ')'
            )

        def walk_tree_recursive(current_node, seen_nodes, node_names, node_names_map, running_string, running_int, indent_level):
            current_args = None
            while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
                current_args = (current_node.arguments if hasattr(current_node, 'arguments') else None)
                current_node = (current_node.leaf if hasattr(current_node, 'leaf') else current_node.sub_root)
            conflict_avoid_name = 'bTreeNode' + pascal_case(current_node.name)
            (node_name, modifier) = create_node_name(conflict_avoid_name, node_names, node_names_map)
            cur_node_names = {node_name}.union(node_names)
            cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
            running_int = running_int + 1
            my_int = running_int
            if current_node.node_type in ('check', 'environment_check', 'action'):
                seen_nodes.add(current_node.name)
                has_args = len(current_node.arguments) > 0
                running_string = running_string + (
                    indent(indent_level) + node_name + ' = BTreeNode '
                    + ('(' if has_args else '') + 'bTreeFunction' + ('Creator' if has_args else '') + pascal_case(current_node.name)
                    + ((' ' + ' '.join([' '.join(val) for cur_arg in current_args for val in execute_code(cur_arg)]) + ')') if has_args else '')
                    + ' [] ' + str(my_int) + os.linesep
                )
            else:
                child_names = []
                node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
                for child in node_children:
                    (child_name, seen_nodes, cur_node_names, cur_node_names_map, running_string, running_int, indent_level) = walk_tree_recursive(child, seen_nodes, cur_node_names, cur_node_names_map, running_string, running_int, indent_level)
                    child_names.append(child_name)
                running_string = running_string + (
                    indent(indent_level) + node_name + ' = BTreeNode ' + node_function(current_node) + ' ' + '[' + ', '.join(child_names) + '] ' + str(my_int) + os.linesep
                )
            return (
                node_name,
                seen_nodes,
                cur_node_names,
                cur_node_names_map,
                running_string,
                running_int,
                indent_level
            )

        (_, seen_nodes,  _, _, node_declarations, _, _) = walk_tree_recursive(model.root, set(), set(), {}, '', -1, 0)

        return (
            seen_nodes,
            (
                'module ' + pascal_case(name) + ' where' + os.linesep
                + 'import BehaviorTreeCore' + os.linesep
                + ''.join([('import BTree' + pascal_case(node.name) + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks) if node.name in seen_nodes])
                + node_declarations
            )
        )

    def handle_initial_value(statement, node_location, misc_args):
        variable_stages['nodeLocation'] = node_location
        assign_var = statement.variable if hasattr(statement, 'variable') else statement
        default_string = ''
        if is_array(assign_var):
            converted_variable_type = to_haskell_type(variable_type(assign_var, declared_enumerations, constants))
            var_is_env = is_env(assign_var)
            random_number_pair_base = ('env' if var_is_env else 'board') + 'RandomNumberPair'
            indent_level = misc_args['indent_level']
            new_name = format_variable_next(assign_var, misc_args)
            results = handle_assign(statement.default_value, converted_variable_type, var_is_env, misc_args)
            update_variable_in_variable_stage(assign_var, misc_args)
            default_string = handle_formatted_results(new_name, None, None, results, indent_level, random_number_pair_base)
        return default_string + handle_variable_statement(statement, None, misc_args)

    def create_macro(statement, node_location, misc_args):
        variable_stages.clear()
        variable_stages['nodeLocation'] = node_location
        assign_var = statement.variable if hasattr(statement, 'variable') else statement
        converted_variable_type = to_haskell_type(variable_type(assign_var, declared_enumerations, constants))
        if is_array(assign_var):
            var_is_env = is_env(assign_var)
            random_number_pair_base = ('env' if var_is_env else 'board') + 'RandomNumberPair'
            new_name = format_variable_next(assign_var, misc_args)
            results = handle_assign(statement.default_value, converted_variable_type, var_is_env, misc_args)
            update_variable_in_variable_stage(assign_var, misc_args)
            return_string = handle_formatted_results(new_name, None, None, results, 2, random_number_pair_base)
            return_string += handle_variable_statement(statement, None, create_misc_args(None, 2))
            type_signature = '(' + ', '.join([converted_variable_type] * variable_array_size(assign_var, declared_enumerations, {}, variables, constants, loop_references)) + ')'
        else:
            return_string = handle_variable_statement(statement, None, create_misc_args(None, 2))
            type_signature = converted_variable_type
        (variable_types, needed_variables) = macro_depends_on[(assign_var.name, node_location)]
        return (
            ('env' if is_env(assign_var) else ('localBoard' if is_local(assign_var) else 'board')) + pascal_case(assign_var.name) + (('Location' + str(node_location)) if node_location is not None else '')
            + ' :: ' + ' -> '.join(variable_types) + ' -> ' + type_signature + os.linesep
            + ('env' if is_env(assign_var) else ('localBoard' if is_local(assign_var) else 'board')) + pascal_case(assign_var.name) + (('Location' + str(node_location)) if node_location is not None else '')
            + ' ' + ' '.join([format_variable(variable, misc_args) for variable in needed_variables]) + ' = ' + format_variable(assign_var, create_misc_args(None, 2)) + os.linesep
            + indent(1) + 'where' + os.linesep
            + return_string
        )

    def safe_update(variable, env_mode, local_mode, local_numbers = None):
        local_numbers = ([] if local_numbers is None else local_numbers)
        function_name = (
            (
                'updateEnv'
                if env_mode
                else
                (
                    'localUpdateBoard'
                    if local_mode
                    else
                    'updateBoard'
                )
            )
            + pascal_case(variable.name)
        )
        arg_type = (
            'BTreeEnvironment'
            if env_mode
            else
            (
                'Integer -> BTreeBlackboard'
                if local_mode
                else
                'BTreeBlackboard'
            )
        )
        return_type = (
            'BTreeEnvironment'
            if env_mode
            else
            'BTreeBlackboard'
        )
        board_type = (
            'environment'
            if env_mode
            else
            'blackboard'
        )
        field_name = (
            (
                'env'
                if env_mode
                else
                (
                    'localBoard'
                    if local_mode
                    else
                    'board'
                )
            )
            + pascal_case(variable.name)
        )
        return (
            function_name + ' :: ' + arg_type + ' -> ' + variable_type(variable) + ' -> ' + return_type + os.linesep
            + (
                (
                    function_name + (' _ ' if local_mode else ' ') + board_type + ' _ = ' + board_type + os.linesep
                )
                if variable.model_as == 'FROZENVAR'
                else
                (
                    (
                        ''.join(
                            [
                                (function_name + ' ' + str(number) + ' ' + board_type + ' value = ' + board_type + ' { ' + field_name + str(number) + ' = value }' + os.linesep)
                                if variable.domain.boolean is not None or variable.domain.min_val is None
                                else
                                (
                                    (
                                        ''.join(
                                            map(
                                                lambda value :
                                                (function_name + ' ' + str(number) + ' ' + board_type + ' ' + handle_constant(value, True) + ' = ' + board_type + ' { ' + field_name + str(number) + ' = ' + handle_constant(value, True) + ' }' + os.linesep)
                                                ,
                                                variable.domain.enums
                                            )
                                        )
                                        + (function_name + ' ' + str(number) + ' _ _ = error "' + variable.name + ' illegal value"' + os.linesep)
                                    )
                                    if variable.domain.min_val is None
                                    else
                                    (
                                        function_name + ' ' + str(number) + ' ' + board_type + ' value' + os.linesep
                                        + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "local ' + variable.name + ' illegal value"' + os.linesep
                                        + indent(1) + '| otherwise = ' + board_type + ' { ' + field_name + str(number) + ' = value }' + os.linesep
                                    )
                                )
                                for number in local_numbers
                            ]
                        )
                        + (function_name + ' _ _ _ = error "' + variable.name + ' illegal local reference"' + os.linesep)
                    )
                    if local_mode
                    else
                    (
                        (function_name + ' ' + board_type + ' value = ' + board_type + ' { ' + field_name + ' = value }' + os.linesep)
                        if variable.domain.boolean is not None
                        else
                        (
                            (
                                ''.join(
                                    map(
                                        lambda value :
                                        (function_name + ' ' + board_type + ' ' + handle_constant(value, True) + ' = ' + board_type + ' { ' + field_name + ' = ' + handle_constant(value, True) + ' }' + os.linesep)
                                        ,
                                        variable.domain.enums
                                    )
                                )
                                + (function_name + ' _ _ = error "' + variable.name + ' illegal value"' + os.linesep)
                            )
                            if variable.domain.min_val is None
                            else
                            (
                                function_name + ' ' + board_type + ' value' + os.linesep
                                + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "' + variable.name + ' illegal value"' + os.linesep
                                + indent(1) + '| otherwise = ' + board_type + ' { ' + field_name + ' = value }' + os.linesep
                            )
                        )
                    )
                )
            )
            + os.linesep
        )

    def create_check_value(variable):
        function_name = (
            (
                'checkValueEnv'
                if is_env(variable)
                else
                (
                    'checkValueLocalBoard'
                    if is_local(variable)
                    else
                    'checkValueBoard'
                )
            )
            + pascal_case(variable.name)
        )
        board_type = 'environment' if is_env(variable) else 'blackboard'
        field_name = (
            (
                'env'
                if is_env(variable)
                else
                (
                    'localBoard'
                    if is_local(variable)
                    else
                    'board'
                )
            )
            + pascal_case(variable.name)
        )
        return (
            function_name + ' :: ' + variable_type(variable) + ' -> ' + variable_type(variable) + os.linesep
            + (
                (function_name + ' value = value' + os.linesep)
                if variable.domain.boolean is not None or variable.domain.true_int is not None
                else
                (
                    (
                        ''.join(
                            map(
                                lambda value :
                                (function_name + ' ' + handle_constant(value, True) + ' = ' + handle_constant(value, True) + os.linesep)
                                ,
                                variable.domain.enums
                            )
                        )
                        + (function_name + ' _ = error "' + field_name + ' illegal value"' + os.linesep)
                    )
                    if variable.domain.min_val is None
                    else
                    (
                        function_name + ' value' + os.linesep
                        + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "' + field_name + ' illegal value"' + os.linesep
                        + indent(1) + '| otherwise = value' + os.linesep
                    )
                )
            )
            + os.linesep
        )

    def order_partial_arguments(current_var_name, create_order):
        use_name = True
        return_string = ''
        for variable_info in create_order:
            if variable_info['initial_name'] == current_var_name:
                use_name = False
            if use_name:
                return_string = return_string + ' ' + variable_info['initial_name']
            else:
                return_string = return_string + ' ' + variable_info['default_arg']
        return return_string

    def get_default_arg(variable):
        converted_variable_type = variable_type(variable)
        if converted_variable_type == 'Integer':
            return '0'
        if converted_variable_type == 'Bool':
            return 'True'
        return '" "'

    def array_set_creator(variable, local_number = None):
        prefix = ('env' if is_env(variable) else ('localBoard' if is_local(variable) else 'board'))
        prefix_cap = pascal_case(prefix)
        data_instance = ('environment' if is_env(variable) else 'blackboard')
        data_type = ('BTreeEnvironment' if is_env(variable) else 'BTreeBlackboard')
        variable_name = pascal_case(variable.name) + ('' if local_number is None else ('Location' +str(local_number)))
        check_name = 'checkValue' + prefix_cap + pascal_case(variable.name)
        return (
            'update' + prefix_cap + variable_name + ' :: Integer -> ' + data_type + ' -> ' + variable_type(variable) + ' -> ' + data_type + os.linesep
            + ''.join(
                [
                    ('update' + prefix_cap + variable_name + ' ' + str(index) + ' = update' + prefix_cap + variable_name + 'Index' + str(index) + os.linesep)
                    for index in range(handle_constant(variable.array_size, False))
                ]
            )
            + 'update' + prefix_cap + variable_name + ' _ = error "' + prefix_cap + variable_name + ' illegal index value"' + os.linesep
            + 'arrayUpdate' + prefix_cap + variable_name + ' :: ' + data_type + ' -> [(Integer, ' + variable_type(variable) + ')] -> ' + data_type + os.linesep
            + 'arrayUpdate' + prefix_cap + variable_name + ' ' + data_instance + ' []  = ' + data_instance + os.linesep  # no update
            + 'arrayUpdate' + prefix_cap + variable_name + ' ' + data_instance + ' [(index, value)] = update' + prefix_cap + variable_name + ' index ' + data_instance + ' value' + os.linesep  # single value update is already defined
            # below we do multiple value updating.
            + 'arrayUpdate' + prefix_cap + variable_name + ' ' + data_instance + ' indicesValues = ' + data_instance + ' {' + os.linesep
            + indent(1)
            + (indent(1) + ', ').join(
                [
                    (prefix + variable_name + 'Index' + str(index) + ' = new' + variable_name + 'Index' + str(index) + os.linesep)
                    for index in range(handle_constant(variable.array_size, False))
                ]
            )
            + indent(1) + '}' + os.linesep
            # we updated each value of the array, and below we are defining what those values are
            + indent(2) + 'where' + os.linesep
            + indent(3) + '(' + ', '.join(
                [
                    ('new' + variable_name + 'Index' + str(index))
                    for index in range(handle_constant(variable.array_size, False))
                ]
            ) + ') = updateValues indicesValues' + os.linesep
            # each of the new values is equal based on updateValues
            # updateValues is a function which goes through an for each step in the list changes one value. It is ordered in a specific way
            # suppose we have [(1, 'a'), (2, 'b'), (1, 'c'), (3, 'd')]
            # then we want this to update index 1 to a, 2 to b, and 3 to d, and ignore the 1=c option.
            # therefore, we use recursion.
            + indent(3) + 'updateValues :: [(Integer, ' + variable_type(variable) + ')] -> (' + ', '.join(map(lambda x: variable_type(variable), range(handle_constant(variable.array_size, False)))) + ')' + os.linesep
            + indent(3) + 'updateValues [] = (' + ', '.join(map(lambda x: (prefix + variable_name + 'Index' + str(x) + ' ' + data_instance), range(handle_constant(variable.array_size, False)))) + ')' + os.linesep # in the base case, just grab what the current value is.
            + ''.join(
                [
                    (
                        indent(3) + 'updateValues ((' + str(index) + ', currentValue) : nextIndicesValues) = ('
                        + ', '.join(map(lambda x: (check_name + ' currentValue') if x == index else ('updatedValue' + str(x)), range(handle_constant(variable.array_size, False))))
                        + ')' + os.linesep
                        + indent(4) + 'where' + os.linesep
                        # + indent(5) + 'updatedValue' + str(index) + ' = checkValueBoard' + variable_name + ' currentValue' + os.linesep # this needs to go through the type safety check.
                        + indent(5) + '(' + ', '.join(map(lambda x: '_' if x == index else ('updatedValue' + str(x)), range(handle_constant(variable.array_size, False)))) + ') = updateValues nextIndicesValues' + os.linesep
                    )
                        for index in range(handle_constant(variable.array_size, False))
                ]
            )
        )

    def handle_blackboard_environment(define_print_info, create_order, blackboard_mode, local_macros, local_var_to_nodes):
        # todo: create environment and blackboard create methods.
        data_type_name = 'BTreeBlackboard' if blackboard_mode else 'BTreeEnvironment'
        data_type_name_2 = 'BTreeBlackboard' if blackboard_mode else 'BTreeBlackboard -> BTreeEnvironment'
        board_env_cap = 'Board' if blackboard_mode else 'Env'
        board_env = 'board' if blackboard_mode else 'env'
        var_name = 'blackboard' if blackboard_mode else 'environment'
        var_name_2 = 'blackboard' if blackboard_mode else ('blackboard' + ' ' + 'environment')
        is_non_local = is_blackboard if blackboard_mode else is_env
        return (
            'module ' + ('BehaviorTreeBlackboard' if blackboard_mode else 'BehaviorTreeEnvironment') +  ' where' + os.linesep
            + 'import SereneRandomizer' + os.linesep
            + 'import System.Random' + os.linesep
            + 'import SereneOperations' + os.linesep
            + ('' if blackboard_mode else ('import BehaviorTreeBlackboard' + os.linesep))
            + os.linesep
            # end of imports.
            # ---------------------------------------------------------------------------------------
            + 'data ' + data_type_name + ' = ' + data_type_name + ' {' + os.linesep
            + indent(1) + 'serene' + board_env_cap + 'Generator :: StdGen' + os.linesep
            + ((indent(1) + ', ') if len(create_order) > 0 else '')
            + (os.linesep + indent(1) + ', ').join([(variable_info['field_name'] + ' :: ' + variable_info['type']) for variable_info in create_order])
            + (os.linesep if len(create_order) > 0 else '')
            + indent(1) + '}' + os.linesep + os.linesep
            + (
                'from' + data_type_name + 'ToString :: ' + data_type_name_2 + ' -> String' + os.linesep
                + 'from' + data_type_name + 'ToString ' + var_name_2 + ' = '
                + '"' + board_env_cap + ' = {"'
                + ' ++ '
                + ' ++ ", " ++ '.join(
                    list(map(
                        lambda variable_info:
                        variable_info['print_info']
                        ,
                        filter(lambda variable_info: variable_info['print_info'] is not None, create_order)
                    )) + define_print_info
                )
                + (' ++ ' if len(create_order) > 0 else '')
                + '"}"' + os.linesep
            )
            # end of blackboard and show for the blackbord.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF ' + ('BLACKBOARD' if blackboard_mode else 'ENVIRONMENT') + ' FUNCTIONS' + os.linesep + os.linesep
            + ''.join(
                [
                    create_macro(variable, None, create_misc_args(None, 0))
                    for variable in model.variables if (variable.model_as == 'DEFINE' and is_non_local(variable))
                ]
            )
            # created accessor functions for define non-local ---------------------------------------------------------------------------------------
            # todo: this is not correct
            + (
                (
                    os.linesep + '-- START OF LOCAL BLACKBOARD FUNCTIONS' + os.linesep + os.linesep
                    + ''.join(
                        [
                            create_macro(variable, node_location, create_misc_args(None, 0))
                            for variable in model.variables if (variable.model_as == 'DEFINE' and is_local(variable) and variable.name in local_var_to_nodes)
                            for node_location in local_var_to_nodes[variable.name]
                        ]
                    )
                    # created accessor functions for define local
                    # ---------------------------------------------------------------------------------------
                )
                if blackboard_mode
                else
                ''
            )
            + os.linesep + '-- START OF GET FUNCTIONS FOR ARRAYS' + os.linesep + os.linesep
            + ''.join(
                [
                    board_env + pascal_case(variable.name) + ' :: ' + data_type_name + ' -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ')' + os.linesep
                    + board_env + pascal_case(variable.name) + ' ' + var_name + ' =  ('
                    + ' '.join([('(' + board_env + pascal_case(variable.name) + 'Index' + str(index) + ' ' + var_name + ')') for index in range(variable_array_size_map[variable.name])])
                    for variable in model.variables if (is_non_local(variable) and is_array(variable))
                ]
            )
            + (
                ''.join(
                    [
                        board_env + pascal_case(variable.name) + 'Location' + str(node_location) + ' :: ' + data_type_name + ' -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ')' + os.linesep
                        + board_env + pascal_case(variable.name) + 'Location' + str(node_location) + ' ' + var_name + ' =  ('
                        + ' '.join([('(' + board_env + pascal_case(variable.name) + 'Location' + str(node_location) + 'Index' + str(index) + ' ' + var_name + ')') for index in range(variable_array_size_map[variable.name])])
                        for variable in model.variables if (is_local(variable) and is_array(variable) and variable.name in local_var_to_nodes)
                        for node_location in local_var_to_nodes[variable.name]
                    ]
                )
                if blackboard_mode else
                ''
            )
            + os.linesep + '-- START OF INDEX FUNCTIONS FOR ARRAYS' + os.linesep + os.linesep
            + ''.join(
                [
                    'indexInto' + pascal_case(variable.name) + ' :: Integer -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ') -> ' + variable_type_map[variable.name] + os.linesep
                    + ''.join(
                        [
                            ('indexInto' + pascal_case(variable.name) + ' ' + str(index) + ' (' + ' '.join(['_'] * index) + ' value ' + ' '.join(['_'] * (variable_array_size_map[variable.name] - index - 1))  + ') = value' + os.linesep)
                            for index in range(variable_array_size_map[variable.name])
                        ]
                    )
                    + 'indexInto' + pascal_case(variable.name) + ' _ = error "indexInto'+ pascal_case(variable.name) + ' illegal index value"' + os.linesep
                    for variable in model.variables if (is_non_local(variable) and is_array(variable))
                ]
            )
            + (
                ''.join(
                    [
                        'indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' :: Integer -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ') -> ' + variable_type_map[variable.name] + os.linesep
                        + ''.join(
                            [
                                ('indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' ' + str(index) + ' (' + ' '.join(['_'] * index) + ' value ' + ' '.join(['_'] * (variable_array_size_map[variable.name] - index - 1))  + ') = value' + os.linesep)
                                for index in range(variable_array_size_map[variable.name])
                            ]
                        )
                        + 'indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' _ = error "indexInto'+ pascal_case(variable.name) + 'Location' + str(node_location) + ' illegal index value"' + os.linesep
                        for variable in model.variables if (is_local(variable) and is_array(variable) and variable.name in local_var_to_nodes)
                        for node_location in local_var_to_nodes[variable.name]
                    ]
                )
                if blackboard_mode
                else
                ''
            )
            # end of array variable indexing for non-define variables
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF TYPE CHECKING FUNCTIONS' + os.linesep + os.linesep
            + ''.join(map(create_check_value, filter(lambda var : var.model_as == 'VAR' and (blackboard_mode != is_env(var)), model.variables)))
            # created checkValue for each variable that can be updated.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF NEW ARRAY FUNCTIONS' + os.linesep + os.linesep
            + ''.join(
                map(
                    lambda variable:
                    (
                        array_set_creator(variable, local_number = None)
                        if not is_local(variable)
                        else
                        ''.join(
                            'updateLocalBoard' + pascal_case(variable.name) + ' :: Integer -> Integer -> ' + data_type_name + ' -> ' + variable_type(variable) + ' -> BTreeBlackboard' + os.linesep
                            + ''.join(
                                map(
                                    lambda location:
                                    'updateLocalBoard' + pascal_case(variable.name) + ' ' + str(location) + ' = updateLocalBoard' + pascal_case(variable.name) + 'Location' + str(location) + os.linesep
                                    ,
                                    local_var_to_nodes[variable.name]
                                )
                            )
                            + 'updateLocalBoard' + pascal_case(variable.name) + ' _ = error "localBoard' + pascal_case(variable.name) + ' illegal local reference"' + os.linesep
                            + 'arrayUpdateLocalBoard' + pascal_case(variable.name) + ' :: Integer -> ' + data_type_name + ' -> [(Integer, ' + variable_type(variable) + ')] -> BTreeBlackboard' + os.linesep
                            + ''.join(
                                map(
                                    lambda location:
                                    'arrayUpdateLocalBoard' + pascal_case(variable.name) + ' ' + str(location) + ' = arrayUpdateLocalBoard' + pascal_case(variable.name) + 'Location' + str(location) + os.linesep
                                    ,
                                    local_var_to_nodes[variable.name]
                                )
                            )
                            + 'arrayUpdateLocalBoard' + pascal_case(variable.name) + ' _ = error "localBoard' + pascal_case(variable.name) + ' illegal local reference"' + os.linesep
                            + ''.join(
                                map(
                                    lambda location:
                                    array_set_creator(variable, local_number = location)
                                    ,
                                    local_var_to_nodes[variable.name]
                                )
                            )
                        )
                    ),
                    filter(lambda variable:
                           (
                               is_array(variable) and
                               blackboard_mode != is_env(variable) and
                               variable.model_as == 'VAR' and
                               ((not is_local(variable) or (variable.name in local_var_to_nodes)))  # this is ordered like this to ensure that if local_var_to_nodes is None this doesn't cause an error.
                           ),
                           model.variables)
                )
            )
            # end of array update functions for variables.
            # ---------------------------------------------------------------------------------------
            + (
                ''
                if blackboard_mode
                else
                (
                    os.linesep + '-- START OF TICK CONDITION' + os.linesep + os.linesep
                    + 'checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool' + os.linesep
                    + 'checkTickConditionTermination blackboard environment = ' + (
                        'True'
                        if model.tick_condition is None
                        else
                        format_code(model.tick_condition, None)
                    ) + os.linesep
                    # + 'modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment' + os.linesep
                    # + 'modifiedID _ environment = environment' + os.linesep  # I think I was planning on using these for eta reduction? but then didn't?
                    + os.linesep + '-- START OF FUTURE CHANGES' + os.linesep + os.linesep
                    + 'applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                    + 'applyFutureChanges [] = id' + os.linesep
                    + 'applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)' + os.linesep
                    + os.linesep + '-- START OF BETWEEN TICK CHANGES' + os.linesep + os.linesep
                    + 'betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                    + 'betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)' + os.linesep
                    + indent(1) + 'where' + os.linesep
                    + indent(2) + 'tempEnvironment0 = curEnvironment' + os.linesep
                    + indent(2) + 'newEnvironment = tempEnvironment' + str(len(model.update)) + os.linesep
                    + ''.join(
                        [
                            (
                                indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' :: BTreeEnvironment -> BTreeEnvironment' + os.linesep
                                + indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' environment' + handle_variable_statement(update, 2, None, None)
                                + os.linesep
                                + indent(2) + 'tempEnvironment' + str(index + 1) + ' = tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' tempEnvironment' + str(index) + os.linesep
                                + os.linesep
                            )
                            for index, update in enumerate(model.update)
                        ]
                    ) + os.linesep
                )
            )
            # end of tick conditions.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF INITIAL ' + ('BLACKBOARD' if blackboard_mode else 'ENVIRONMENT') + ' VALUE' + os.linesep + os.linesep
            + 'initial' + ('Blackboard' if blackboard_mode else 'Environment') + ' :: Integer -> ' + data_type_name_2 + os.linesep
            + 'initial' + ('Blackboard' if blackboard_mode else 'Environment') + ' seed ' + ('' if blackboard_mode else ('blackboard' + ' ')) + '= ' + data_type_name + ' newSereneGenerator ' + ' '.join(map(lambda x : x['initial_name'], create_order))
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
            + indent(2) + 'newSereneGenerator = tempGen' + str(len(create_order)) + os.linesep
            + ''.join(
                [
                    (
                        indent(2) + variable_info['partial_name'] + ' = ' + data_type_name + ' newSereneGenerator' + order_partial_arguments(variable_info['initial_name'], create_order) + os.linesep
                        + indent(2) + variable_info['initial_func'] + ' :: StdGen -> (' + variable_info['type'] + ', StdGen)' + os.linesep
                        + indent(2) + variable_info['initial_func'] + ' curGen' + variable_info['initial_value']
                        + os.linesep
                        + indent(2) + '(' + variable_info['initial_name'] + ', tempGen' + str(index + 1) + ') = ' + variable_info['initial_func'] + ' tempGen' + str(index) + os.linesep
                        + os.linesep
                    )
                    for index, variable_info in enumerate(create_order)
                ]
            )
            + os.linesep
            # created initial blackboard. ---------------------------------------------------------------------------------------
        )

    def get_print_info(variable, index, prefix, postfix, arguments):
        return (
            None
            if is_array(variable) and index != 0
            else
            (
                '"' + prefix + pascal_case(variable.name) + postfix + ': "' + (' ++ "["' if is_array(variable) else '')
                + ' ++ ", "'.join(
                    map(
                        lambda nested_index:
                        ' ++ show (' + prefix + pascal_case(variable.name) + ' ' + arguments(nested_index) + ')'
                        ,
                        range(handle_constant(variable.array_size, False) if is_array(variable) else 1)
                    )
                )
                + ('++ "]"' if is_array(variable) else '')
            )
        )

    def create_environment(model):
        create_order = [
            {
                'print_info' : get_print_info(variable, index, 'env', '', ((lambda x: str(x) + ' environment') if is_array(variable) else (lambda x: 'environment'))),
                'category_name' : 'env' + pascal_case(variable.name),
                'initial_name' : 'newVal' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'initial_func' : 'initVal' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'field_name' : 'env' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'partial_name' : 'partialEnvironment' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : handle_initial_value(
                    (variable.assign if ((not is_array(variable)) or variable.array_mode == 'range') else variable.assigns[index]),
                    variable_type(variable), 2, 'env',
                    'partialEnvironment' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                    None, array_index = (index if is_array(variable) else None)),
                'model_as' : variable.model_as
            }
            for variable in filter(lambda var: (var.model_as != 'DEFINE' and is_env(var)), model.variables)
            for index in range(handle_constant(variable.array_size, False) if is_array(variable) else 1)
        ]
        define_print_info = [
            get_print_info(variable, 0, 'env', '', ((lambda x: str(x) + ' blackboard environment') if is_array(variable) else (lambda x: 'blackboard environment')))
            for variable in filter(lambda var: (var.model_as == 'DEFINE' and is_env(var)), model.variables)
        ]
        return handle_blackboard_environment(define_print_info, create_order, False, None, {})

    def create_blackboard(model):
        def walk_tree_recursive_blackboard(current_node, node_names, node_names_map, running_dict, running_int, location_info, running_create_order, running_define_print_info):
            while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
                if hasattr(current_node, 'leaf'):
                    current_node = current_node.leaf
                else:
                    current_node = current_node.sub_root

            conflict_avoid_name = current_node.name.replace(' ', '') + '__node'

            (node_name, modifier) = create_node_name(conflict_avoid_name, node_names, node_names_map)
            cur_node_names = {node_name}.union(node_names)
            cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
            running_int = running_int + 1
            my_int = running_int

            if current_node.node_type == 'action':
                for variable in current_node.local_variables:
                    location_info.append((variable, my_int))
                    if variable.model_as == 'DEFINE':
                        cur_type = variable_type(variable)
                        if variable.name not in running_dict:
                            running_dict[variable.name] = []
                        cur_assign = variable.assign
                        cur_assigns = variable.assigns
                        cur_array_mode = variable.array_mode
                        for initial_statement in current_node.init_statements:
                            if initial_statement.variable.name == variable.name:
                                cur_assign = initial_statement.assign
                                cur_assigns = initial_statement.assigns
                                cur_array_mode = initial_statement.array_mode
                                break
                        # todo: plan is to utilize this area to also create define indexes.
                        # we will simply have two ints, str(my_int) and then str(index), utilizing a double variable strategy.
                        # node location is necessary so that we can access other local variables.
                        if is_array(variable):
                            running_dict[variable.name].append(
                                'localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + ' :: Integer -> BTreeBlackboard -> ' + cur_type + os.linesep
                                + ''.join(
                                    map(
                                        lambda index:
                                        'localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + ' ' + str(index)
                                        + ' = localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + 'Index' + str(index) + os.linesep,
                                        range(handle_constant(variable.array_size, False))
                                    )
                                )
                                + 'localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + ' _ = error "localBoard' + pascal_case(variable.name) + str(my_int) + ' illegal index"' + os.linesep
                                + ''.join(
                                    map(
                                        lambda index:
                                        'localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + 'Index' + str(index) + ' blackboard' + create_macro(cur_assign if cur_array_mode == 'range' else cur_assigns[index], 0, None, index)
                                        + indent(1) + 'where nodeLocation = ' + str(my_int) + os.linesep,
                                        range(handle_constant(variable.array_size, False))
                                    )
                                )
                            )
                        else:
                            running_dict[variable.name].append(
                                'localBoard' + pascal_case(variable.name) + ' ' + str(my_int) + ' blackboard' + create_macro(cur_assign, 0, None)  # misc_args none here because we are operating in a func
                                + indent(1) + 'where nodeLocation = ' + str(my_int) + os.linesep
                            )
                        running_define_print_info.append(
                            get_print_info(variable, 0, 'localBoard', 'Location' + str(my_int), ((lambda x: str(my_int) + ' ' + str(x) + ' blackboard') if is_array(variable) else (lambda x: str(my_int) + 'blackboard')))  # index hard coded to 0 cuz we're not looping for the whole thing.
                        )
                    else:
                        cur_assign = variable.assign
                        cur_assigns = variable.assigns
                        cur_array_mode = variable.array_mode
                        overwritten = False
                        for initial_statement in current_node.init_statements:
                            if initial_statement.variable.name == variable.name:
                                cur_assign = initial_statement.assign
                                cur_assigns = initial_statement.assigns
                                cur_array_mode = initial_statement.array_mode
                                overwritten = True
                                break
                        cur_type = variable_type(variable)
                        for index in range(handle_constant(variable.array_size, False) if is_array(variable) else 1):
                            running_create_order.append(
                                (
                                    overwritten,
                                    {
                                        'print_info' : get_print_info(variable, index, 'localBoard', 'Location' + str(my_int), ((lambda x: str(my_int) + ' ' + str(x) + ' blackboard') if is_array(variable) else (lambda x: str(my_int) + 'blackboard'))),
                                        'category_name' : 'localBoard' + pascal_case(variable.name),
                                        'initial_name' : 'localNewVal' + pascal_case(variable.name) + 'Location' + str(my_int) + (('Index' + str(index)) if is_array(variable) else ''),
                                        'initial_func' : 'localInitVal' + pascal_case(variable.name) + 'Location' + str(my_int) + (('Index' + str(index)) if is_array(variable) else ''),
                                        'field_name' : 'localBoard' + pascal_case(variable.name) + 'Location' + str(my_int) + (('Index' + str(index)) if is_array(variable) else ''),
                                        'partial_name' : 'partialBlackboard' + pascal_case(variable.name) + 'Location' + str(my_int) + (('Index' + str(index)) if is_array(variable) else ''),
                                        'type' : variable_type(variable),
                                        'default_arg' : get_default_arg(variable),
                                        'initial_value' : handle_initial_value(
                                            (cur_assign if ((not is_array(variable)) or cur_array_mode == 'range') else cur_assigns[index]),
                                            cur_type, 2, 'board',
                                            'partialBlackboard' + pascal_case(variable.name) + 'Location' + str(my_int) + (('Index' + str(index)) if is_array(variable) else ''),
                                            my_int, array_index = (index if is_array(variable) else None)),
                                        'model_as' : variable.model_as
                                    }
                                )
                            )
            elif current_node.node_type in {'check', 'environment_check'}:
                pass  # can't have local variables in checks.
            else:
                node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
                for child in node_children:
                    (cur_node_names, cur_node_names_map, running_dict, running_int, location_info, running_create_order, running_define_print_info) = walk_tree_recursive_blackboard(child, cur_node_names, cur_node_names_map, running_dict, running_int, location_info, running_create_order, running_define_print_info)
            return (
                (
                    (
                        cur_node_names,
                        cur_node_names_map,
                        running_dict,
                        running_int,
                        location_info,
                        running_create_order,
                        running_define_print_info
                    )
                )
            )

        (_, _, local_macros, _, location_info, running_create_order, running_define_print_info) = walk_tree_recursive_blackboard(model.root, set(), {}, {}, -1, [], [], [])
        create_order = [
            {
                'print_info' : get_print_info(variable, index, 'board', '', ((lambda x: str(x) + ' blackboard') if is_array(variable) else (lambda x: 'blackboard'))),
                'category_name' : 'board' + pascal_case(variable.name),
                'initial_name' : 'newVal' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'initial_func' : 'initVal' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'field_name' : 'board' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'partial_name' : 'partialBlackboard' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : handle_initial_value(
                    (variable.assign if ((not is_array(variable)) or variable.array_mode == 'range') else variable.assigns[index]),
                    variable_type(variable), 2, 'board',
                    'partialBlackboard' + pascal_case(variable.name) + (('Index' + str(index)) if is_array(variable) else ''),
                    None, array_index = (index if is_array(variable) else None)),
                'model_as' : variable.model_as
            }
            for variable in filter(lambda var: (var.model_as != 'DEFINE' and is_blackboard(var)), model.variables)
            for index in range(handle_constant(variable.array_size, False) if is_array(variable) else 1)
        ] + list(map(lambda x: x[1], filter(lambda x: not x[0], running_create_order))) + list(map(lambda x: x[1], filter(lambda x: x[0], running_create_order)))

        define_print_info = [
            get_print_info(variable, 0, 'board', '', ((lambda x: str(x) + ' blackboard') if is_array(variable) else (lambda x: 'blackboard')))
            for variable in filter(lambda var: (var.model_as =='DEFINE' and is_blackboard(var)), model.variables)
        ] + running_define_print_info
        local_var_to_nodes = {}
        for (variable, my_int) in location_info:
            name = variable.name
            if name in local_var_to_nodes:
                local_var_to_nodes[name].append(my_int)
            else:
                local_var_to_nodes[name] = [my_int]
        return handle_blackboard_environment(define_print_info, create_order, True, local_macros, local_var_to_nodes)

    function_format = {
        'loop' : ('', format_function_loop),
        'if' : ('', format_function_if),
        'abs' : ('abs', format_function_before),
        'max' : ('max', format_function_before),
        'min' : ('min', format_function_before),
        'sin' : ('sin', format_function_before),
        'cos' : ('cos', format_function_before),
        'tan' : ('tan', format_function_before),
        'ln' : ('log', format_function_before),
        'not' : ('not', format_function_before),
        'and' : ('&&', format_function_between),
        'or' : ('||', format_function_between),
        'xor' : ('sereneXOR', format_function_before),
        'xnor' : ('sereneXNOR', format_function_before),
        'imply' : ('sereneIMPLIES', format_function_before),
        'equiv' : ('==', format_function_between),
        'eq' : ('==', format_function_between),
        'neq' : ('/=', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('<=', format_function_between),
        'gte' : ('>=', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('*', format_function_between),
        'idiv' : ('quot', format_function_before),  # quot rounds to 0, which is what nuxmv does.
        'mod' : ('rem', format_function_before),  # rem matches the description of mod in the nuxmv user manual. do not use mod. will differ for negatives.
        'rdiv' : ('/', format_function_before),  # quot rounds to 0, which is what nuxmv does.
        'floor' : ('floor', format_function_before),
        'count' : ('sereneCOUNT', format_function_count),  # probably not usable now
        'index' : ('index', format_function_index)  # definitely not usable now
    }

    randomizer = (
        'module SereneRandomizer where' + os.linesep
        + 'import System.Random' + os.linesep
        + os.linesep
        + 'getGenerator :: Integer -> StdGen' + os.linesep
        + 'getGenerator seed = mkStdGen (fromInteger seed)' + os.linesep
        + os.linesep
        + 'getRandomInteger :: StdGen -> Integer -> (Integer, StdGen)' + os.linesep
        + 'getRandomInteger generator maxValue = (toInteger randomValue, newGenerator)' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + '(randomValue, newGenerator) = randomR (0, maxValue) generator' + os.linesep
        + os.linesep
    )

    standard_imports = (
        'import BehaviorTreeCore' + os.linesep
        + 'import BehaviorTreeBlackboard' + os.linesep
        + 'import BehaviorTreeEnvironment' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import SereneOperations' + os.linesep
        + os.linesep
    )

    serene_operations = (
        'module SereneOperations where' + os.linesep
        + os.linesep
        + 'sereneXOR :: Bool -> Bool -> Bool' + os.linesep
        + 'sereneXOR True True = False' + os.linesep
        + 'sereneXOR True False = True' + os.linesep
        + 'sereneXOR False True = True' + os.linesep
        + 'sereneXOR False False = False' + os.linesep
        + os.linesep
        + 'sereneXNOR :: Bool -> Bool -> Bool' + os.linesep
        + 'sereneXNOR True True = True' + os.linesep
        + 'sereneXNOR True False = False' + os.linesep
        + 'sereneXNOR False True = False' + os.linesep
        + 'sereneXNOR False False = True' + os.linesep
        + os.linesep
        + 'sereneIMPLIES :: Bool -> Bool -> Bool' + os.linesep
        + 'sereneIMPLIES True True = True' + os.linesep
        + 'sereneIMPLIES True False = False' + os.linesep
        + 'sereneIMPLIES False True = True' + os.linesep
        + 'sereneIMPLIES False False = True' + os.linesep
        + os.linesep
        + 'sereneCOUNT :: Bool -> Bool -> Integer' + os.linesep
        + 'sereneCOUNT True True = 2' + os.linesep
        + 'sereneCOUNT True False = 1' + os.linesep
        + 'sereneCOUNT False True = 1' + os.linesep
        + 'sereneCOUNT False False = 0' + os.linesep
        + os.linesep
    )

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('--max_iter', default = 100)
    # arg_parser.add_argument('--keep_names', action = 'store_true')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    (variables, constants, declared_enumerations) = validate_model(model)
    variable_type_map = {
        variable.name : to_haskell_type(variable_type(variable, declared_enumerations, constants))
        for variable in variables
    }
    variable_array_size_map = {
        variable.name : variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references)
        for variable in variables if is_array(variable)
    }
    variable_stages = {}  # this will be used to handle names and make updates more efficient.
    arguments = set()
    loop_references = {}

    my_location = args.location + 'app/'

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/haskell_file/BehaviorTreeCore.hs', my_location + 'BehaviorTreeCore.hs')

    with open(my_location + 'SereneRandomizer.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(randomizer)

    with open(my_location + 'SereneOperations.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(serene_operations)

    with open(my_location + 'BehaviorTreeEnvironment.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_environment(model))

    with open(my_location + 'BehaviorTreeBlackboard.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_blackboard(model))

    with open(my_location + pascal_case(args.output_file) + '.hs', 'w', encoding='utf-8') as write_file:
        (seen_nodes, to_write) = create_tree(model, args.output_file)
        write_file.write(to_write)

    with open(my_location + 'Main.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_runner(model, args.output_file, args.max_iter))

    for action in model.action_nodes:
        if action.name in seen_nodes:
            arguments = {argument_pair.argument_name for argument_pair in action.arguments}
            with open(my_location + 'BTree' + pascal_case(action.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_action_node(action))
            arguments = set()
    for check in model.check_nodes:
        if check.name in seen_nodes:
            arguments = {argument_pair.argument_name for argument_pair in check.arguments}
            with open(my_location + 'BTree' + pascal_case(check.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_check_node(check))
            arguments = set()
    for environment_check in model.environment_checks:
        if environment_check.name in seen_nodes:
            arguments = {argument_pair.argument_name for argument_pair in environment_check.arguments}
            with open(my_location + 'BTree' + pascal_case(environment_check.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_environment_check_node(environment_check))
            arguments = set()

    return


if __name__ == '__main__':
    dsl_to_haskell()
