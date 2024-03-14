'''
This module is for internal use with BehaVerify.
It is used to create Haskell code from BehaVerify DSL for Behavior Trees.
It contains a variety of utility functions.

Author: Serena Serafina Serbinowska
Last Edit: 2024-03-14
'''
import argparse
import os
import shutil
import itertools
from behaverify_common import haskell_indent as indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type, BTreeException, constant_type
from serene_functions import build_meta_func
from check_grammar import validate_model


def dsl_to_haskell(metamodel_file, model_file, location, output_name, max_iter, recursion_limit):
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

    def get_default_value(variable):
        the_type = variable_type_map[variable.name]
        value = ('0' if the_type == 'Integer' else ('True' if the_type == 'Bool' else '" "'))
        if is_array(variable):
            return '(' + ', '.join([value] * variable_array_size_map[variable.name]) + ')'
        return value

    def str_conversion(atom_type, atom):
        if atom_type in ('VARIABLE', 'NODE'):
            return str(atom)
        if atom_type == 'CONSTANT':
            atom_type = constant_type(atom, declared_enumerations)
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

    def format_case_loop_recursive(function_call, misc_args, cond_func, values, index):
        if len(values) == index:
            if function_call.loop_variable in loop_references:
                loop_references.pop(function_call.loop_variable)
            return format_code(function_call.default_value, misc_args)
        loop_references[function_call.loop_variable] = values[index]
        if not cond_func((constants, loop_references))[0]:
            return format_case_loop_recursive(function_call, misc_args, cond_func, values, index + 1)
        return ['(if ' + format_code(function_call.cond_value, misc_args)[0] + ' then ' + format_code(function_call.values[0], misc_args)[0] + ' else ' + format_case_loop_recursive(function_call, misc_args, cond_func, values, index + 1)[0] + ')']

    def format_function_case_loop(_, function_call, misc_args):
        all_domain_values = []
        if function_call.min_val is None:
            for domain_code in function_call.loop_variable_domain:
                for domain_value in execute_code(domain_code):
                    resolved = resolve_potential_reference_no_type(domain_value, declared_enumerations, {}, variables, constants, loop_references)
                    all_domain_values.append(resolved[1])
        else:
            (min_val, max_val) = get_min_max(function_call.min_val, function_call.max_val, declared_enumerations, {}, variables, constants, loop_references)
            all_domain_values = range(min_val, max_val + 1)
        if function_call.reverse:
            all_domain_values = list(reversed(all_domain_values))
        cond_func = build_meta_func(function_call.loop_condition)
        return format_case_loop_recursive(function_call, misc_args, cond_func, all_domain_values, 0)

    def format_function_before(function_name, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) == 1:
            return ['(' + function_name + ' ' + formatted_values[0] + ')']
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

    def format_function_count(_, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) == 1:
            return ['(if ' + formatted_values + ' then 1 else 0)']
        return [
            '('
            + ' + '.join([('(sereneCOUNT ' + formatted_values[2 * index] + ' ' + formatted_values[(2 * index) + 1] + ')') for index in range(len(formatted_values)//2)])
            + (
                ''
                if len(formatted_values) % 2 == 0 else
                (' + (if ' + formatted_values[-1] + ' then 1 else 0)')
            )
            + ')'
        ]

    def format_function_index(_, function_call, misc_args):
        variable = resolve_potential_reference_no_type(execute_code(function_call.to_index)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        if function_call.constant_index == 'constant_index':
            index = str(resolve_potential_reference_no_type(execute_code(function_call.values[0])[0], declared_enumerations, {}, variables, constants, loop_references)[1])
        else:
            index = format_code(function_call.values[0], misc_args)[0]
        return [
            '(indexInto' + pascal_case(variable.name) + ' ' + index + ' ' + format_variable(variable)+ ')'
        ]

    def format_function(code, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.'''
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def create_misc_args(init_mode, indent_level):
        return {
            'init_mode' : init_mode,  # 'env', 'board', or None
            'indent_level' : indent_level
        }

    def format_variable(variable):
        prefix = 'env' if is_env(variable) else 'board'
        arguments = ('blackboard environment' if variable.model_as == 'DEFINE' else 'environment') if is_env(variable) else ('nodeLocation blackboard' if is_local(variable) else 'blackboard')
        return '(' + prefix + pascal_case(variable.name) + ' ' + arguments + ')'

    def handle_atom(code):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException:
            return code.atom.reference
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom)

    def format_code(code, misc_args):
        return (
            [handle_atom(code)] if code.atom is not None else (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)] if code.code_statement is not None else (
                    format_function(code, misc_args)
                )
            )
        )

    def handle_case_result(case_result, converted_variable_type, misc_args):
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
        counters['random'] += 1
        random_length = len(formatted_values)
        value_string = ''
        indent_level = misc_args['indent_level']
        function_name = 'randomNumberToResult' + str(counters['random'])
        value_string = function_name + ' (fst randomPair' + str(counters['random']) + ')'
        where_string = (
            indent(indent_level + 2) + function_name + ' :: Integer -> ' + converted_variable_type + os.linesep
            + ''.join([
                (indent(indent_level + 2) + function_name + ' ' + str(index) + ' = ' + value + os.linesep)
                for (index, value) in enumerate(formatted_values)
            ])
            + (indent(indent_level + 2) + function_name + ' value = error ("' + function_name + ' illegal value: " ++ (show value))' + os.linesep)
        )
        return (condition_string, value_string, where_string, counters['random'], random_length)

    def handle_assign(assign, converted_variable_type, misc_args):
        return [handle_case_result(case_result, converted_variable_type, misc_args) for case_result in assign.case_results] + [handle_case_result(assign.default_result, converted_variable_type, misc_args)]

    def handle_loop_array_index(packed_args, misc_args):
        (loop_array_index, converted_variable_type, constant_index) = packed_args
        if loop_array_index.array_index is not None:
            results = handle_assign(loop_array_index.array_index.assign, converted_variable_type, misc_args)
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
        return execute_loop(loop_array_index, handle_loop_array_index, (loop_array_index.loop_array_index, converted_variable_type, constant_index), misc_args)

    def handle_formatted_results(new_name, results, indent_level):
        return_string = indent(indent_level) + new_name + os.linesep
        where_string = indent(indent_level + 1) + 'where' + os.linesep
        needs_where = False
        for (condition, value, where, pair_num, random_length) in results:
            return_string += indent(indent_level + 1) + '| ' + condition + ' = ' + value + os.linesep
            where_string += where
            if random_length > 1:
                needs_where = True
                where_string += indent(indent_level) + 'randomPair' + str(pair_num) + ' = getRandomInteger (snd randomPair' + str(pair_num - 1) + ') ' + str(random_length - 1) + os.linesep
        if len(results) == 1:
            return_string = (indent(indent_level) + new_name + ' = ' + results[0][1] + os.linesep)
        return return_string + (where_string if needs_where else '')

    def handle_variable_statement(variable_statement, statement_number, misc_args):
        counters['random'] = 0
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        converted_variable_type = to_haskell_type(variable_type(assign_var, declared_enumerations, constants))
        indent_level = misc_args['indent_level']
        return_string = (
            indent(indent_level) + 'statement' + str(statement_number) + (' :: BTreeBlackboard -> BTreeBlackboard' if misc_args['init_mode'] == 'board' else ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)') + os.linesep
            + indent(indent_level) + 'statement' + str(statement_number) + (' blackboard = ' if misc_args['init_mode'] == 'board' else ' (blackboard, environment)  = ')
            + (
                ('(blackboard, envUpdate' + pascal_case(assign_var.name) + ' environment newGenerator newVal)')
                if is_env(assign_var) else
                (
                    (
                        ('boardUpdate' + pascal_case(assign_var.name) + ' nodeLocation blackboard newGenerator newVal')
                        if is_local(assign_var) else
                        ('boardUpdate' + pascal_case(assign_var.name) + ' blackboard newGenerator newVal')
                    )
                    if misc_args['init_mode'] == 'board' else
                    (
                        ('(boardUpdate' + pascal_case(assign_var.name) + ' nodeLocation blackboard newGenerator newVal, environment)')
                        if is_local(assign_var) else
                        ('(boardUpdate' + pascal_case(assign_var.name) + ' blackboard newGenerator newVal, environment)')
                    )
                )
            )
            + os.linesep
            + indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + 'randomPair0 = (-1, ' + ('env' if is_env(assign_var) else 'board') + 'Generator ' + ('environment' if is_env(assign_var) else 'blackboard') + ')' + os.linesep
        )
        new_misc_args = create_misc_args(misc_args['init_mode'], indent_level + 2)
        if is_array(assign_var):
            if assign_var.iterative_assign == 'iterative_assign':
                iterative_condition_assign_list = [(build_meta_func(iterative_assign_conditional.condition), iterative_assign_conditional.assign) for iterative_assign_conditional in variable_statement.iterative_assign_conditionals]
                index_var_name = variable_statement.index_var_name
                return_string = ''
                for index in range(variable_array_size_map[assign_var.name]):
                    loop_references[index_var_name] = index
                    need_default = True
                    for (condition_func, assign) in iterative_condition_assign_list:
                        if condition_func((constants, loop_references))[0]:
                            results = handle_assign(assign, variable_type_map[assign_var.name], new_misc_args)
                            need_default = False
                            break
                    if need_default:
                        results = handle_assign(variable_statement.assign, variable_type_map[assign_var.name], new_misc_args)
                    return_string += handle_formatted_results('newValue' + str(index), results, indent_level + 2)
                return_string += indent(indent_level + 2) + 'newValue = (' + ', '.join(['newValue' + str(index) for index in range(variable_array_size_map[assign_var.name])]) + ')' + os.linesep
                loop_references.pop(index_var_name)
                return return_string
            meta_results = []
            for loop_array_index in variable_statement.assigns:
                meta_results.extend(handle_loop_array_index((loop_array_index, converted_variable_type, variable_statement.constant_index), new_misc_args))
            update_pair_strings = []
            for (num, (indices, results)) in enumerate(meta_results):
                return_string += handle_formatted_results('newUpdate' + str(num), results, indent_level + 2)
                for index in indices:
                    update_pair_strings.append('(' + index + ', ' + 'newUpdate' + str(num) + ')')
            if misc_args['init_mode'] in ('board', 'env'):
                for index in range(variable_array_size_map[assign_var.name]):
                    results = handle_assign(variable_statement.default_value, variable_type_map[assign_var.name], new_misc_args)
                    return_string += handle_formatted_results('defaultValue' + str(index), results, indent_level + 2)
                return_string += indent(indent_level + 2) + 'defaultValue = (' + ', '.join(['defaultValue' + str(index) for index in range(variable_array_size_map[assign_var.name])]) + ')' + os.linesep
            else:
                return_string += indent(indent_level + 2) + 'defaultValue = ' + format_variable(assign_var) + os.linesep
            return (
                return_string
                + indent(indent_level + 2) + 'newGenerator = snd randomPair' + str(counters['random']) + os.linesep
                + indent(indent_level + 2) + 'newVal = newArray' + pascal_case(assign_var.name) + ' defaultValue [' + ', '.join(update_pair_strings) + ']'
                + os.linesep
            )
        results = handle_assign(variable_statement.assign, converted_variable_type, new_misc_args)
        return (
            return_string
            + indent(indent_level + 2) + 'newGenerator = snd randomPair' + str(counters['random']) + os.linesep
            + handle_formatted_results('newVal', results, indent_level + 2)
        )

    def handle_read_statement(read_statement, statement_number, misc_args):
        indent_level = misc_args['indent_level']
        return_string = ''
        cond_var = read_statement.condition_variable
        condition = format_code(read_statement.condition, misc_args)[0]
        return_string = (
            indent(indent_level) + 'statement' + str(statement_number) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
            + indent(indent_level) + 'statement' + str(statement_number) + ' (preBlackboard, environment) = (newBlackboard, newEnvironment)' + os.linesep
            + indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + '(newBlackboard, newEnvironment) = if condition then ' + ''.join(['(statement' + str(statement_number + 1 + index) + ' ' for index in reversed(range(len(read_statement.variable_statements)))]) + '(blackboard, environment)' + ')' * len(read_statement.variable_statements) + ' else (blackboard, environment)' + os.linesep
        )
        if read_statement.non_determinism == 'non_determinism':
            return_string += (
                indent(indent_level + 2) + 'condPair = getRandomInteger (boardGenerator preBlackboard 1)' + os.linesep
                + indent(indent_level) + 'condition = (' + condition + ') && ((fst condPair) == 1)' + os.linesep
            )
        else:
            return_string += (
                indent(indent_level + 2) + 'condPair = (-1, boardGenerator preBlackboard)' + os.linesep
                + indent(indent_level + 2) + 'condition = ' + condition + os.linesep
            )
        if cond_var is not None:
            return_string += indent(indent_level + 2) + 'blackboard = boardUpdate' + pascal_case(cond_var.name) + (' nodeLocation ' if is_local(cond_var.name) else ' ') + 'preBlackboard (snd condPair) condition' + os.linesep
        else:
            return_string += indent(indent_level + 2) + 'blackboard = boardUpdate preBlackboard (snd condPair)' + os.linesep
        new_misc_args = create_misc_args(misc_args['init_mode'], indent_level + 2)
        for (index, variable_statement) in enumerate(read_statement.variable_statements):
            return_string += handle_variable_statement(variable_statement, statement_number + 1 + index, new_misc_args)
        return return_string

    def handle_write_statement(write_statement, statement_number, misc_args):
        return_string = ''
        delay_queue = []
        index = 0
        for variable_statement in write_statement.update:
            if variable_statement.instant:
                return_string += handle_variable_statement(variable_statement, statement_number + index, misc_args)
                index = index + 1
            else:
                delay_queue.append(variable_statement)
        return (return_string, delay_queue, index)

    def format_returns(status_result):
        return status_result.status.capitalize()

    def handle_return_statement(return_statement, misc_args):
        indent_level = misc_args['indent_level']
        return_string = (
            indent(indent_level) + 'returnStatusFunction :: BTreeBlackboard -> BTreeEnvironment -> BTreeNodeStatus' + os.linesep
            + indent(indent_level) + 'returnStatusFunction blackboard environment = returnStatus' + os.linesep
            + indent(indent_level + 1) + 'where' + os.linesep
        )
        if len(return_statement.case_results) == 0:
            return (
                return_string
                + indent(indent_level + 2) + 'returnStatus = ' + format_returns(return_statement.default_result) + os.linesep
            )
        return (
            return_string
            + indent(indent_level + 2) + 'returnStatus' + os.linesep
            + ''.join(
                [
                    (indent(indent_level + 3) + '| ' + format_code(case_result.condition, create_misc_args(init_mode = False, indent_level = indent_level + 3))[0] + ' = ' + format_returns(case_result) + os.linesep)
                    for case_result in return_statement.case_results
                ]
            )
            + indent(indent_level + 3) + '| otherwise = ' + format_returns(return_statement.default_result) + os.linesep
        )

    def handle_statement(statement, statement_number, misc_args):
        return (
            (handle_variable_statement(statement.variable_statement, statement_number, misc_args), [], 1)
            if statement.variable_statement is not None else
            (
                (handle_read_statement(statement.read_statement, statement_number, misc_args), [], 1)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, statement_number, misc_args)
            )
        )

    def module_declaration(node_name):
        return 'module BTree' + pascal_case(node_name) + ' where' + os.linesep

    def check_function(node):
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
            + indent(1 + indent_modifier) + '| ' + format_code(node.condition, None)[0] + ' = (Success, [], [], blackboard, environment, futureChanges)' + os.linesep
            + indent(1 + indent_modifier) + '| otherwise = (Failure, [], [], blackboard, environment, futureChanges)'
        )

    def between_tick_update(updates):
        indent_modifier = 0
        return_string = ''
        for (index, statement) in enumerate(updates):
            return_string += handle_variable_statement(statement, index, create_misc_args(None, 2 + indent_modifier))
        return (
            'betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
            + 'betweenTickUpdate (blackboard, environment) = (newBlackboard, newEnvironment)' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2 + indent_modifier) + '(newBlackboard, newEnvironment) = ' + ''.join(['(statement' + str(index) + ' ' for index in reversed(range(len(updates)))]) + '(blackboard, environment)' + ')' * len(updates) + os.linesep
            + return_string
        )

    def action_function(node):
        indent_modifier = 2 if len(node.arguments) > 0 else 0
        return_string = ''
        delayed_updates = []
        statement_number = 0
        for statement in node.pre_update_statements:
            temp = handle_statement(statement, statement_number, create_misc_args(None, 2 + indent_modifier))
            return_string += temp[0]
            delayed_updates.extend(temp[1])
            statement_number = statement_number + temp[2]
        mid_point_number = statement_number
        return_string += handle_return_statement(node.return_statement, create_misc_args(None, 2 + indent_modifier))
        for statement in node.post_update_statements:
            temp = handle_statement(statement, statement_number, create_misc_args(None, 2 + indent_modifier))
            return_string += temp[0]
            delayed_updates.extend(temp[1])
            statement_number = statement_number + temp[2]
        for (index, delayed) in enumerate(delayed_updates):
            return_string += (
                indent(2 + indent_modifier) + 'futureChanges' + str(index) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                + indent(2 + indent_modifier) + 'futureChanges' + str(index) + ' = statement0' + os.linesep
                + indent(3 + indent_modifier) + 'where' + os.linesep
                + handle_variable_statement(delayed, 0, create_misc_args(None, 4 + indent_modifier))
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
            + indent(2 + indent_modifier) + 'returnStatus = returnStatusFunction midBlackboard midEnvironment' + os.linesep
            + indent(2 + indent_modifier) + '(newBlackboard, newEnvironment) = ' + ''.join(['(statement' + str(index) + ' ' for index in reversed(range(mid_point_number, statement_number))]) + '(midBlackboard, midEnvironment)' + ')' * (statement_number - mid_point_number) + os.linesep
            + indent(2 + indent_modifier) + 'newFutureChanges = ' + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, reversed(range(len(delayed_updates)))))) + (' : ' if len(delayed_updates) > 0 else '') + 'futureChanges' + os.linesep
            + indent(2 + indent_modifier) + '(midBlackboard, midEnvironment) = ' + ''.join(['(statement' + str(index) + ' ' for index in reversed(range(mid_point_number))]) + '(blackboard, environment)' + ')' * mid_point_number + os.linesep
            + return_string
        )

    def build_check_node(node):
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + check_function(node)
                )

    def build_environment_check_node(node):
        return build_check_node(node)

    def build_action_node(node):
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + action_function(node)
                )

    def create_runner(model, name, max_iter):
        '''creates the runner for haskell code'''
        current_node = model.root
        while True:
            if hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
                continue
            current_name = current_node.leaf.name if current_node.name is None else current_node.name
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            break
        root_name = current_name
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
                    ('(' + 'xISyCreator ' + str(node.x).capitalize() + ' ' + str(node.y).capitalize() + ')')
                )
                + ')'
            )

        def walk_tree_recursive(current_node, seen_nodes, node_names, running_string, running_int, indent_level):
            current_args = None
            while  hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
            current_name = current_node.name if hasattr(current_node, 'name') and current_node.name is not None else current_node.leaf.name
            current_args = (current_node.arguments if hasattr(current_node, 'arguments') else None)
            current_node = (current_node.leaf if hasattr(current_node, 'leaf') else current_node)

            node_name = 'bTreeNode' + pascal_case(current_name)
            cur_node_names = {node_name}.union(node_names)
            running_int = running_int + 1
            my_int = running_int
            node_names_to_node_locations[current_node.name] = my_int
            if current_node.node_type in ('check', 'environment_check', 'action'):
                seen_nodes.add(current_node.name)
                has_args = len(current_node.arguments) > 0
                running_string = running_string + (
                    indent(indent_level) + node_name + ' = BTreeNode '
                    + ('(' if has_args else '') + 'bTreeFunction' + ('Creator' if has_args else '') + pascal_case(current_node.name)
                    + ((' ' + ' '.join(['(' + str_conversion(*resolve_potential_reference_no_type(val, declared_enumerations, {}, variables, constants, loop_references)) + ')' for cur_arg in current_args for val in execute_code(cur_arg)]) + ')') if has_args else '')
                    + ' [] ' + str(my_int) + os.linesep
                )
            else:
                child_names = []
                node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
                for child in node_children:
                    (child_name, seen_nodes, cur_node_names, running_string, running_int, indent_level) = walk_tree_recursive(child, seen_nodes, cur_node_names, running_string, running_int, indent_level)
                    child_names.append(child_name)
                running_string = running_string + (
                    indent(indent_level) + node_name + ' = BTreeNode ' + node_function(current_node) + ' ' + '[' + ', '.join(child_names) + '] ' + str(my_int) + os.linesep
                )
            return (
                node_name,
                seen_nodes,
                cur_node_names,
                running_string,
                running_int,
                indent_level
            )

        (_, seen_nodes,  _, node_declarations, _, _) = walk_tree_recursive(model.root, set(), set(), '', -1, 0)

        return (
            seen_nodes,
            (
                'module ' + pascal_case(name) + ' where' + os.linesep
                + 'import BehaviorTreeCore' + os.linesep
                + ''.join([('import BTree' + pascal_case(node.name) + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks) if node.name in seen_nodes])
                + node_declarations
            )
        )

    def create_macro(variable_statement, node_location, misc_args):
        counters['random'] = 0
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        indent_level = misc_args['indent_level']
        if is_array(assign_var):
            type_signature = '(' + ', '.join([variable_type_map[assign_var.name]] * variable_array_size(assign_var, declared_enumerations, {}, variables, constants, loop_references)) + ')'
        else:
            type_signature = variable_type_map[assign_var.name]
        return_string = (
            indent(indent_level) + ('env' if is_env(assign_var) else 'board') + pascal_case(assign_var.name) + (('Location' + str(node_location)) if node_location is not None else '')
            + ' :: BTreeBlackboard ' + ('-> BTreeEnvironment' if is_env(assign_var) else '') + ' -> ' + type_signature + os.linesep
            + indent(indent_level) + ('env' if is_env(assign_var) else 'board') + pascal_case(assign_var.name) + (('Location' + str(node_location)) if node_location is not None else '')
            + (' blackboard environment' if is_env(assign_var) else ' blackboard') + ' = newVal' + os.linesep
            + indent(indent_level + 1) + 'where' + os.linesep
        )
        new_misc_args = create_misc_args(misc_args['init_mode'], indent_level + 2)
        if is_array(assign_var):
            meta_results = []
            for loop_array_index in variable_statement.assigns:
                meta_results.extend(handle_loop_array_index((loop_array_index, variable_type_map[assign_var.name], variable_statement.constant_index), new_misc_args))
            update_pair_strings = []
            for (num, (indices, results)) in enumerate(meta_results):
                return_string += handle_formatted_results('newUpdate' + str(num), results, indent_level + 2)
                for index in indices:
                    update_pair_strings.append('(' + index + ', ' + 'newUpdate' + str(num) + ')')
            for index in range(variable_array_size_map[assign_var.name]):
                results = handle_assign(variable_statement.default_value, variable_type_map[assign_var.name], new_misc_args)
                return_string += handle_formatted_results('defaultValue' + str(index), results, indent_level + 2)
            return_string += indent(indent_level + 2) + 'defaultValue = (' + ', '.join(['defaultValue' + str(index) for index in range(variable_array_size_map[assign_var.name])]) + ')' + os.linesep
            return (
                return_string
                + indent(indent_level + 2) + 'newVal = newArray' + pascal_case(assign_var.name) + ' defaultValue [' + ', '.join(update_pair_strings) + ']'
                + os.linesep
            )
        results = handle_assign(variable_statement.assign, variable_type_map[assign_var.name], new_misc_args)
        return (
            return_string
            + handle_formatted_results('newVal', results, indent_level + 2)
        )

    # def safe_update(variable, env_mode, local_mode, local_numbers = None):
    #     local_numbers = ([] if local_numbers is None else local_numbers)
    #     function_name = (
    #         (
    #             'updateEnv'
    #             if env_mode
    #             else
    #             (
    #                 'localUpdateBoard'
    #                 if local_mode
    #                 else
    #                 'updateBoard'
    #             )
    #         )
    #         + pascal_case(variable.name)
    #     )
    #     arg_type = (
    #         'BTreeEnvironment'
    #         if env_mode
    #         else
    #         (
    #             'Integer -> BTreeBlackboard'
    #             if local_mode
    #             else
    #             'BTreeBlackboard'
    #         )
    #     )
    #     return_type = (
    #         'BTreeEnvironment'
    #         if env_mode
    #         else
    #         'BTreeBlackboard'
    #     )
    #     board_type = (
    #         'environment'
    #         if env_mode
    #         else
    #         'blackboard'
    #     )
    #     field_name = (
    #         (
    #             'env'
    #             if env_mode
    #             else
    #             (
    #                 'localBoard'
    #                 if local_mode
    #                 else
    #                 'board'
    #             )
    #         )
    #         + pascal_case(variable.name)
    #     )
    #     return (
    #         function_name + ' :: ' + arg_type + ' -> ' + variable_type(variable) + ' -> ' + return_type + os.linesep
    #         + (
    #             (
    #                 function_name + (' _ ' if local_mode else ' ') + board_type + ' _ = ' + board_type + os.linesep
    #             )
    #             if variable.model_as == 'FROZENVAR'
    #             else
    #             (
    #                 (
    #                     ''.join(
    #                         [
    #                             (function_name + ' ' + str(number) + ' ' + board_type + ' value = ' + board_type + ' { ' + field_name + str(number) + ' = value }' + os.linesep)
    #                             if variable.domain.boolean is not None or variable.domain.min_val is None
    #                             else
    #                             (
    #                                 (
    #                                     ''.join(
    #                                         map(
    #                                             lambda value :
    #                                             (function_name + ' ' + str(number) + ' ' + board_type + ' ' + handle_constant(value, True) + ' = ' + board_type + ' { ' + field_name + str(number) + ' = ' + handle_constant(value, True) + ' }' + os.linesep)
    #                                             ,
    #                                             variable.domain.enums
    #                                         )
    #                                     )
    #                                     + (function_name + ' ' + str(number) + ' _ _ = error "' + variable.name + ' illegal value"' + os.linesep)
    #                                 )
    #                                 if variable.domain.min_val is None
    #                                 else
    #                                 (
    #                                     function_name + ' ' + str(number) + ' ' + board_type + ' value' + os.linesep
    #                                     + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "local ' + variable.name + ' illegal value"' + os.linesep
    #                                     + indent(1) + '| otherwise = ' + board_type + ' { ' + field_name + str(number) + ' = value }' + os.linesep
    #                                 )
    #                             )
    #                             for number in local_numbers
    #                         ]
    #                     )
    #                     + (function_name + ' _ _ _ = error "' + variable.name + ' illegal local reference"' + os.linesep)
    #                 )
    #                 if local_mode
    #                 else
    #                 (
    #                     (function_name + ' ' + board_type + ' value = ' + board_type + ' { ' + field_name + ' = value }' + os.linesep)
    #                     if variable.domain.boolean is not None
    #                     else
    #                     (
    #                         (
    #                             ''.join(
    #                                 map(
    #                                     lambda value :
    #                                     (function_name + ' ' + board_type + ' ' + handle_constant(value, True) + ' = ' + board_type + ' { ' + field_name + ' = ' + handle_constant(value, True) + ' }' + os.linesep)
    #                                     ,
    #                                     variable.domain.enums
    #                                 )
    #                             )
    #                             + (function_name + ' _ _ = error "' + variable.name + ' illegal value"' + os.linesep)
    #                         )
    #                         if variable.domain.min_val is None
    #                         else
    #                         (
    #                             function_name + ' ' + board_type + ' value' + os.linesep
    #                             + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "' + variable.name + ' illegal value"' + os.linesep
    #                             + indent(1) + '| otherwise = ' + board_type + ' { ' + field_name + ' = value }' + os.linesep
    #                         )
    #                     )
    #                 )
    #             )
    #         )
    #         + os.linesep
    #     )

    # def create_check_value(variable):
    #     function_name = (
    #         (
    #             'checkValueEnv'
    #             if is_env(variable)
    #             else
    #             (
    #                 'checkValueLocalBoard'
    #                 if is_local(variable)
    #                 else
    #                 'checkValueBoard'
    #             )
    #         )
    #         + pascal_case(variable.name)
    #     )
    #     board_type = 'environment' if is_env(variable) else 'blackboard'
    #     field_name = (
    #         (
    #             'env'
    #             if is_env(variable)
    #             else
    #             (
    #                 'localBoard'
    #                 if is_local(variable)
    #                 else
    #                 'board'
    #             )
    #         )
    #         + pascal_case(variable.name)
    #     )
    #     return (
    #         function_name + ' :: ' + variable_type_map[variable.name] + ' -> ' + variable_type_map[variable.name] + os.linesep
    #         + (
    #             (function_name + ' value = value' + os.linesep)
    #             if variable.domain.boolean is not None or variable.domain.true_int is not None
    #             else
    #             (
    #                 (
    #                     ''.join(
    #                         map(
    #                             lambda value :
    #                             (function_name + ' ' + handle_constant(value, True) + ' = ' + handle_constant(value, True) + os.linesep)
    #                             ,
    #                             variable.domain.enums
    #                         )
    #                     )
    #                     + (function_name + ' _ = error "' + field_name + ' illegal value"' + os.linesep)
    #                 )
    #                 if variable.domain.min_val is None
    #                 else
    #                 (
    #                     function_name + ' value' + os.linesep
    #                     + indent(1) + '| ' + handle_constant(variable.domain.min_val, True) + ' > value || value > ' + handle_constant(variable.domain.max_val, True) + ' = error "' + field_name + ' illegal value"' + os.linesep
    #                     + indent(1) + '| otherwise = value' + os.linesep
    #                 )
    #             )
    #         )
    #         + os.linesep
    #     )

    def array_set_creator(variable):
        var_type = variable_type_map[variable.name]
        var_array_size = variable_array_size_map[variable.name]
        return (
            'newArray' + pascal_case(variable.name) + ' :: (' + ', '.join([var_type] * var_array_size) + ') -> [(Integer, ' + var_type + ')] -> (' + ', '.join([var_type] * var_array_size) + ')' + os.linesep
            + 'newArray' + pascal_case(variable.name) + ' values  []  = values' + os.linesep  # no update
            + 'newArray' + pascal_case(variable.name) + ' (' + ', '.join(['value' + str(index) for index in range(var_array_size)]) + ') indicesValues = updateValues indicesValues' + os.linesep
            + indent(2) + 'where' + os.linesep
            # each of the new values is equal based on updateValues
            # updateValues is a function which goes through an for each step in the list changes one value. It is ordered in a specific way
            # suppose we have [(1, 'a'), (2, 'b'), (1, 'c'), (3, 'd')]
            # then we want this to update index 1 to a, 2 to b, and 3 to d, and ignore the 1=c option.
            # therefore, we use recursion.
            + indent(3) + 'updateValues :: [(Integer, ' + var_type + ')] -> (' + ', '.join([var_type] * var_array_size) + ')' + os.linesep
            + indent(3) + 'updateValues [] = (' + ', '.join(['value' + str(index) for index in range(var_array_size)]) + ')' + os.linesep # in the base case, just grab what the current value is.
            + ''.join(
                [
                    (
                        indent(3) + 'updateValues ((' + str(index) + ', currentValue) : nextIndicesValues) = ('
                        + ', '.join([('currentValue' if sub_index == index else ('updatedValue' + str(sub_index))) for sub_index in range(var_array_size)])
                        + ')' + os.linesep
                        + indent(4) + 'where' + os.linesep
                        + indent(5) + '(' + ', '.join([('_' if sub_index == index else ('updatedValue' + str(sub_index))) for sub_index in range(var_array_size)]) + ') = updateValues nextIndicesValues' + os.linesep
                    )
                    for index in range(var_array_size)
                ]
            )
        )

    def create_initial_statements(blackboard_mode, local_initial_statements):
        initial_statements = []
        statement_number = 0
        misc_args = create_misc_args('board' if blackboard_mode else 'env', 2)
        for variable in model.variables:
            if variable.model_as != 'DEFINE' and ((blackboard_mode and is_blackboard(variable)) or ((not blackboard_mode) and is_env(variable))):
                initial_statements.append(handle_variable_statement(variable, statement_number, misc_args))
                statement_number += 1
        for (node_location, define_var, statement) in local_initial_statements:
            if not define_var:
                initial_statements.append(handle_variable_statement(statement, statement_number, misc_args) + indent(4) + 'nodeLocation = ' + str(node_location) + os.linesep)
                statement_number += 1
        return (
            ''.join(initial_statements)
            + indent(2) + ('newBlackboard' if blackboard_mode else '(_, newEnvironment)') + ' = ' + ''.join(['(statement' + str(index) + ' ' for index in reversed(range(statement_number))]) + ('dummy' if blackboard_mode else '(blackboard, dummy)') + ')' * statement_number + os.linesep
        )

    def handle_blackboard_environment(blackboard_mode, local_initial_statements):
        def deal_with_variable(variable):
            return (is_blackboard(variable) or variable.name in local_var_to_nodes) if blackboard_mode else is_env(variable)
        data_type_name = 'BTreeBlackboard' if blackboard_mode else 'BTreeEnvironment'
        data_type_name_2 = 'BTreeBlackboard' if blackboard_mode else 'BTreeBlackboard -> BTreeEnvironment'
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
            + indent(1)
            + (os.linesep + indent(1) + ', ').join(
                [indent(1) + board_env + 'Generator :: StdGen']
                +
                [
                    (
                        (os.linesep + indent(1) + ', ').join(
                            [
                                ('board' + pascal_case(variable.name) + 'Location' + str(node_location) + ' :: ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name]) + ')') if is_array(variable) else variable_type_map[variable.name]))
                                for node_location in local_var_to_nodes[variable.name]
                            ]
                        )
                        if variable.name in local_var_to_nodes else
                        ''
                    )
                    if is_local(variable) else
                    (board_env + pascal_case(variable.name) + ' :: ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name]) + ')') if is_array(variable) else variable_type_map[variable.name]))
                    for variable in model.variables if variable.model_as != 'DEFINE' and deal_with_variable(variable)
                ]
            )
            + os.linesep
            + indent(1) + '}' + os.linesep + os.linesep
            + (
                'from' + data_type_name + 'ToString :: ' + data_type_name_2 + ' -> String' + os.linesep
                + 'from' + data_type_name + 'ToString ' + var_name_2 + ' = '
                + '"' + board_env + ' = {"'
                + ' ++ '
                + ' ++ ", " ++ '.join(
                    [
                        (
                            '"'
                            + (('env' + pascal_case(variable.name)) if is_env(variable) else ('board' + pascal_case(variable.name) + (('Location' + str(node_location)) if is_local(variable) else '')))
                            + ': " ++ '
                            + ('(show ' + (('(board' + pascal_case(variable.name) + 'Location' + str(node_location) + ' blackboard)') if is_local(variable) else format_variable(variable)) + ')')
                        )
                        for variable in model.variables if deal_with_variable(variable)
                        for node_location in (local_var_to_nodes[variable.name] if is_local(variable) else [None])
                    ]
                    +
                    ['"}"']
                ).replace('", " ++ "}"', '"}"')
                + os.linesep
            )
            # end of blackboard and show for the blackbord.
            + (
                (
                    os.linesep + '-- START OF GET FUNCTIONS FOR LOCAL VARIABLES' + os.linesep + os.linesep
                    + ''.join(
                        [
                            'board' + pascal_case(variable.name) + ' :: Integer -> BTreeBlackboard -> ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name]) + ')') if is_array(variable) else variable_type_map[variable.name]) + os.linesep
                            + ''.join(
                                [
                                    'board' + pascal_case(variable.name) + ' ' + str(node_location) + ' = board' + pascal_case(variable.name) + 'Location' + str(node_location) + os.linesep
                                    for node_location in local_var_to_nodes[variable.name]
                                ]
                            )
                            + 'board' + pascal_case(variable.name) + ' _ = error "illegal local reference: board' + pascal_case(variable.name) + '"' + os.linesep
                            for variable in model.variables if variable.name in local_var_to_nodes  # this intentionally does not have a != DEFINE clause. It sets up the define definitions below.
                        ]
                    )
                )
                if blackboard_mode
                else
                ''
            )
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF ' + ('BLACKBOARD' if blackboard_mode else 'ENVIRONMENT') + ' FUNCTIONS' + os.linesep + os.linesep
            + ''.join(
                [
                    create_macro(variable, None, create_misc_args(None, 0))
                    for variable in model.variables if (variable.model_as == 'DEFINE' and is_non_local(variable))
                ]
            )
            # created accessor functions for define non-local ---------------------------------------------------------------------------------------
            + (
                (
                    os.linesep + '-- START OF LOCAL BLACKBOARD FUNCTIONS' + os.linesep + os.linesep
                    + ''.join(
                        [
                            create_macro(statement, node_location, create_misc_args(None, 0))
                            for (node_location, define_var, statement) in local_initial_statements if define_var
                        ]
                    )
                    # created accessor functions for define local
                    # ---------------------------------------------------------------------------------------
                )
                if blackboard_mode
                else
                ''
            )
            + os.linesep + '-- START OF INDEX FUNCTIONS FOR ARRAYS' + os.linesep + os.linesep
            # we don't need a special case for indexing local variables
            # each node location is indexed the same way.
            + ''.join(
                [
                    'indexInto' + pascal_case(variable.name) + ' :: Integer -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ') -> ' + variable_type_map[variable.name] + os.linesep
                    + ''.join(
                        [
                            ('indexInto' + pascal_case(variable.name) + ' ' + str(index) + ' (' + ', '.join(['_'] * index + ['value'] + ['_'] * (variable_array_size_map[variable.name] - index - 1)) + ') = value' + os.linesep)
                            for index in range(variable_array_size_map[variable.name])
                        ]
                    )
                    + 'indexInto' + pascal_case(variable.name) + ' _ _ = error "indexInto' + pascal_case(variable.name) + ' illegal index value"' + os.linesep
                    for variable in model.variables if is_array(variable) and deal_with_variable(variable)# and (not is_local(variable))
                ]
            )
            # + ''.join(
            #     [
            #         'indexInto' + pascal_case(variable.name) + ' :: Integer -> Integer -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ') -> ' + variable_type_map[variable.name] + os.linesep
            #         + ''.join(
            #             [
            #                 'indexInto' + pascal_case(variable.name) + ' ' + str(node_location) + ' = indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + os.linesep
            #                 for node_location in local_var_to_nodes[variable.name]
            #             ]
            #         )
            #         + 'indexInto' + pascal_case(variable.name) + ' _ = error "indexInto' + pascal_case(variable.name) + ' illegal local value"' + os.linesep
            #         + ''.join(
            #             [
            #                 'indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' :: Integer -> (' + ', '.join([variable_type_map[variable.name]] * variable_array_size(variable, declared_enumerations, {}, variables, constants, loop_references))  + ') -> ' + variable_type_map[variable.name] + os.linesep
            #                 + ''.join(
            #                     [
            #                         ('indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' ' + str(index) + ' (' + ', '.join(['_'] * index + ['value'] + ['_'] * (variable_array_size_map[variable.name] - index - 1)) + ') = value' + os.linesep)
            #                         for index in range(variable_array_size_map[variable.name])
            #                     ]
            #                 )
            #                 + 'indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' _ _ = error "indexInto' + pascal_case(variable.name) + 'Location' + str(node_location) + ' illegal index value"' + os.linesep
            #                 for node_location in local_var_to_nodes[variable.name]
            #             ]
            #         )
            #         for variable in model.variables if is_array(variable) and deal_with_variable(variable) and is_local(variable)
            #     ]
            # )
            # end of array variable indexing for non-define variables
            # ---------------------------------------------------------------------------------------
            # + os.linesep + '-- START OF TYPE CHECKING FUNCTIONS' + os.linesep + os.linesep
            # + ''.join(map(create_check_value, filter(lambda var : var.model_as == 'VAR' and (blackboard_mode != is_env(var)), model.variables)))
            # created checkValue for each variable that can be updated.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF NEW ARRAY FUNCTIONS' + os.linesep + os.linesep
            + ''.join(
                [
                    array_set_creator(variable)
                    for variable in model.variables
                    if is_array(variable) and deal_with_variable(variable)
                ]
            )
            # end of array update functions for variables.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF UPDATES' + os.linesep + os.linesep
            + board_env + 'Update :: ' + data_type_name + ' -> StdGen -> ' + data_type_name + os.linesep
            + board_env + 'Update ' + var_name + ' newGen = ' + var_name + ' { ' + board_env + 'Generator = newGen }' + os.linesep
            + ''.join(
                [
                    board_env + 'Update' + pascal_case(variable.name) + ' :: ' + data_type_name + ' -> StdGen -> ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name])  + ')') if is_array(variable) else variable_type_map[variable.name]) + ' -> ' + data_type_name + os.linesep
                    + board_env + 'Update' + pascal_case(variable.name) + ' ' + var_name + ' newGen newVal = ' + var_name + ' { ' + board_env + 'Generator = newGen, ' + board_env + pascal_case(variable.name) + ' = newVal' + ' }' + os.linesep
                    for variable in model.variables if variable.model_as == 'VAR' and (not is_local(variable)) and deal_with_variable(variable)
                ]
            )
            + (
                ''.join(
                    [
                        board_env + 'Update' + pascal_case(variable.name) + ' :: Integer ->' + data_type_name + ' -> StdGen -> ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name])  + ')') if is_array(variable) else variable_type_map[variable.name]) + ' -> ' + data_type_name + os.linesep
                        + ''.join(
                            [
                                (board_env + 'Update' + pascal_case(variable.name) + ' ' + str(node_location) + ' ' + var_name + ' newGen newVal = ' + var_name + ' { ' + board_env + 'Generator = newGen, ' + board_env + pascal_case(variable.name) + 'Location' + str(node_location) + ' = newVal' + ' }' + os.linesep)
                                for node_location in local_var_to_nodes[variable.name]
                            ]
                        )
                        + board_env + 'Update' + pascal_case(variable.name) + ' _ _ _ _ = error "illegal local reference: boardUpdate' + pascal_case(variable.name) + '"' + os.linesep
                        for variable in model.variables if variable.model_as == 'VAR' and variable.name in local_var_to_nodes
                    ]
                )
                if blackboard_mode else
                ''
            )
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
                        format_code(model.tick_condition, None)[0]
                    ) + os.linesep
                    + os.linesep + '-- START OF FUTURE CHANGES' + os.linesep + os.linesep
                    + 'applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                    + 'applyFutureChanges [] = id' + os.linesep
                    + 'applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)' + os.linesep
                    + os.linesep + '-- START OF BETWEEN TICK CHANGES' + os.linesep + os.linesep
                    + between_tick_update(model.update)
                )
            )
            # end of tick conditions.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF INITIAL ' + ('BLACKBOARD' if blackboard_mode else 'ENVIRONMENT') + ' VALUE' + os.linesep + os.linesep
            + 'initial' + ('Blackboard' if blackboard_mode else 'Environment') + ' :: Integer -> ' + data_type_name_2 + os.linesep
            + 'initial' + ('Blackboard' if blackboard_mode else 'Environment') + ' seed ' + ('' if blackboard_mode else ('blackboard' + ' ')) + '= ' + ('newBlackboard' if blackboard_mode else 'newEnvironment') + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + '-- START OF UDPATE FROZENVAR (for internal use only)' + os.linesep
            + ''.join(
                [
                    indent(2) + board_env + 'Update' + pascal_case(variable.name) + ' :: ' + data_type_name + ' -> StdGen -> ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name])  + ')') if is_array(variable) else variable_type_map[variable.name]) + ' -> ' + data_type_name + os.linesep
                    + indent(2) + board_env + 'Update' + pascal_case(variable.name) + ' ' + var_name + ' newGen newVal = ' + var_name + ' { ' + board_env + 'Generator = newGen, ' + board_env + pascal_case(variable.name) + ' = newVal' + ' }' + os.linesep
                    for variable in model.variables if variable.model_as == 'FROZENVAR' and (not is_local(variable)) and deal_with_variable(variable)
                ]
            )
            + (
                ''.join(
                    [
                        indent(2) + board_env + 'Update' + pascal_case(variable.name) + ' :: Integer ->' + data_type_name + ' -> StdGen -> ' + (('(' + ', '.join([variable_type_map[variable.name]] * variable_array_size_map[variable.name])  + ')') if is_array(variable) else variable_type_map[variable.name]) + ' -> ' + data_type_name + os.linesep
                        + ''.join(
                            [
                                (indent(2) + board_env + 'Update' + pascal_case(variable.name) + ' ' + str(node_location) + ' ' + var_name + ' newGen newVal = ' + var_name + ' { ' + board_env + 'Generator = newGen, ' + board_env + pascal_case(variable.name) + 'Location' + str(node_location) + ' = newVal' + ' }' + os.linesep)
                                for node_location in local_var_to_nodes[variable.name]
                            ]
                        )
                        + indent(2) + board_env + 'Update' + pascal_case(variable.name) + ' _ _ _ _ = error "illegal local reference: boardUpdate' + pascal_case(variable.name) + '"' + os.linesep
                        for variable in model.variables if variable.model_as == 'FROZENVAR' and variable.name in local_var_to_nodes
                    ]
                )
                if blackboard_mode else
                ''
            )
            + indent(2) + '-- START OF CREATING' + os.linesep
            + indent(2) + 'firstGen = getGenerator seed' + os.linesep
            + indent(2) + 'dummy = ' + data_type_name + ' firstGen ' + ' '.join(
                [
                    get_default_value(variable)
                    for variable in model.variables if variable.model_as != 'DEFINE' and deal_with_variable(variable)
                    for node_location in (local_var_to_nodes[variable.name] if is_local(variable) else [None])
                ]
            ) + os.linesep
            + create_initial_statements(blackboard_mode, local_initial_statements)
            + os.linesep
            # created initial blackboard. ---------------------------------------------------------------------------------------
        )

    def create_environment():
        return handle_blackboard_environment(False, [])

    def create_blackboard():
        def walk_tree_recursive_blackboard(current_node, node_names, running_int, location_info, local_initial_statements):
            while hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
            current_name = current_node.leaf.name if current_node.name is None else current_node.name
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            node_name = current_name + '__node'
            cur_node_names = {node_name}.union(node_names)
            running_int = running_int + 1
            my_int = running_int
            if current_node.node_type == 'action':
                for variable in current_node.local_variables:
                    location_info.append((variable, my_int))
                    cur_statement = variable
                    for initial_statement in current_node.init_statements:
                        if initial_statement.variable.name == variable.name:
                            cur_statement = initial_statement
                            break
                    local_initial_statements.append((my_int, variable.model_as == 'DEFINE', cur_statement))
            elif current_node.node_type in {'check', 'environment_check'}:
                pass  # can't have local variables in checks.
            else:
                node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
                for child in node_children:
                    (cur_node_names, running_int, location_info, local_initial_statements) = walk_tree_recursive_blackboard(child, cur_node_names, running_int, location_info, local_initial_statements)
            return (
                cur_node_names,
                running_int,
                location_info,
                local_initial_statements
            )

        (_, _, location_info, local_initial_statements) = walk_tree_recursive_blackboard(model.root, set(), -1, [], [])
        for (variable, my_int) in location_info:
            name = variable.name
            if name in local_var_to_nodes:
                local_var_to_nodes[name].append(my_int)
            else:
                local_var_to_nodes[name] = [my_int]
        return handle_blackboard_environment(True, local_initial_statements)

    function_format = {
        'loop' : ('', format_function_loop),
        'case_loop' : ('', format_function_case_loop),
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
        'implies' : ('sereneIMPLIES', format_function_before),
        'equivalent' : ('==', format_function_between),
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
        'count' : ('', format_function_count),
        'index' : ('', format_function_index)
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

    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit)
    variable_type_map = {
        variable.name : to_haskell_type(variable_type(variable, declared_enumerations, constants))
        for variable in model.variables
    }
    variable_array_size_map = {
        variable.name : variable_array_size(variable, declared_enumerations, {}, variables, constants, {})
        for variable in model.variables if is_array(variable)
    }
    node_names_to_node_locations = {}
    counters = {'statement' : 0, 'random' : 0}
    # arguments = set()
    local_var_to_nodes = {}
    loop_references = {}
    location = location + ('' if location[-1] == '/' else '/')
    my_location = location + 'app/'
    if not os.path.isdir(my_location):
        if os.path.exists(my_location):
            raise FileExistsError('Specified Output Location cannot be used as app is a file in this location')
        os.makedirs(my_location)
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/haskell_file/BehaviorTreeCore.hs', my_location + 'BehaviorTreeCore.hs')
    with open(my_location + 'SereneRandomizer.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(randomizer)
    with open(my_location + 'SereneOperations.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(serene_operations)
    with open(my_location + 'BehaviorTreeEnvironment.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_environment())
    with open(my_location + 'BehaviorTreeBlackboard.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_blackboard())
    with open(my_location + pascal_case(output_name) + '.hs', 'w', encoding='utf-8') as write_file:
        (seen_nodes, to_write) = create_tree(model, output_name)
        write_file.write(to_write)
    with open(my_location + 'Main.hs', 'w', encoding='utf-8') as write_file:
        write_file.write(create_runner(model, output_name, max_iter))

    for action in model.action_nodes:
        if action.name in seen_nodes:
            # arguments = {argument_pair.argument_name for argument_pair in action.arguments}
            with open(my_location + 'BTree' + pascal_case(action.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_action_node(action))
            # arguments = set()
    for check in model.check_nodes:
        if check.name in seen_nodes:
            # arguments = {argument_pair.argument_name for argument_pair in check.arguments}
            with open(my_location + 'BTree' + pascal_case(check.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_check_node(check))
            # arguments = set()
    for environment_check in model.environment_checks:
        if environment_check.name in seen_nodes:
            # arguments = {argument_pair.argument_name for argument_pair in environment_check.arguments}
            with open(my_location + 'BTree' + pascal_case(environment_check.name) + '.hs', 'w', encoding='utf-8') as write_file:
                write_file.write(build_environment_check_node(environment_check))
            # arguments = set()
    with open(location + output_name + '.cabal', 'w', encoding = 'utf-8') as write_file:
        write_file.write(
            'name: ' + output_name + os.linesep
            + 'version: 0.1.0.0' + os.linesep
            + 'author: Auto Generated by BehaVerify' + os.linesep
            + 'maintainer: No Maintainer.' + os.linesep
            + 'build-type: Simple' + os.linesep
            + 'executable testing' + os.linesep
            + indent(1) + 'main-is: Main.hs' + os.linesep
            + indent(1) + 'ghc-options: -w' + os.linesep
            + indent(1) + 'other-modules:' + os.linesep
            + (', ' + os.linesep).join([(indent(2) + os.path.splitext(os.path.basename(file_name))[0]) for file_name in os.listdir(my_location) if os.path.splitext(os.path.basename(file_name))[1] == '.hs']) + os.linesep
            + indent(1) + 'build-depends: base, random' + os.linesep
            + indent(1) + 'hs-source-dirs: app' + os.linesep
            + indent(1) + 'default-language: Haskell2010' + os.linesep
        )
    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('output_name')
    arg_parser.add_argument('--max_iter', default = 100)
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    # arg_parser.add_argument('--keep_names', action = 'store_true')
    args = arg_parser.parse_args()
    dsl_to_haskell(args.metamodel_file, args.model_file, args.location, args.output_name, args.max_iter, args.recursion_limit)
