'''
This module is for internal use with BehaVerify.
It is used to create Haskell code from BehaVerify DSL for Behavior Trees.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2023-09-12
'''
import argparse
import os
import shutil
import itertools
import textx
from behaverify_common import haskell_indent as indent, create_node_name

from check_model import (validate_model,
                         is_local,
                         is_env,
                         is_blackboard,
                         is_array,
                         build_range_func)


def dsl_to_haskell():
    '''
    this function is used to convert the dsl to haskell code
    '''
    def to_haskell_type(constant_type):
        '''Used to get the type of the constant'''
        if constant_type == 'ENUM':
            return 'String'
        if constant_type == 'BOOLEAN':
            return 'Bool'
        if constant_type == 'INT':
            return 'Integer'
        raise ValueError('Constant ' + constant_type + ' is of an unsupported type. Only ENUM, BOOLEAN, and INT are supported')
    def variable_type(variable):
        '''returns the vaiable type, correctly formatted for haskell'''
        return (
            (
                'Integer'
                if variable.domain == 'INT'
                else
                (
                    'String'
                    if variable.domain == 'ENUM'
                    else
                    'Bool'
                )
            )
            if variable.model_as == 'DEFINE'
            else
            (
                'Bool'
                if variable.domain.boolean is not None
                else
                (
                    (
                        'Integer'
                        if variable.domain.true_int is not None
                        else
                        (
                            'String'
                            if isinstance(handle_constant(variable.domain.enums[0], False), str)
                            else
                            'Integer'
                        )
                    )
                    if variable.domain.min_val is None
                    else
                    'Integer'
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

    def __format_function_before__(function_name, values, index_start, init_mode, blackboard_name, environment_name):
        if len(values) - index_start <= 2:
            return (
                '('
                + function_name + ' '
                + ' '.join([format_code(value, init_mode, blackboard_name, environment_name) for value in values[index_start:]])
                + ')'
            )
        cur_val = values[index_start]
        return (
            '('
            + function_name + ' ' + format_code(cur_val, init_mode, blackboard_name, environment_name) + ' ' + __format_function_before__(function_name, values, index_start + 1, init_mode, blackboard_name, environment_name)
            + ')'
        )

    def format_function_before(function_name, code, init_mode, blackboard_name, environment_name):
        '''used with functions where the call is before the arguments'''
        if len(code.function_call.values) <= 2:
            return (
                '('
                + function_name + ' '
                + ' '.join([format_code(value, init_mode, blackboard_name, environment_name) for value in code.function_call.values])
                + ')'
            )
        return __format_function_before__(function_name, code.function_call.values, 0, init_mode, blackboard_name, environment_name)

    def __format_function_between__(function_name, values, index_start, init_mode, blackboard_name, environment_name):
        if len(values) - index_start <= 2:
            return (
                '('
                + (' ' + function_name + ' ').join([format_code(value, init_mode, blackboard_name, environment_name) for value in values[index_start:]])
                + ')'
            )
        cur_val = values[index_start]
        return (
            '('
            + format_code(cur_val, init_mode, blackboard_name, environment_name) + ' ' + function_name + ' ' + __format_function_between__(function_name, values, index_start + 1, init_mode, blackboard_name, environment_name)
            + ')'
        )

    def format_function_between(function_name, code, init_mode, blackboard_name, environment_name):
        '''used with functions where the call is between functions'''
        if len(code.function_call.values) <= 2:
            return (
                '('
                + (' ' + function_name + ' ').join([format_code(value, init_mode, blackboard_name, environment_name) for value in code.function_call.values])
                + ')'
            )
        return __format_function_between__(function_name, code.function_call.values, 0, init_mode, blackboard_name, environment_name)

    def __format_function_count__(_, values, index_start, init_mode, blackboard_name, environment_name):
        if len(values) - index_start <= 0:
            return '0'
        if len(values) - index_start == 1:
            return '(sereneCOUNT False ' + format_code(values[index_start], init_mode, blackboard_name, environment_name) + ')'
        if len(values) - index_start == 2:
            return '(sereneCOUNT ' + format_code(values[index_start], init_mode, blackboard_name, environment_name) + ' ' + format_code(values[index_start + 1], init_mode, blackboard_name, environment_name) + ')'
        val1 = values[index_start]
        val2 = values[index_start + 1]
        return '((sereneCOUNT ' + format_code(val1, init_mode, blackboard_name, environment_name) + ' ' + format_code(val2, init_mode, blackboard_name, environment_name) + ') + ' + __format_function_count__(_, values, index_start + 2, init_mode, blackboard_name, environment_name) + ')'

    def format_function_count(_, code, init_mode, blackboard_name, environment_name):
        '''used with count function specifically'''
        return __format_function_count__(_, code.function_call.values, 0, init_mode, blackboard_name, environment_name)

    def format_function_index(_, code, init_mode, blackboard_name, environment_name):
        '''not used'''
        variable = code.function_call.variable
        return (
            '('
            + ('env' if is_env(variable) else ('localBoard' if is_local(variable) else 'board')) + pascal_case(variable.name)
            + (' nodeLocation' if is_local(variable) else '')
            + ' ' + format_code(code.function_call.values[0], init_mode, blackboard_name, environment_name)
            + ' ' + ((((blackboard_name + ' ') if variable.model_as == 'DEFINE' else '') + environment_name) if is_env(variable) else blackboard_name)
            + ')'
        )

    funcion_format = {
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

    def format_variable(variable, init_mode, blackboard_name, environment_name):
        '''used to format variable names'''
        if variable.model_as == 'DEFINE':
            init_mode = None  # we do this to allow defines to work in a partially finished blackboard/environtmen
        return (
            ('(localBoard' + pascal_case(variable.name) + ' nodeLocation ' + blackboard_name + ')')
            if is_local(variable)
            else
            (
                (
                    ('newVal' + pascal_case(variable.name))
                    if init_mode == 'env'
                    else
                    (
                        ('(env' + pascal_case(variable.name) + ' ' + blackboard_name + ' ' + environment_name + ')')
                        if variable.model_as == 'DEFINE'
                        else
                        ('(env' + pascal_case(variable.name) + ' ' + environment_name + ')')
                    )
                )
                if is_env(variable)
                else
                (
                    ('newVal' + pascal_case(variable.name))
                    # if 'board' in init_mode
                    if init_mode == 'board'
                    else
                    ('(board' + pascal_case(variable.name) + ' ' + blackboard_name + ')')
                )
            )
        )

    def format_code(code, init_mode, blackboard_name, environment_name):
        '''used to format code'''
        return (
            (
                handle_constant(code.constant, True) if code.constant is not None else (
                    format_variable(code.variable, init_mode, blackboard_name, environment_name) if code.variable is not None else (
                        ('(' + format_code(code.code_statement, init_mode, blackboard_name, environment_name) + ')') if code.code_statement is not None else (
                            funcion_format[code.function_call.function_name][1](funcion_format[code.function_call.function_name][0], code, init_mode, blackboard_name, environment_name)
                        )
                    )
                )
            )
        )

    def handle_constant(constant, str_conversion):
        '''used to handle constnts and replace them with integer values'''
        if constant in arguments:
            return constant
        new_constant = ((constants['serene_index'][-1] if constant == 'serene_index' else constants[constant]) if constant in constants else constant)
        return (
            (
                ('"' + new_constant + '"')
                if isinstance(new_constant, str)
                else
                (
                    str(new_constant)
                    if isinstance(new_constant, bool)
                    else
                    (
                        ('(' + str(new_constant) + ')')
                        if new_constant < 0
                        else
                        str(new_constant)
                    )
                )
            )
            if str_conversion
            else
            new_constant
        )

    def handle_variable_statement(statement, indent_level, init_mode, board_env_name, blackboard_name, environment_name):
        '''handles variable statements. the function declaration was created elsewhere. this creates the logic of the variable udpate.'''
        assign_var = statement.variable
        if is_array(assign_var):
            # todo: fix this area to deal with constant index. right now only works with variable index.
            number_of_updates = 0
            update_pair_strings = []
            update_value_strings = []
            random_gen_strings = []
            needs_random = False
            if statement.array_mode == 'range':
                needs_random = any(case_result.range_mode == 'range' or len(case_result.values) > 1 for case_result in statement.assign.assign.case_results) or statement.assign.assign.default_result.range_mode == 'range' or len(statement.assign.assign.default_result.values) > 1
                if len(statement.values) == 0:
                    number_of_updates = handle_constant(assign_var.array_size, False)
                    update_range = range(number_of_updates)
                else:
                    cond_func = build_range_func(statement.values[2], constants)
                    update_range = list(filter(cond_func, range(handle_constant(statement.values[0], False), handle_constant(statement.values[1], False) + 1)))
                    number_of_updates = len(update_range)
                for index, range_val in enumerate(update_range):
                    constants['serene_index'].append(range_val)
                    update_value_strings.append(indent(indent_level + 2) + 'updateValue' + str(index) + handle_assign(statement.assign.assign, assign_var, indent_level + 2, init_mode, board_env_name, blackboard_name, environment_name, True, 'randomGenerator' + str(len(random_gen_strings)) if needs_random else None))
                    update_pair_strings.append(
                        indent(indent_level + 2) + 'updatePair' + str(index) + ' = '
                        + '(' + (handle_constant(statement.assign.index_expr, True) if statement.constant_index == 'constant_index' else format_code(statement.assign.index_expr, init_mode, blackboard_name, environment_name)) + ', updateValue' + str(index) + ')'
                        + os.linesep
                    )
                    constants['serene_index'].pop()
                    if needs_random:
                        random_gen_strings.append(
                            indent(indent_level + 2) + 'randomGenerator' + str(len(random_gen_strings)) + ' = '
                            + (
                                (('sereneEnvGenerator ' + environment_name) if is_env(assign_var) else ('sereneBoardGenerator ' + blackboard_name))
                                if len(random_gen_strings) == 0
                                else
                                ('snd (getRandomInteger randomGenerator' + str(len(random_gen_strings) - 1) + ' 1)')
                            )
                            + os.linesep
                        )
            else:
                number_of_updates = len(statement.assigns)
                for index, array_index in enumerate(statement.assigns):
                    currently_random = any(case_result.range_mode == 'range' or len(case_result.values) > 1 for case_result in array_index.assign.case_results) or array_index.assign.default_result.range_mode == 'range' or len(array_index.assign.default_result.values) > 1
                    needs_random = needs_random or currently_random
                    update_value_strings.append(indent(indent_level + 2) + 'updateValue' + str(index) + handle_assign(array_index.assign, assign_var, indent_level + 2, init_mode, board_env_name, blackboard_name, environment_name, True, 'randomGenerator' + str(len(random_gen_strings)) if currently_random else None))
                    update_pair_strings.append(
                        indent(indent_level + 2) + 'updatePair' + str(index)
                        + ' = '
                        + '(' + (handle_constant(array_index.index_expr, True) if statement.constant_index == 'constant_index' else format_code(array_index.index_expr, init_mode, blackboard_name, environment_name)) + ', updateValue' + str(index)  + ')'
                        + os.linesep
                    )
                    if currently_random:
                        random_gen_strings.append(
                            indent(indent_level + 2) + 'randomGenerator' + str(len(random_gen_strings)) + ' = '
                            + (
                                (('sereneEnvGenerator ' + environment_name) if is_env(assign_var) else ('sereneBoardGenerator ' + blackboard_name))
                                if len(random_gen_strings) == 0
                                else
                                ('snd (getRandomInteger randomGenerator' + str(len(random_gen_strings) - 1) + ' 1)')
                            )
                            + os.linesep
                        )
            return (
                ' = '
                + (
                    ('arrayUpdateEnv' + pascal_case(assign_var.name) + ' ' + (('(updateEnvGenerator ' + environment_name + ' randomGenerator' + str(len(random_gen_strings) - 1)  + ')') if needs_random else environment_name) + ' updates')
                    if board_env_name is None
                    else
                    (
                        ('(' + blackboard_name + ', arrayUpdateEnv' + pascal_case(assign_var.name) + ' ' + (('(updateEnvGenerator ' + environment_name + ' randomGenerator' + str(len(random_gen_strings) - 1)  + ')') if needs_random else environment_name) + ' updates)')
                        if is_env(assign_var)
                        else
                        (('(arrayUpdateLocalBoard' if is_local(assign_var) else '(arrayUpdateBoard') + pascal_case(assign_var.name) + (' nodeLocation' if is_local(assign_var) else '') + ' ' + (('(updateBoardGenerator ' + blackboard_name + ' randomGenerator' + str(len(random_gen_strings) - 1)  + ')') if needs_random else blackboard_name) + ' updates, ' + environment_name + ')')
                    )
                )
                + os.linesep
                + indent(indent_level + 1) + 'where' + os.linesep
                + ('' if board_env_name is None else (indent(indent_level + 2) + '(' + blackboard_name + ', ' +  environment_name + ') = ' + board_env_name + os.linesep))
                + ''.join(random_gen_strings)
                + indent(indent_level + 2) + 'updates = [' + ', '.join(map(lambda x: 'updatePair' + str(x), range(number_of_updates))) + ']' + os.linesep
                + ''.join(update_pair_strings)
                + ''.join(update_value_strings)
                # + board_env_post_script(indent_level + 2, board_env_name, blackboard_name, environment_name) # handled elsewhere
            )
        return handle_assign(statement.assign, assign_var, indent_level, init_mode, board_env_name, blackboard_name, environment_name, False, None)

    def handle_read_statement(statement, indent_level, init_mode):
        '''used to handle read statements'''
        cond_var = statement.condition_variable
        inject_string = ''
        shift = (0 if cond_var is None else 1)
        inject_string = (
            (
                (indent(indent_level + 2) + 'privateTempBoardEnv0 = boardEnv' + os.linesep)
                if not statement.non_determinism
                else
                (
                    indent(indent_level + 2) + '(conditionRandomInteger, conditionRandomGenerator) = getRandomInteger (sereneEnvGenerator (snd boardEnv)) 1' + os.linesep
                    + indent(indent_level + 2) + 'privateTempBoardEnv0 = (fst boardEnv, updateEnvGenerator (snd boardEnv) conditionRandomGenerator)' + os.linesep
                )
            )
            +
            (
                ''
                if cond_var is None
                else
                (
                    indent(indent_level + 2) + 'privateTempBoardEnv1 = ('
                    + ('updateLocalBoard' if is_local(cond_var) else '') + pascal_case(cond_var.name)
                    + (' nodeLocation' if is_local(cond_var) else '')
                    + ' (fst privateTempBoardEnv0) True, snd privateTempBoardEnv0)' + os.linesep
                )
            )
        )
        return (
            [
                (
                    os.linesep
                    + indent(indent_level + 1) + '| not (' + format_code(statement.condition, init_mode, 'conditionBlackboard', 'conditionEnvironment') + ') = boardEnv' + os.linesep
                    + (
                        (indent(indent_level + 1) + '| conditionRandomInteger == 0 = privateTempBoardEnv0' + os.linesep)
                        if statement.non_determinism
                        else
                        ''
                    )
                    + indent(indent_level + 1) + '| otherwise = privateBoardEnv' + os.linesep  # this needs to be changed to handle non-determinism
                    + indent(indent_level + 1) + 'where' + os.linesep
                    + indent(indent_level + 2) + '(conditionBlackboard, conditionEnvironment) = boardEnv' + os.linesep
                    + inject_string
                    + indent(indent_level + 2) + 'privateBoardEnv = privateTempBoardEnv' + str(len(statement.variable_statements) + shift) + os.linesep
                    + ''.join(
                        [
                            (
                                indent(indent_level + 2) + 'privateTempBoardEnv' + str(x + shift + 1)  # no os.linesep here intentionally, handled by varirable statement
                                + handle_variable_statement(variable_statement, indent_level + 2, init_mode, 'privateTempBoardEnv' + str(x + shift), 'blackboard', 'environment')
                            )
                            for x, variable_statement in enumerate(statement.variable_statements)
                        ]
                    )
                )
            ],
            []
        )

    def handle_write_statement(statement, indent_level, init_mode):
        '''handles write statements'''
        return (
            [
                (
                    handle_variable_statement(update, indent_level, init_mode, 'boardEnv', 'blackboard', 'environment')
                )
                for update in statement.update if update.instant
            ],
            [
                (
                    handle_variable_statement(update, indent_level, init_mode, 'boardEnv', 'blackboard', 'environment')
                )
                for update in statement.update if not update.instant
            ]
        )

    def format_returns(status_result):
        '''fixes capitalization'''
        return status_result.status.capitalize()

    def handle_return_statement(statement, indent_level = 2):
        '''handles return statements'''
        blackboard_name = 'blackboard'
        environment_name = 'environment'
        return (
            indent(indent_level) + 'returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus' + os.linesep
            + indent(indent_level) + 'returnStatement boardEnv'
            + (
                (' = ' + format_returns(statement.default_result) + os.linesep)
                if len(statement.case_results) == 0
                else
                (
                    os.linesep
                    + ''.join(
                        [
                            (
                                indent(indent_level + 1) + '| ' + format_code(case_result.condition, None, blackboard_name, environment_name) + ' = ' + format_returns(case_result) + os.linesep
                            )
                            for case_result in statement.case_results
                        ]
                    )
                    + indent(indent_level + 1) + '| otherwise = ' + format_returns(statement.default_result) + os.linesep
                )
            )
            + indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + '(blackboard, environment) = boardEnv' + os.linesep
        )

    def handle_statement(statement, indent_level, init_mode):
        '''switches between the three statement types'''
        return (
            ([handle_variable_statement(statement.variable_statement, indent_level, init_mode, 'boardEnv', 'blackboard', 'environment')], []) if statement.variable_statement is not None else (
                handle_read_statement(statement.read_statement, indent_level, init_mode) if statement.read_statement is not None else (
                    handle_write_statement(statement.write_statement, indent_level, init_mode)
                    )
                )
            )

    def module_declaration(node_name):
        '''just a string'''
        return 'module BTree' + pascal_case(node_name) + ' where' + os.linesep

    def check_function(node):
        '''used to build check functions'''
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
            + indent(1 + indent_modifier) + '| ' + format_code(node.condition, None, 'blackboard', 'environment') + ' = (Success, [], [], blackboard, environment, futureChanges)' + os.linesep
            + indent(1 + indent_modifier) + '| otherwise = (Failure, [], [], blackboard, environment, futureChanges)'
        )

    def action_function(node):
        '''used to build action functions'''
        indent_modifier = 2 if len(node.arguments) > 0 else 0
        pre = len(node.pre_update_statements)
        post = len(node.post_update_statements)
        pre_updates = []
        delay_updates = []
        post_updates = []
        for index in range(pre):
            (new_pre, new_delay) = handle_statement(node.pre_update_statements[index], 2 + indent_modifier, None)
            pre_updates += new_pre
            delay_updates += new_delay
        for index in range(post):
            (new_post, new_delay) = handle_statement(node.post_update_statements[index], 2 + indent_modifier, None)
            post_updates += new_post
            delay_updates += new_delay
        pre = len(pre_updates)
        post = len(post_updates)
        delay = len(delay_updates)

        def env_decl(index, indent_level):
            return (
                indent(indent_level) + 'boardEnvUpdate' + str(index) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                + indent(indent_level) + 'boardEnvUpdate' + str(index) + ' boardEnv'  # no os.linesep here. we handle that in the variable statement.
            )

        def code_decl(index, indent_level):
            return (
                indent(indent_level) + 'futureChanges' + str(index) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
                + indent(indent_level) + 'futureChanges' + str(index) + ' boardEnv'  # no os.linesep here. we handle that in the variable statement.
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
                if len(node.arguments) > 0
                else
                ''
            )
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
            + indent(indent_modifier) + 'bTreeFunction' + pascal_case(node.name) + ' _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)' + os.linesep
            + indent(1 + indent_modifier) + 'where' + os.linesep
            + ('').join(
                [
                    (env_decl(index, 2 + indent_modifier) + value)
                    for index, value in enumerate(pre_updates)
                ]
            )
            + handle_return_statement(node.return_statement, 2 + indent_modifier)
            + ('').join(
                [
                    (env_decl(index + pre, 2 + indent_modifier) + value)
                    for index, value in enumerate(post_updates)
                ]
            )
            + ('').join(
                [
                    (code_decl(index, 2 + indent_modifier) + value)
                    for index, value in enumerate(delay_updates)
                ]
            )
            + indent(2 + indent_modifier) + 'preStatusBoardEnv = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre))))) + (' $ ' if pre > 1 else ' ') + '(oldBlackboard, oldEnvironment)' + os.linesep
            + indent(2 + indent_modifier) + 'returnStatus = returnStatement preStatusBoardEnv' + os.linesep
            + indent(2 + indent_modifier) + '(newBlackboard, newEnvironment) = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre, pre + post))))) + (' $ ' if post > 1 else ' ') + 'preStatusBoardEnv' + os.linesep
            + indent(2 + indent_modifier) + 'newFutureChanges = ' + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, reversed(range(delay))))) + (' : ' if delay > 0 else '') + 'futureChanges' + os.linesep
        )

    def build_check_node(node):
        '''sequence to build check nodes'''
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + check_function(node)
                )

    def build_environment_check_node(node):
        '''just calls check node lol'''
        return build_check_node(node)

    def build_action_node(node):
        '''action node sequence'''
        return (module_declaration(node.name)
                + standard_imports
                + os.linesep
                + os.linesep
                + action_function(node)
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
            # + ''.join([('import BTree' + pascal_case(node.name) + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
            # the above line is unnecessary. Not sure why it was here.
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
                        if node.memory == 'with_partial_memory'
                        else
                        (
                            'TrueMemory'
                            if node.memory == 'with_true_memory'
                            else
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
                        if node.memory == 'with_partial_memory'
                        else
                        (
                            'TrueMemory'
                            if node.memory == 'with_true_memory'
                            else
                            ''
                        )
                    )
                    + 'Creator '
                    + (
                        'successOnAllFailureOne'
                        if node.parallel_policy == 'success_on_all'
                        else
                        (
                            'successOnOneFailureOne'
                            if node.parallel_policy == 'success_on_one'
                            else
                            'NOT DONE'
                        )
                    )
                    + ')'
                )
            return (
                '(decoratorCreator '
                + (
                    'inverterCreator'
                    if node.node_type == 'inverter'
                    else
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
                    + ((' ' + ' '.join(map(lambda arg: handle_constant(arg, True), current_args)) + ')') if has_args else '')
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
                    # this is wrong, and will need to change the current_node.name with the node type, but i'm lazy right now.
                )
            return (
                (
                    (
                        node_name,
                        seen_nodes,
                        cur_node_names,
                        cur_node_names_map,
                        running_string,
                        running_int,
                        indent_level
                    )
                )
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

    def board_env_post_script(indent_level, board_env_name, blackboard_name, environment_name):
        return (
            indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + '(' + blackboard_name + ', ' + environment_name + ') = ' + board_env_name + os.linesep
        )

    def create_random_func(case_result, function_name, var_type, cond_func, random_range, indent_level, init_mode, blackboard_name, environment_name):
        # figure out where case_result is coming from.
        # i think it's defined below.
        if case_result.range_mode:
            return (
                indent(indent_level) + function_name + ' :: Integer -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                        for index, value in enumerate(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))
                    ]
                )
            )
        if len(case_result.values) > 1:
            return (
                indent(indent_level) + function_name + ' :: Integer -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, blackboard_name, environment_name) + os.linesep)
                        for index, value in enumerate(case_result.values)
                    ]
                )
            )
        return ''

    def handle_case_result(case_result, case_mode, init_mode, indent_level, assign_var, env_board, env_board_random, env_board_generator, update_generator, update_env_board, board_env_name, blackboard_name, environment_name, unique_id, value_only_mode, random_gen_string):
        '''
        case_mode = 'case' -> this is a case result
        case_mode = 'default' -> this is a default result
        case_mode = 'only' -> this is a default result with no case results.
        '''
        if case_mode == 'only':
            if (case_result.range_mode != 'range') and len(case_result.values) == 1:
                # use a special case if we're just setting to a constant value. no need for special bells and whistles.
                return (
                    (
                        ' = '
                        + (
                            format_code(case_result.values[0], init_mode, blackboard_name, environment_name)
                            if value_only_mode
                            else
                            (
                                ('' if board_env_name is None else ('(' + blackboard_name + ', ' if is_env(assign_var) else '('))
                                + update_env_board + pascal_case(assign_var.name) + ' ' + env_board + ' ' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name)
                                + ('' if board_env_name is None else (')' if is_env(assign_var) else ', ' + environment_name + ')'))
                            )
                        )
                    ),
                    ''
                )
        return_string = (
            (os.linesep + indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, blackboard_name, environment_name) + ' = ')
            if case_mode == 'case'
            else
            (
                ' = '
                if case_mode == 'only'
                else
                (os.linesep + indent(indent_level + 1) + '| otherwise = ')
            )
        )
        if (case_result.range_mode != 'range') and (len(case_result.values) == 1):
            cond_func = None
            random_range = 0
            function_name = ''
        elif case_result.range_mode == 'range':
            cond_func = build_range_func(case_result.values[2], constants)
            random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
            function_name = 'privateRandom' + str(unique_id)
            # unique_id = unique_id + 1
        else:
            cond_func = None
            random_range = len(case_result.values) - 1
            function_name = 'privateRandom' + str(unique_id)
            # unique_id = unique_id + 1

        return_string += (
            (
                (function_name + ' (fst (getRandomInteger ' + random_gen_string + ' ' + str(random_range) + '))')
                if case_result.range_mode == 'range' or len(case_result.values) > 1
                else
                format_code(case_result.values[0], init_mode, blackboard_name, environment_name)
            )
            if value_only_mode
            else
            (
                ('' if board_env_name is None else ('(' + blackboard_name + ', ' if is_env(assign_var) else '('))
                + (
                    (
                        update_env_board + pascal_case(assign_var.name) + ' ' + env_board + ' ' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name)
                    )
                    if (not case_result.range_mode) and (len(case_result.values) == 1)
                    else
                    (
                        update_generator + ' ('
                        + update_env_board + pascal_case(assign_var.name) + ' ' + env_board + ' '
                        + '(' + function_name + ' (fst (getRandomInteger (' + env_board_generator + ' ' + env_board_random + ') ' + str(random_range)
                        + ')))) (snd (getRandomInteger (' + env_board_generator + ' ' + env_board_random + ') ' + str(random_range) + '))'
                    )
                )
                + ('' if board_env_name is None else (')' if is_env(assign_var) else ', ' + environment_name + ')'))
            )
        )
        where_string = create_random_func(case_result, function_name, variable_type(assign_var), cond_func, random_range, indent_level + 2, init_mode, blackboard_name, environment_name)
        return (return_string, where_string)

    def handle_assign(assign, assign_var, indent_level, init_mode, board_env_name, blackboard_name, environment_name, value_only_mode, random_gen_string):
        '''handles variable statements. the function declaration was created elsewhere. this creates the logic of the variable udpate.'''
        update_env_board = (
            'updateEnv'
            if is_env(assign_var)
            else
            (
                'updateLocalBoard'
                if is_local(assign_var)
                else
                'updateBoard'
            )
        )
        update_generator = (
            'updateEnvGenerator'
            if is_env(assign_var)
            else
            'updateBoardGenerator'
        )
        env_board = (
            environment_name
            if is_env(assign_var)
            else
            (
                ('nodeLocation ' + blackboard_name)
                if is_local(assign_var)
                else
                blackboard_name
            )
        )
        env_board_random = (environment_name if is_env(assign_var) else blackboard_name)
        env_board_generator = (
            'sereneEnvGenerator'
            if is_env(assign_var)
            else
            (
                'sereneBoardGenerator'
            )
        )
        strings = [
            handle_case_result(case_result, 'case', init_mode, indent_level, assign_var, env_board, env_board_random, env_board_generator, update_generator, update_env_board, board_env_name, blackboard_name, environment_name, index + 1, value_only_mode, random_gen_string)
            for (index, case_result) in enumerate(assign.case_results)
        ]
        strings.append(
            handle_case_result(assign.default_result, 'only' if len(assign.case_results) == 0 else 'default', init_mode, indent_level, assign_var, env_board, env_board_random, env_board_generator, update_generator, update_env_board, board_env_name, blackboard_name, environment_name, 0, value_only_mode, random_gen_string)
        )
        return_string = ''.join(map(lambda x: x[0], strings))
        where_string = ''.join(map(lambda x: x[1], strings))
        return (
            return_string + os.linesep
            + ('' if board_env_name is None else board_env_post_script(indent_level, board_env_name, blackboard_name, environment_name))
            + ('' if where_string == '' else ((indent(indent_level + 1) + 'where' + os.linesep) if board_env_name is None else ''))
            + where_string
        )

    def handle_initial_value(assign, var_type, indent_level, init_mode, partial_string, node_location, array_index = None):
        blackboard_name = 'blackboard'
        environment_name = 'environment'
        if array_index is not None:
            constants['serene_index'].append(array_index)

        def post_script(indent_level):
            return (
                indent(indent_level + 1) + 'where' + os.linesep
                + indent(indent_level + 2) + (blackboard_name if init_mode == 'board' else environment_name) + ' = ' +  partial_string + os.linesep
                + ((indent(indent_level + 2) + 'nodeLocation = ' + str(node_location) + os.linesep) if node_location is not None else '')
            )

        if len(assign.case_results) == 0:
            if (not assign.default_result.range_mode) and len(assign.default_result.values) == 1:
                return (
                    ' = (' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + ', curGen)' + os.linesep
                    + post_script(indent_level)
                )

        def create_random_func(function_name, values, range_mode, var_type, cond_func, random_range, indent_level):
            if range_mode:
                return (
                    indent(indent_level + 2) + function_name + ' :: Integer -> ' + var_type + os.linesep
                    + ''.join(
                        [
                            (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                            for index, value in enumerate(filter(cond_func, range(handle_constant(values[0], False), handle_constant(values[1], False) + 1)))
                        ]
                    )
                )
            if len(values) > 1:
                return (
                    indent(indent_level + 2) + function_name + ' :: Integer -> ' + var_type + os.linesep
                    + ''.join(
                        [
                            (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, blackboard_name, environment_name) + os.linesep)
                            for index, value in enumerate(values)
                        ]
                    )
                )
            return ''

        default = assign.default_result
        case_result = None
        return_string = ('' if len(assign.case_results) == 0 else os.linesep)
        where_string = ''
        unique_id = 0
        for case_result in assign.case_results:
            return_string += (
                indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, blackboard_name, environment_name) + ' = '
            )
            if (not case_result.range_mode) and (len(case_result.values) == 1):
                cond_func = None
                random_range = 0
                function_name = ''
            elif case_result.range_mode:
                cond_func = build_range_func(case_result.values[2], constants)
                random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1
            else:
                cond_func = None
                random_range = len(case_result.values) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1

            return_string += (
                (
                    '(' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name) + ', curGen)' + os.linesep
                )
                if (not case_result.range_mode) and (len(case_result.values) == 1)
                else
                (
                    '(' + function_name + ' (fst (getRandomInteger curGen ' + str(random_range) + ')), snd (getRandomInteger curGen ' + str(random_range) + '))' + os.linesep
                )
            )
            where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
        case_result = default
        return_string += (
            (
                ' = '
            )
            if len(assign.case_results) == 0
            else
            (
                indent(indent_level + 1) + '| otherwise = '
            )
        )
        if (not case_result.range_mode) and (len(case_result.values) == 1):
            cond_func = None
            random_range = 0
            function_name = ''
        elif case_result.range_mode:
            cond_func = build_range_func(case_result.values[2], constants)
            random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1
        else:
            cond_func = None
            random_range = len(case_result.values) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1

        return_string += (
            ('(' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name) + ', curGen)' + os.linesep)
            if (not case_result.range_mode) and (len(case_result.values) == 1)
            else
            ('(' + function_name + ' (fst (getRandomInteger curGen ' + str(random_range) + ')), snd (getRandomInteger curGen ' + str(random_range) + '))' + os.linesep)
        )
        where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
        return return_string + post_script(indent_level) + (where_string if unique_id > 0 else '')

    def handle_update_value(assign, variable_name, var_type, indent_level, init_mode):
        blackboard_name = 'blackboard'
        environment_name = 'environment'
        if len(assign.case_results) == 0:
            if (not assign.default_result.range_mode) and len(assign.default_result.values) == 1:
                return (' = environment { env' + pascal_case(variable_name) + ' = ' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + '}' + os.linesep)

        def post_script(indent_level):
            return (
                indent(indent_level + 1) + 'where' + os.linesep
            )

        def create_random_func(function_name, values, range_mode, var_type, cond_func, random_range, indent_level):
            if range_mode:
                return (
                    indent(indent_level + 2) + function_name + ' :: Integer -> ' + var_type + os.linesep
                    + ''.join(
                        [
                            (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                            for index, value in enumerate(filter(cond_func, range(handle_constant(values[0], False), handle_constant(values[1], False) + 1)))
                        ]
                    )
                )
            if len(values) > 1:
                return (
                    indent(indent_level + 2) + function_name + ' :: Integer -> ' + var_type + os.linesep
                    + ''.join(
                        [
                            (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, blackboard_name, environment_name) + os.linesep)
                            for index, value in enumerate(values)
                        ]
                    )
                )
            return ''

        default = assign.default_result
        return_string = ('' if len(assign.case_results) == 0 else os.linesep)
        where_string = ''
        unique_id = 0
        for case_result in assign.case_results:
            return_string += (
                indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, blackboard_name, environment_name) + ' = '
            )
            if (not case_result.range_mode) and (len(case_result.values) == 1):
                cond_func = None
                random_range = 0
                function_name = ''
            elif case_result.range_mode:
                cond_func = build_range_func(case_result.values[2], constants)
                random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1
            else:
                cond_func = None
                random_range = len(case_result.values) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1

            return_string += (
                (
                    'environment { env' + pascal_case(variable_name) + ' = ' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name) + ' }' + os.linesep
                )
                if (not case_result.range_mode) and (len(case_result.values) == 1)
                else
                (
                    'environment { sereneEnvGenerator = (snd (getRandomInteger (sereneEnvGenerator environment) ' + str(random_range) + ')), env' + pascal_case(variable_name) + ' = ' + function_name + ' (fst (getRandomInteger (sereneEnvGenerator environment) ' + str(random_range) + ')) }' + os.linesep
                )
            )
            where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
        return_string += (
            (
                ' = '
            )
            if len(assign.case_results) == 0
            else
            (
                indent(indent_level + 1) + '| otherwise = '
            )
        )
        if (not default.range_mode) and (len(default.values) == 1):
            cond_func = None
            random_range = 0
            function_name = ''
        elif default.range_mode:
            cond_func = build_range_func(default.values[2], constants)
            random_range = len(list(filter(cond_func, range(handle_constant(default.values[0], False), handle_constant(default.values[1], False) + 1)))) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1
        else:
            cond_func = None
            random_range = len(default.values) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1

        return_string += (
            ('environment { env' + pascal_case(variable_name) + ' = ' + format_code(default.values[0], init_mode, blackboard_name, environment_name) + ' }' + os.linesep)
            if (not default.range_mode) and (len(default.values) == 1)
            else
            ('environment { sereneEnvGenerator = (snd (getRandomInteger (sereneEnvGenerator environment) ' + str(random_range) + ')), env' + pascal_case(variable_name) + ' = ' + function_name + ' (fst (getRandomInteger (sereneEnvGenerator environment) ' + str(random_range) + ')) }' + os.linesep)
        )
        where_string += create_random_func(function_name, default.values, default.range_mode, var_type, cond_func, random_range, indent_level)
        return return_string + ((post_script(indent_level) + where_string) if unique_id > 0 else '')

    def create_macro(assign, indent_level, init_mode, array_index = None):
        blackboard_name = 'blackboard'
        environment_name = 'environment'
        if array_index is not None:
            constants['serene_index'].append(array_index)
        return_string = (
            (' = ' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep)
            if len(assign.case_results) == 0
            else
            (
                os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, blackboard_name, environment_name) + ' = ' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep)
                        for case_result in assign.case_results
                    ]
                )
                + (indent(indent_level + 1) + '| otherwise = ' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep)
            )
        )
        if array_index is not None:
            constants['serene_index'].pop()
        return return_string

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
        var_type = variable_type(variable)
        if var_type == 'Integer':
            return '0'
        if var_type == 'Bool':
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
        data_type_name = 'BTreeBlackboard' if blackboard_mode else 'BTreeEnvironment'
        data_type_name_2 = 'BTreeBlackboard' if blackboard_mode else 'BTreeBlackboard -> BTreeEnvironment'
        board_env_cap = 'Board' if blackboard_mode else 'Env'
        board_env = 'board' if blackboard_mode else 'env'
        blackboard_name = 'blackboard'
        environment_name = 'environment'
        var_name = blackboard_name if blackboard_mode else environment_name
        var_name_2 = blackboard_name if blackboard_mode else (blackboard_name + ' ' + environment_name)
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
            # + (
            #     'instance Show ' + data_type_name + ' where' + os.linesep
            #     + indent(1) + 'show (' + data_type_name + ' _ '
            #     + ' '.join(map(lambda x: x['field_name'], create_order))
            #     + ') = '
            #     + '"' + board_env_cap + ' = {"'
            #     + ' ++ '
            #     + ' ++ '.join(
            #         [
            #             ('"' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
            #             if index == 0
            #             else
            #             ('", ' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
            #             for index, variable_info in enumerate(create_order)
            #         ]
            #     )
            #     + (' ++ ' if len(create_order) > 0 else '')
            #     + '"}"' + os.linesep
            # )
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
                    (
                        board_env + pascal_case(variable.name) + ' :: ' + data_type_name_2 + ' -> ' + variable_type(variable) + os.linesep
                        + board_env + pascal_case(variable.name) + ' ' + var_name_2 + create_macro(variable.assign, 0, None, array_index = None)  # init_mode none here because we are operating in a func
                    )
                    for variable in model.variables if (variable.model_as == 'DEFINE' and is_non_local(variable) and not is_array(variable))
                ]
            )
            + ''.join(
                map(
                    lambda variable:
                    board_env + pascal_case(variable.name) + ' :: Integer -> ' + data_type_name_2 + ' -> ' + variable_type(variable) + os.linesep
                    + ''.join(
                        map(
                            lambda index:
                            board_env + pascal_case(variable.name) + ' ' + str(index) + ' ' + var_name_2 + create_macro(variable.assign if variable.array_mode == 'range' else variable.assigns[index], 0, None, array_index = index),
                            range(handle_constant(variable.array_size, False))
                        )
                    )
                    + board_env + pascal_case(variable.name) + (' ' if blackboard_mode else ' _ ') + '_ _ = error "' + board_env + pascal_case(variable.name) + ' illegal index value"' + os.linesep,
                    filter(lambda variable: variable.model_as == 'DEFINE' and is_non_local(variable) and is_array(variable), model.variables)
                )
            )
            # created accessor functions for define non-local ---------------------------------------------------------------------------------------
            + (
                (
                    os.linesep + '-- START OF LOCAL BLACKBOARD FUNCTIONS' + os.linesep + os.linesep
                    + ''.join(
                        [
                            (
                                'local' + board_env_cap + pascal_case(variable.name) + ' :: Integer -> ' + data_type_name_2 + ' -> ' + variable_type(variable) + os.linesep
                                + (
                                    ''.join(local_macros[variable.name])
                                    if variable.name in local_macros
                                    else
                                    ''
                                )
                                + 'local' + board_env_cap + pascal_case(variable.name) + ' _ _ = error "' + variable.name + ' illegal local reference"' + os.linesep
                                # this one needs two _ because unlike the other one, we aren't doing eta reduction
                                # we handle each case in the recursive call and now just need to combine them.
                                # + 'localBoard' + pascal_case(variable.name) + ' nodeLocation blackboard' + create_macro(variable.assign, 0, None)  # init_mode none here because we are operating in a func
                            )
                            for variable in model.variables if (variable.model_as == 'DEFINE' and is_local(variable) and not is_array(variable) and variable.name in local_var_to_nodes)
                        ]
                    )
                    + ''.join(
                        map(
                            lambda variable:
                            'local' + board_env_cap + pascal_case(variable.name) + ' :: Integer -> Integer -> ' + data_type_name_2 + ' -> ' + variable_type(variable) + os.linesep
                            + ''.join(map(lambda location: 'local' + board_env_cap + pascal_case(variable.name) + ' ' + str(location) + ' = local' + board_env_cap + pascal_case(variable.name) + 'Location' + str(location) + os.linesep, local_var_to_nodes[variable.name]))
                            + 'local' + board_env_cap + pascal_case(variable.name) + ' _ = error "local' + board_env_cap + pascal_case(variable.name) + ' illegal local reference"' + os.linesep
                            + ''.join(local_macros[variable.name])
                            ,
                            filter(lambda variable: variable.model_as == 'DEFINE' and is_local(variable) and is_array(variable) and variable.name in local_var_to_nodes, model.variables)
                        )
                    )
                    # created accessor functions for define local
                    # ---------------------------------------------------------------------------------------
                    + os.linesep + '-- START OF GET FUNCTIONS FOR LOCAL VARIABLES' + os.linesep + os.linesep
                    + ''.join(
                        [
                            (
                                'local' + board_env_cap + pascal_case(variable.name) + ' :: Integer' + (' -> Integer ' if is_array(variable) else ' ') + '-> ' + data_type_name + ' -> ' + variable_type(variable) + os.linesep
                                + (
                                    ''.join(
                                        [
                                            ('local' + board_env_cap + pascal_case(variable.name) + ' ' + str(number) + ' = local' + board_env_cap + pascal_case(variable.name) + 'Location' + str(number) + os.linesep)
                                            for number in local_var_to_nodes[variable.name]
                                        ]
                                    )
                                    if variable.name in local_var_to_nodes
                                    else
                                    ''
                                )
                                + 'local' + board_env_cap + pascal_case(variable.name) + ' _ = error "' + variable.name + ' illegal local reference"' + os.linesep
                            )
                            for variable in model.variables if (variable.model_as != 'DEFINE' and is_local(variable) and variable.name in local_var_to_nodes)
                        ]
                    )
                    # the above creates accessor functions to get local variables. ---------------------------------------------------------------------------------------
                )
                if blackboard_mode
                else
                ''
            )
            + os.linesep + '-- START OF GET FUNCTIONS FOR ARRAYS' + os.linesep + os.linesep
            + ''.join(
                [
                    board_env + pascal_case(variable.name) + ' :: Integer -> ' + data_type_name + ' -> ' + variable_type(variable) + os.linesep
                    + ''.join(
                        [
                            (board_env + pascal_case(variable.name) + ' ' + str(index) + ' = ' + board_env + pascal_case(variable.name) + 'Index' + str(index) + os.linesep)
                            for index in range(handle_constant(variable.array_size, False))
                        ]
                    )
                    + board_env + pascal_case(variable.name) + ' _ = error "' + board_env + pascal_case(variable.name) + ' illegal index value"' + os.linesep
                    for variable in model.variables if (variable.model_as != 'DEFINE' and is_non_local(variable) and is_array(variable))
                ]
            )
            + (
                ''.join(
                    [
                        'local' + board_env_cap + pascal_case(variable.name) + 'Location' + str(variable_location) + ' :: Integer -> ' + data_type_name_2 + ' -> ' + variable_type(variable) + os.linesep
                        + ''.join(
                            [
                                ('local' + board_env_cap + pascal_case(variable.name) + 'Location' + str(variable_location) + ' ' + str(index) + ' = local' + board_env_cap + pascal_case(variable.name) + 'Location' + str(variable_location) + 'Index' + str(index) + os.linesep)
                                for index in range(handle_constant(variable.array_size, False))
                            ]
                        )
                        + 'local' + board_env_cap + pascal_case(variable.name) + str(variable_location) + ' _ = error "local' + board_env_cap + pascal_case(variable.name) + str(variable_location) + ' illegal index value"' + os.linesep
                        for variable in model.variables if (variable.model_as != 'DEFINE' and is_local(variable) and is_array(variable) and (variable.name in local_var_to_nodes))
                        for variable_location in local_var_to_nodes[variable.name]
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
            + os.linesep + '-- START OF SET FUNCTIONS' + os.linesep + os.linesep
            + 'update' + board_env_cap + 'Generator :: ' + data_type_name + ' -> StdGen -> ' + data_type_name + os.linesep
            + 'update' + board_env_cap + 'Generator ' + var_name + ' newGen = ' + var_name + ' { serene' + board_env_cap + 'Generator = newGen }' + os.linesep
            # created an update for the random number generator
            # ---------------------------------------------------------------------------------------
            + (
                ''.join(
                    map(
                        lambda var:
                        (
                            'updateLocal' + board_env_cap + pascal_case(var.name) + ' :: Integer -> ' + data_type_name_2 + ' -> ' + variable_type(var) + ' -> ' + data_type_name + os.linesep
                            + ''.join(
                                map(
                                    lambda local_number:
                                    ('updateLocal' + board_env_cap + pascal_case(var.name) + ' ' + str(local_number) + ' = updateLocal' + board_env_cap + pascal_case(var.name) + 'Location' + str(local_number) + os.linesep)
                                    ,
                                    (local_var_to_nodes[var.name] if var.name in local_var_to_nodes else [])
                                )
                            )
                            + 'updateLocal' + board_env_cap + pascal_case(var.name) + ' _ = error "local' + board_env_cap + pascal_case(var.name) + ' illegal local reference"' + os.linesep
                        ),
                        filter(lambda var: (var.model_as == 'VAR' and is_local(var) and not is_array(var) and var.name in local_var_to_nodes), model.variables)
                    )
                )
                if blackboard_mode
                else
                ''
            )
            # created updaters for local variables which switches based on node location
            # ---------------------------------------------------------------------------------------
            + ''.join(
                [
                    (
                        'update' + pascal_case(variable['field_name']) + ' :: ' + data_type_name + ' -> ' + variable['type'] + ' -> ' + data_type_name + os.linesep
                        + 'update' + pascal_case(variable['field_name']) + ' ' + var_name + ' value = ' + var_name + ' { ' + variable['field_name'] + ' = (checkValue' + pascal_case(variable['category_name']) + ' value)}' + os.linesep
                    )
                    for variable in create_order if variable['model_as'] == 'VAR'
                ]
            )
            # created updaters for all fields. these are direct updaters. local variables reference these, as do array variables. these reference checkValue, see below.
            # ---------------------------------------------------------------------------------------
            + os.linesep + '-- START OF SET FUNCTIONS FOR ARRAYS' + os.linesep + os.linesep
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
                        format_code(model.tick_condition, None, blackboard_name, environment_name)
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
                                #+ indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' environment' + handle_update_value(update.assign, update.variable.name, variable_type(update.variable), 2, None)
                                + indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' environment' + handle_variable_statement(update, 2, None, None, 'blackboard', 'environment')
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
            + 'initial' + ('Blackboard' if blackboard_mode else 'Environment') + ' seed ' + ('' if blackboard_mode else (blackboard_name + ' ')) + '= ' + data_type_name + ' newSereneGenerator ' + ' '.join(map(lambda x : x['initial_name'], create_order))
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
                                'localBoard' + pascal_case(variable.name) + ' ' + str(my_int) + ' blackboard' + create_macro(cur_assign, 0, None)  # init_mode none here because we are operating in a func
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

    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    validate_model(model, constants)
    constants['serene_index'] = []
    arguments = set()

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
