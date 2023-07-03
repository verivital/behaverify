'''used to create haskell code from BehaVerify DSL for Behavior Trees'''
import argparse
import os
import shutil
import itertools
import textx
from behaverify_common import haskell_indent as indent, create_node_name

from check_model import (validate_model
                         # , constant_type
                         # , variable_type
                         , is_local
                         , is_env
                         , is_blackboard
                         # , variable_scope
                         , is_array
                         , build_range_func)


def variable_type(variable):
    '''returns the vaiable type, correctly formatted for haskell'''
    return (
        (
            'Int'
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
                    'String'
                    if isinstance(handle_constant(variable.domain.enums[0], False), str)
                    else
                    'Int'
                )
                if variable.domain.min_val is None
                else
                'Int'
            )
        )
    )


def pascal_case(variable_name):
    '''removes underscores, capitalizes'''
    return ''.join(
        map(
            lambda x: x.capitalize()
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
                x[1].capitalize()
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
    raise Exception('Array not implemented yet')


FUNCTION_FORMAT = {
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
    'equal' : ('==', format_function_between),
    'not_equal' : ('/=', format_function_between),
    'less_than' : ('<', format_function_between),
    'greater_than' : ('>', format_function_between),
    'less_than_or_equal' : ('<=', format_function_between),
    'greater_than_or_equal' : ('>=', format_function_between),
    'negative' : ('-', format_function_before),
    'addition' : ('+', format_function_between),
    'subtraction' : ('-', format_function_between),
    'multiplication' : ('*', format_function_between),
    'division' : ('quot', format_function_before),  # quot rounds to 0, which is what nuxmv does.
    'mod' : ('%', format_function_between),
    'count' : ('sereneCOUNT', format_function_count),  # probably not usable now
    'index' : ('index', format_function_index)  # definitely not usable now
}


def format_variable(variable, init_mode, blackboard_name, environment_name):
    '''used to format variable names'''
    # if debug:
    #     print('format variable: ' + str(init_mode, blackboard_name, environment_name))
    # no init_mode for local variables because other variables cannot depend on the initial values of local variables.
    # return (
    #     ('(localBoard' + pascal_case(variable.name) + ' nodeLocation blackboard)')
    #     if is_local(variable)
    #     else
    #     (
    #         (
    #             ('newVal' + pascal_case(variable.name))
    #             if init_mode == 'env'
    #             else
    #             (
    #                 ('(env' + pascal_case(variable.name) + ' blackboard environment)')
    #                 if variable.model_as == 'DEFINE'
    #                 else
    #                 ('(env' + pascal_case(variable.name) + ' environment)')
    #             )
    #         )
    #         if is_env(variable)
    #         else
    #         (
    #             ('newVal' + pascal_case(variable.name))
    #             if init_mode == 'board'
    #             else
    #             ('(board' + pascal_case(variable.name) + ' blackboard)')
    #         )
    #     )
    # )
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
    # if debug:
    #     print('code: ' + str(init_mode, blackboard_name, environment_name))
    return (
        (
            handle_constant(code.constant, True) if code.constant is not None else (
                format_variable(code.variable, init_mode, blackboard_name, environment_name) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, init_mode, blackboard_name, environment_name) + ')') if code.code_statement is not None else (
                        FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, init_mode, blackboard_name, environment_name)
                    )
                )
            )
        )
    )


def handle_constant(constant, str_conversion):
    '''used to handle constnts and replace them with integer values'''
    # global constants
    new_constant = (constants[constant] if constant in constants else constant)
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


def handle_variable_statement(assign, assign_var, indent_level, init_mode, board_env_string):
    '''handles variable statements'''
    variable_name = assign_var.name
    update_env_board = (
        'updateEnv'
        if is_env(assign_var)
        else
        (
            'localUpdateBoard'
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
        ' environment '
        if is_env(assign_var)
        else
        (
            ' nodeLocation blackboard '
            if is_local(assign_var)
            else
            ' blackboard '
        )
    )
    env_board_generator = (
        'sereneEnvGenerator'
        if is_env(assign_var)
        else
        (
            'sereneBoardGenerator'
        )
    )

    def post_script(indent_level):
        return (
            indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + '(blackboard, environment) = ' + board_env_string + os.linesep
        )

    def create_random_func(function_name, values, range_mode, var_type, cond_func, random_range, indent_level):
        # figure out where case_result is coming from.
        # i think it's defined below.
        if range_mode:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                        for index, value in enumerate(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))
                    ]
                )
            )
        if len(values) > 1:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, 'blackboard', 'environment') + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        return ''

    if is_array(assign_var):
        print('ARRAY VARIABLES NOT YET SUPPORTED')
        raise Exception('Array not supported')

    else:
        case_result = None
        default = assign.default_result
        if len(assign.case_results) == 0:
            if (not default.range_mode) and len(default.values) == 1:
                return (
                    ' = '
                    + ('(blackboard, ' if is_env(assign_var) else '(')
                    + update_env_board + pascal_case(variable_name) + env_board + format_code(default.values[0], init_mode, 'blackboard', 'environment')
                    + (')' if is_env(assign_var) else ', environment)')
                    + os.linesep
                    + post_script(indent_level)
                )
        var_type = variable_type(assign_var)
        # var_type = ('Bool' if assign.variable.domain.boolean is not None else ('String' if assign.variable.domain.min_val is None else 'Int'))
        return_string = ('' if len(assign.case_results) == 0 else os.linesep)
        where_string = post_script(indent_level)
        unique_id = 0
        for case_result in assign.case_results:
            return_string += (
                indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, 'blackboard', 'environment') + ' = '
            )
            if (not case_result.range_mode) and (len(case_result.values) == 1):
                cond_func = None
                random_range = 0
                function_name = ''
            elif case_result.range_mode:
                cond_func = build_range_func(case_result.values[2])
                random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1
            else:
                cond_func = None
                random_range = len(case_result.values) - 1
                function_name = 'privateRandom' + str(unique_id)
                unique_id = unique_id + 1

            return_string += (
                ('(blackboard, ' if is_env(assign_var) else '(')
                + (
                    (
                        update_env_board + pascal_case(variable_name) + env_board + format_code(case_result.values[0], init_mode, 'blackboard', 'environment')
                    )
                    if (not case_result.range_mode) and (len(case_result.values) == 1)
                    else
                    (
                        update_generator + ' ('
                        + update_env_board + pascal_case(variable_name) + env_board
                        + '(' + function_name + ' (fst (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range)
                        + ')))) (snd (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range) + '))'
                    )
                )
                + (')' if is_env(assign_var) else ', environment)')
                + os.linesep
            )
            where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
        # we are now in the default case, but will simply rename case_result.
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
            cond_func = build_range_func(case_result.values[2])
            random_range = len(list(filter(cond_func, range(handle_constant(case_result.values[0], False), handle_constant(case_result.values[1], False) + 1)))) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1
        else:
            cond_func = None
            random_range = len(case_result.values) - 1
            function_name = 'privateRandom' + str(unique_id)
            unique_id = unique_id + 1

        return_string += (
            ('(blackboard, ' if is_env(assign_var) else '(')
            + (
                (
                    update_env_board + pascal_case(variable_name) + env_board + format_code(case_result.values[0], init_mode, 'blackboard', 'environment')
                )
                if (not case_result.range_mode) and (len(case_result.values) == 1)
                else
                (
                    update_generator + ' ('
                    + update_env_board + pascal_case(variable_name) + env_board
                    + '(' + function_name + ' (fst (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range)
                    + ')))) (snd (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range) + '))'
                )
            )
            + (')' if is_env(assign_var) else ', environment)')
            + os.linesep
        )
        where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
        return return_string + where_string


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
                indent(indent_level + 2) + '(conditionRandomInt, conditionRandomGenerator) = getRandomInt (sereneEnvGenerator (snd boardEnv)) 1' + os.linesep
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
                + ('localUpdateBoard' if is_local(cond_var) else '') + pascal_case(cond_var.name)
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
                    (indent(indent_level + 1) + '| nonDeterministicInt == 0 = privateTempBoardEnv0' + os.linesep)
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
                            + handle_variable_statement(variable_statement.assign, variable_statement.variable, indent_level + 2, init_mode, 'privateTempBoardEnv' + str(x + shift))
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
                handle_variable_statement(update.assign, update.variable, indent_level, init_mode, 'boardEnv')
            )
            for update in statement.update if update.instant
        ],
        [
            (
                handle_variable_statement(update.assign, update.variable, indent_level, init_mode, 'boardEnv')
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
        ([handle_variable_statement(statement.variable_statement.assign, statement.variable_statement.variable, indent_level, init_mode, 'boardEnv')], []) if statement.variable_statement is not None else (
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
    return (
        camel_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
        + camel_case(node.name) + ' _ nodeLocation _ _ _ _ blackboard environment futureChanges' + os.linesep
        + indent(1) + '| ' + format_code(node.condition, None, 'blackboard', 'environment') + ' = (Success, [], [], blackboard, environment, futureChanges)' + os.linesep
        + indent(1) + '| otherwise = (Failure, [], [], blackboard, environment, futureChanges)'
    )


def action_function(node):
    '''used to build action functions'''
    pre = len(node.pre_update_statements)
    post = len(node.post_update_statements)
    pre_updates = []
    delay_updates = []
    post_updates = []
    for index in range(pre):
        (new_pre, new_delay) = handle_statement(node.pre_update_statements[index], 2, None)
        pre_updates += new_pre
        delay_updates += new_delay
    for index in range(post):
        (new_post, new_delay) = handle_statement(node.post_update_statements[index], 2, None)
        post_updates += new_post
        delay_updates += new_delay
    # print(pre_updates)
    # print(post_updates)
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

    # def post_script(indent_level):
    #     return (
    #         indent(indent_level + 1) + 'where' + os.linesep
    #         + indent(indent_level + 2) + '(blackboard, environment) = boardEnv' + os.linesep
    #     )

    return (
        camel_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
        + camel_case(node.name) + ' _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)' + os.linesep
        + indent(1) + 'where' + os.linesep
        + ('').join(
            [
                (env_decl(index, 2) + value)
                for index, value in enumerate(pre_updates)
            ]
        )
        + handle_return_statement(node.return_statement)
        + ('').join(
            [
                (env_decl(index + pre, 2) + value)
                for index, value in enumerate(post_updates)
            ]
        )
        + ('').join(
            [
                (code_decl(index, 2) + value)
                for index, value in enumerate(delay_updates)
            ]
        )
        + indent(2) + 'preStatusBoardEnv = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre))))) + (' $ ' if pre > 1 else ' ') + '(oldBlackboard, oldEnvironment)' + os.linesep
        + indent(2) + 'returnStatus = returnStatement preStatusBoardEnv' + os.linesep
        + indent(2) + '(newBlackboard, newEnvironment) = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre, pre + post))))) + (' $ ' if post > 1 else ' ') + 'preStatusBoardEnv' + os.linesep
        + indent(2) + 'newFutureChanges = ' + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, reversed(range(delay))))) + (' : ' if delay > 0 else '') + 'futureChanges' + os.linesep
    )


def build_check_node(node):
    '''sequence to build check nodes'''
    return (module_declaration(node.name)
            + STANDARD_IMPORTS
            + os.linesep
            + os.linesep
            + check_function(node)
            )


def build_check_environment_node(node):
    '''just calls check node lol'''
    return build_check_node(node)


def build_action_node(node):
    '''action node sequence'''
    return (module_declaration(node.name)
            + STANDARD_IMPORTS
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
            # print(dir(current_node))
            current_node = current_node.sub_root
    root_name = current_node.name
    return (
        'module Main where' + os.linesep
        + 'import ' + pascal_case(name) + os.linesep
        + 'import BehaviorTreeCore' + os.linesep
        + 'import BehaviorTreeEnvironment' + os.linesep
        + 'import BehaviorTreeBlackboard' + os.linesep
        + 'import System.Environment (getArgs)' + os.linesep
        + ''.join([('import BTree' + pascal_case(node.name) + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
        + os.linesep + os.linesep
        + 'executeFromSeeds :: Int -> Int -> Int -> [(BTreeBlackboard, BTreeEnvironment)]' + os.linesep
        + 'executeFromSeeds seed1 seed2 maxIteration = eachBoardEnv' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'initBoard = initialBlackboard seed1' + os.linesep
        + indent(2) + 'initEnv = initialEnvironment seed2 initBoard' + os.linesep
        + indent(2) + 'treeRoot = bTreeNode' + pascal_case(root_name) + os.linesep
        + indent(2) + 'executionChain :: Int -> TrueMemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]' + os.linesep
        + indent(2) + 'executionChain count memory partial blackboard environment' + os.linesep
        + indent(3) + '| count >= maxIteration = [(blackboard, environment)]' + os.linesep
        + indent(3) + '| not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]' + os.linesep
        + indent(3) + '| otherwise = (blackboard, environment) : executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv' + os.linesep
        + indent(3) + 'where' + os.linesep
        + indent(4) + '(_, nextMemory, nextPartial, tempBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment' + os.linesep
        + indent(4) + '(nextBoard, nextEnv) = betweenTickUpdate (applyFutureChanges futureChanges (tempBoard, tempEnv))' + os.linesep
        + indent(2) + 'eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv'
        + os.linesep + os.linesep
        + 'main :: IO ()' + os.linesep
        + 'main =' + os.linesep
        + indent(1) + 'do {' + os.linesep
        + indent(2) + 'args <- getArgs' + os.linesep
        + indent(2) + '; let (seed1, seed2) = seedFromArgs args in mapM_ print (executeFromSeeds seed1 seed2 ' + str(int(max_iter) + 1) + ')' + os.linesep
        + indent(1) + '}' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'seedFromArgs :: [String] -> (Int, Int)' + os.linesep
        + indent(2) + 'seedFromArgs [] = (0, 0)' + os.linesep
        + indent(2) + 'seedFromArgs curArgs' + os.linesep
        + indent(3) + '| null (tail curArgs) = (read (head curArgs), 0)' + os.linesep
        + indent(3) + '| otherwise = (read (head curArgs), read (head (tail curArgs)))' + os.linesep
    )


def create_tree(model, name):
    '''walks the tree to find stuff'''
    def node_function(node):
        if node.node_type == 'selector' or node.node_type == 'sequence':
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
        elif node.node_type == 'parallel':
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
        else:
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

    def walk_tree_recursive(current_node, node_names, node_names_map, running_string, running_int, indent_level):
        while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            else:
                # print(dir(current_node))
                current_node = current_node.sub_root

        conflict_avoid_name = 'bTreeNode' + pascal_case(current_node.name)

        (node_name, modifier) = create_node_name(conflict_avoid_name, node_names, node_names_map)
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        running_int = running_int + 1
        my_int = running_int

        # ----------------------------------------------------------------------------------
        # start of massive if statements
        # -----------------------------------------------------------------------------------
        if current_node.node_type in ('check', 'check_environment', 'action'):
            running_string = running_string + (
                indent(indent_level) + node_name + ' = BTreeNode ' + camel_case(current_node.name) + ' [] ' + str(my_int) + os.linesep
            )
        else:
            child_names = []
            node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
            for child in node_children:
                (child_name, cur_node_names, cur_node_names_map, running_string, running_int, indent_level) = walk_tree_recursive(child, cur_node_names, cur_node_names_map, running_string, running_int, indent_level)
                child_names.append(child_name)
            running_string = running_string + (
                indent(indent_level) + node_name + ' = BTreeNode ' + node_function(current_node) + ' ' + '[' + ', '.join(child_names) + '] ' + str(my_int) + os.linesep
                # this is wrong, and will need to change the current_node.name with the node type, but i'm lazy right now.
            )
        return (
            (
                (
                    node_name,
                    cur_node_names,
                    cur_node_names_map,
                    running_string,
                    running_int,
                    indent_level
                )
            )
        )

    (_, _, _, node_declarations, _, _) = walk_tree_recursive(model.root, set(), {}, '', -1, 0)

    return (
        'module ' + pascal_case(name) + ' where' + os.linesep
        + 'import BehaviorTreeCore' + os.linesep
        + ''.join([('import BTree' + pascal_case(node.name) + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
        + node_declarations
    )


def handle_initial_value(assign, variable, var_type, indent_level, init_mode, partial_string, node_location):
    blackboard_name = 'blackboard'
    environment_name = 'environment'

    def post_script(indent_level):
        return (
            indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + ('blackboard = ' if init_mode == 'board' else 'environment = ') + partial_string + os.linesep
            + ((indent(indent_level + 2) + 'nodeLocation = ' + str(node_location) + os.linesep) if node_location is not None else '')
        )

    if is_array(variable):
        raise Exception('Array not allowed yet')
    if len(assign.case_results) == 0:
        if (not assign.default_result.range_mode) and len(assign.default_result.values) == 1:
            return (
                ' = (' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + ', curGen)' + os.linesep
                + post_script(indent_level)
            )

    def create_random_func(function_name, values, range_mode, var_type, cond_func, random_range, indent_level):
        if range_mode:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                        for index, value in enumerate(filter(cond_func, range(handle_constant(values[0], False), handle_constant(values[1], False) + 1)))
                    ]
                )
            )
        elif len(values) > 1:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, blackboard_name, environment_name) + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        else:
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
            cond_func = build_range_func(case_result.values[2])
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
                '(' + function_name + ' (fst (getRandomInt curGen ' + str(random_range) + ')), snd (getRandomInt curGen ' + str(random_range) + '))' + os.linesep
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
        cond_func = build_range_func(case_result.values[2])
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
            '(' + function_name + ' (fst (getRandomInt curGen ' + str(random_range) + ')), snd (getRandomInt curGen ' + str(random_range) + '))' + os.linesep
        )
    )
    where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
    # return return_string + ((post_script(indent_level) + where_string) if unique_id > 0 else '')
    return return_string + post_script(indent_level) + (where_string if unique_id > 0 else '')

# debug = False
def handle_update_value(assign, variable_name, var_type, indent_level, init_mode):
    # print('----------------------------------------------------------------------')
    # global debug
    # debug = True
    # print('update: ' + str(init_mode, blackboard_name, environment_name))
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
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + str(value) + os.linesep)
                        for index, value in enumerate(filter(cond_func, range(handle_constant(values[0], False), handle_constant(values[1], False) + 1)))
                    ]
                )
            )
        elif len(values) > 1:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, init_mode, blackboard_name, environment_name) + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        else:
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
            cond_func = build_range_func(case_result.values[2])
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
                'environment { sereneEnvGenerator = (snd (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')), env' + pascal_case(variable_name) + ' = ' + function_name + ' (fst (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')) }' + os.linesep
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
        cond_func = build_range_func(default.values[2])
        random_range = len(list(filter(cond_func, range(handle_constant(default.values[0], False), handle_constant(default.values[1], False) + 1)))) - 1
        function_name = 'privateRandom' + str(unique_id)
        unique_id = unique_id + 1
    else:
        cond_func = None
        random_range = len(default.values) - 1
        function_name = 'privateRandom' + str(unique_id)
        unique_id = unique_id + 1

    return_string += (
        (
            'environment { env' + pascal_case(variable_name) + ' = ' + format_code(default.values[0], init_mode, blackboard_name, environment_name) + ' }' + os.linesep
        )
        if (not default.range_mode) and (len(default.values) == 1)
        else
        (
            'environment { sereneEnvGenerator = (snd (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')), env' + pascal_case(variable_name) + ' = ' + function_name + ' (fst (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')) }' + os.linesep
        )
    )
    where_string += create_random_func(function_name, default.values, default.range_mode, var_type, cond_func, random_range, indent_level)
    # debug = False
    return return_string + ((post_script(indent_level) + where_string) if unique_id > 0 else '')


def create_macro(assign, indent_level, init_mode):
    blackboard_name = 'blackboard'
    environment_name = 'environment'
    if len(assign.case_results) == 0:
        return ' = ' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep
    return (
        os.linesep
        + ''.join(
            [
                (indent(indent_level + 1) + '| ' + format_code(case_result.condition, init_mode, blackboard_name, environment_name) + ' = ' + format_code(case_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep)
                for case_result in assign.case_results
            ]
        )
        + (indent(indent_level + 1) + '| otherwise = ' + format_code(assign.default_result.values[0], init_mode, blackboard_name, environment_name) + os.linesep)
    )


def safe_update(variable, env_mode, local_mode, local_numbers = []):
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
            'Int -> BTreeBlackboard'
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
                                        # [
                                        #     (function_name + ' ' + str(number) + ' ' + board_type + ' "' + str(value) + '" = ' + board_type + ' { ' + field_name + str(number) + ' = value }' + os.linesep)
                                        #     for value in variable.domain.enums
                                        # ]
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
                                # [
                                #     (function_name + ' ' + board_type + ' "' + str(value) + '" = ' + board_type + ' { ' + field_name + ' = "' + str(value) + '" }' + os.linesep)
                                #     for value in variable.domain.enums
                                # ]
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
    if var_type == 'Int':
        return '0'
    if var_type == 'Bool':
        return 'True'
    return '" "'


def create_environment(model):
    blackboard_name = 'blackboard'
    environment_name = 'environment'
    # names_to_types = {
    #     variable.name : (('Array' + pascal_case(variable.name)) if is_array(variable) else variable_type(variable))
    #     for variable in model.variables if (is_env(variable) and variable.model_as != 'DEFINE')
    # }
    # initial_values = {
    #     variable.name : handle_initial_value(variable.assign, variable, names_to_types[variable.name], 2, 'env', 'partialEnvironment' + pascal_case(variable.name), None)
    #     for index, variable in enumerate(model.variables) if (is_env(variable) and variable.model_as != 'DEFINE')
    # }
    create_order = (
        [
            {
                'initial_name' : 'newVal' + pascal_case(variable.name),
                'initial_func' : 'initVal' + pascal_case(variable.name),
                'field_name' : 'env' + pascal_case(variable.name),
                'partial_name' : 'partialEnvironment' + pascal_case(variable.name),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : handle_initial_value(variable.assign, variable, variable_type(variable), 2, 'env', 'partialEnvironment' + pascal_case(variable.name), None)
            }
            for variable in model.variables if (variable.model_as != 'DEFINE' and is_env(variable))
        ]
    )
    return (
        'module BehaviorTreeEnvironment where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + 'import BehaviorTreeBlackboard' + os.linesep
        + 'import SereneOperations' + os.linesep
        + os.linesep
        + ''.join(
            [
                (
                    'data Array' + pascal_case(variable.name) + ' = Array' + pascal_case(variable.name) + ' {' + os.linesep
                    + indent(1) + ', '
                    + (indent(1) + ', ').join(map(
                        lambda x : ('val' + str(x) + ' :: Int' + os.linesep),
                        range(variable.array_size)
                        ))
                    + indent(1) + '}' + os.linesep
                    + os.linesep
                )
                for variable in model.variables if (is_env(variable) and is_array(variable) and variable.model_as != 'DEFINE')
            ]
        )
        + 'data BTreeEnvironment = BTreeEnvironment {' + os.linesep
        + indent(1) + 'sereneEnvGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(create_order) > 0 else '')
        + (os.linesep + indent(1) + ', ').join([(variable_info['field_name'] + ' :: ' + variable_info['type']) for variable_info in create_order])
        + (os.linesep if len(create_order) > 0 else '')
        + indent(1) + '}' + os.linesep + os.linesep
        + (
            'instance Show BTreeEnvironment where' + os.linesep
            + indent(1) + 'show (BTreeEnvironment _ '
            + ' '.join(map(lambda x : x['field_name'], create_order))
            + ') = '
            + '"Env = {"'
            + ' ++ '
            + ' ++ '.join(
                [
                    ('"' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
                    if index == 0
                    else
                    ('", ' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
                    for index, variable_info in enumerate(create_order)
                ]
            )
            + (' ++ ' if len(create_order) > 0 else '')
            + '"}"' + os.linesep
        )
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'env' + pascal_case(variable.name) + ' :: BTreeBlackboard -> BTreeEnvironment -> ' + variable_type(variable) + os.linesep
                    + 'env' + pascal_case(variable.name) + ' blackboard environment' + create_macro(variable.assign, 0, init_mode = None)  # init_mode none here because we are operating in a func
                )
                for variable in model.variables if (variable.model_as == 'DEFINE' and is_env(variable))
            ]
        )
        + os.linesep + os.linesep
        + 'updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment' + os.linesep
        + 'updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }' + os.linesep
        + ''.join(
            map(
                lambda var :
                safe_update(var, True, False)
                ,
                filter(lambda var :
                       var.model_as != 'DEFINE' and is_env(var)
                       ,
                       model.variables
                       )
            )
        )
        + 'checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool' + os.linesep
        + 'checkTickConditionTermination blackboard environment = ' + (
            'True'
            if model.tick_condition is None
            else
            format_code(model.tick_condition, None, blackboard_name, environment_name)
        ) + os.linesep + os.linesep
        + 'modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment' + os.linesep
        + 'modifiedID _ environment = environment' + os.linesep
        + 'applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
        + 'applyFutureChanges [] = id' + os.linesep
        + 'applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)' + os.linesep
        + os.linesep + os.linesep
        + 'betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
        + 'betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempEnvironment0 = curEnvironment' + os.linesep
        + indent(2) + 'newEnvironment = tempEnvironment' + str(len(model.update)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' :: BTreeEnvironment -> BTreeEnvironment' + os.linesep
                    + indent(2) + 'tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' environment' + handle_update_value(update.assign, update.variable.name, variable_type(update.variable), 2, None)
                    + os.linesep
                    + indent(2) + 'tempEnvironment' + str(index + 1) + ' = tickUpdate' + str(index + 1) + pascal_case(update.variable.name) + ' tempEnvironment' + str(index) + os.linesep
                    + os.linesep
                )
                for index, update in enumerate(model.update)
            ]
        ) + os.linesep
        + os.linesep + os.linesep
        + 'initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment' + os.linesep
        + 'initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator ' + ' '.join(map(lambda x : x['initial_name'], create_order)) + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(create_order)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + variable_info['partial_name'] + ' = BTreeEnvironment newSereneGenerator' + order_partial_arguments(variable_info['initial_name'], create_order) + os.linesep
                    + indent(2) + variable_info['initial_func'] + ' :: StdGen -> (' + variable_info['type'] + ', StdGen)' + os.linesep
                    + indent(2) + variable_info['initial_func'] + ' curGen' + variable_info['initial_value']
                    + os.linesep
                    + indent(2) + '(' + variable_info['initial_name'] + ', tempGen' + str(index + 1) + ') = ' + variable_info['initial_func'] + ' tempGen' + str(index) + os.linesep
                    + os.linesep
                )
                for index, variable_info in enumerate(create_order)
            ]
        ) + os.linesep
    )


# debug = False
def create_blackboard(model):

    def walk_tree_recursive_blackboard(current_node, node_names, node_names_map, running_dict, running_int, running_create_order):
        while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            else:
                # print(dir(current_node))
                current_node = current_node.sub_root

        conflict_avoid_name = current_node.name.replace(' ', '') + '__node'

        (node_name, modifier) = create_node_name(conflict_avoid_name, node_names, node_names_map)
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        running_int = running_int + 1
        my_int = running_int

        # ----------------------------------------------------------------------------------
        # start of massive if statements
        # -----------------------------------------------------------------------------------
        if current_node.node_type == 'action':
            for variable in current_node.local_variables:
                if variable.model_as == 'DEFINE':
                    cur_type = variable_type(variable)
                    if variable.name not in running_dict:
                        running_dict[variable.name] = []
                    cur_assign = variable.assign
                    for initial_statement in current_node.init_statements:
                        if initial_statement.variable.name == variable.name:
                            cur_assign = initial_statement.assign
                            break
                    running_dict[variable.name].append(
                        'localBoard' + pascal_case(variable.name) + ' ' + str(my_int) + ' blackboard' + create_macro(cur_assign, 0, None)  # init_mode none here because we are operating in a func
                        + indent(1) + 'where nodeLocation = ' + str(my_int) + os.linesep
                    )
                else:
                    cur_assign = variable.assign
                    overwritten = False
                    for initial_statement in current_node.init_statements:
                        if initial_statement.variable.name == variable.name:
                            cur_assign = initial_statement.assign
                            overwritten = True
                            break
                    cur_type = variable_type(variable)
                    running_create_order.append((variable,
                                                 my_int,
                                                 overwritten,
                                                 handle_initial_value(cur_assign, variable, cur_type, 2, 'board', 'partialBlackboard' + pascal_case(variable.name) + str(my_int), my_int)
                                                 ))
        elif current_node.node_type == 'check' or current_node.node_type == 'check_environment':
            # can't have local variables in checks.
            pass
        else:
            node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
            for child in node_children:
                (cur_node_names, cur_node_names_map, running_dict, running_int, running_create_order) = walk_tree_recursive_blackboard(child, cur_node_names, cur_node_names_map, running_dict, running_int, running_create_order)
        return (
            (
                (
                    cur_node_names,
                    cur_node_names_map,
                    running_dict,
                    running_int,
                    running_create_order
                )
            )
        )

    (_, _, local_macros, _, running_create_order) = walk_tree_recursive_blackboard(model.root, set(), {}, {}, -1, [])

    create_order = (
        [
            {
                'initial_name' : 'newVal' + pascal_case(variable.name),
                'initial_func' : 'initVal' + pascal_case(variable.name),
                'field_name' : 'board' + pascal_case(variable.name),
                'partial_name' : 'partialBlackboard' + pascal_case(variable.name),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : handle_initial_value(variable.assign, variable, variable_type(variable), 2, 'board', 'partialBlackboard' + pascal_case(variable.name), None)
            }
            for variable in model.variables if (variable.model_as != 'DEFINE' and is_blackboard(variable))
        ]
        +
        [
            {
                'initial_name' : 'localNewVal' + pascal_case(variable.name) + str(my_int),
                'initial_func' : 'localInitVal' + pascal_case(variable.name) + str(my_int),
                'field_name' : 'localBoard' + pascal_case(variable.name) + str(my_int),
                'partial_name' : 'partialBlackboard' + pascal_case(variable.name) + str(my_int),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : initial_value
            }
            for (variable, my_int, cur_overwritten, initial_value) in running_create_order if not cur_overwritten
        ]
        +
        [
            {
                'initial_name' : 'localNewVal' + pascal_case(variable.name) + str(my_int),
                'initial_func' : 'localInitVal' + pascal_case(variable.name) + str(my_int),
                'field_name' : 'localBoard' + pascal_case(variable.name) + str(my_int),
                'partial_name' : 'partialBlackboard' + pascal_case(variable.name) + str(my_int),
                'type' : variable_type(variable),
                'default_arg' : get_default_arg(variable),
                'initial_value' : initial_value
            }
            for (variable, my_int, cur_overwritten, initial_value) in running_create_order if cur_overwritten
        ]
    )

    local_var_to_nodes = {}
    for (variable, my_int, _, _) in running_create_order:
        name = variable.name
        if name in local_var_to_nodes:
            local_var_to_nodes[name].append(my_int)
        else:
            local_var_to_nodes[name] = [my_int]
    return (
        'module BehaviorTreeBlackboard where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + 'import SereneOperations' + os.linesep
        + os.linesep
        + 'data BTreeBlackboard = BTreeBlackboard {' + os.linesep
        + indent(1) + 'sereneBoardGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(create_order) > 0 else '')
        + (os.linesep + indent(1) + ', ').join([(variable_info['field_name'] + ' :: ' + variable_info['type']) for variable_info in create_order])
        + (os.linesep if len(create_order) > 0 else '')
        + indent(1) + '}' + os.linesep + os.linesep
        + (
            'instance Show BTreeBlackboard where' + os.linesep
            + indent(1) + 'show (BTreeBlackboard _ '
            + ' '.join(map(lambda x: x['field_name'], create_order))
            + ') = '
            + '"Board = {"'
            + ' ++ '
            + ' ++ '.join(
                [
                    ('"' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
                    if index == 0
                    else
                    ('", ' + variable_info['field_name'] + ': " ++ show ' + variable_info['field_name'])
                    for index, variable_info in enumerate(create_order)
                ]
            )
            + (' ++ ' if len(create_order) > 0 else '')
            + '"}"' + os.linesep
        )
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'localBoard' + pascal_case(variable.name) + ' :: Int -> BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + (
                        ''.join(
                            [
                                ('localBoard' + pascal_case(variable.name) + ' ' + str(number) + ' = localBoard' + pascal_case(variable.name) + str(number) + os.linesep)
                                for number in local_var_to_nodes[variable.name]
                            ]
                        )
                        if variable.name in local_var_to_nodes
                        else
                        ''
                    )
                    + 'localBoard' + pascal_case(variable.name) + ' _ = error "' + variable.name + ' illegal local reference"' + os.linesep
                )
                for variable in model.variables if (variable.model_as != 'DEFINE' and is_local(variable))
            ]
        )
        # the above creates custom functions to get local variables.
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'board' + pascal_case(variable.name) + ' :: BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + 'board' + pascal_case(variable.name) + ' blackboard' + create_macro(variable.assign, 0, None)  # init_mode none here because we are operating in a func
                )
                for variable in model.variables if (variable.model_as == 'DEFINE' and is_blackboard(variable))
            ]
        )
        + ''.join(
            [
                (
                    'localBoard' + pascal_case(variable.name) + ' :: Int -> BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + (
                        ''.join(local_macros[variable.name])
                        if variable.name in local_macros
                        else
                        ''
                    )
                    + 'localBoard' + pascal_case(variable.name) + ' _ _ = error "' + variable.name + ' illegal local reference"' + os.linesep
                    # this one needs two _ because unlike the other one, we aren't doing eta reduction
                    # we handle each case in the recursive call and now just need to combine them.
                    # + 'localBoard' + pascal_case(variable.name) + ' nodeLocation blackboard' + create_macro(variable.assign, 0, None)  # init_mode none here because we are operating in a func
                )
                for variable in model.variables if (variable.model_as == 'DEFINE' and is_local(variable))
            ]
        )
        + os.linesep + os.linesep
        + 'updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard' + os.linesep
        + 'updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }' + os.linesep
        + ''.join(
            map(
                lambda var :
                safe_update(var, False, False)
                ,
                filter(lambda var :
                       (var.model_as != 'DEFINE' and is_blackboard(var))
                       ,
                       model.variables
                       )
            )
        )
        + ''.join(
            map(
                lambda var :
                safe_update(var, False, True, (local_var_to_nodes[var.name] if var.name in local_var_to_nodes else []))
                ,
                filter(lambda var :
                       (var.model_as != 'DEFINE' and is_local(var))
                       ,
                       model.variables
                       )
            )
        )
        + os.linesep + os.linesep
        + 'initialBlackboard :: Int -> BTreeBlackboard' + os.linesep
        + 'initialBlackboard seed = BTreeBlackboard newSereneGenerator ' + ' '.join(map(lambda x : x['initial_name'], create_order))
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(create_order)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + variable_info['partial_name'] + ' = BTreeBlackboard newSereneGenerator' + order_partial_arguments(variable_info['initial_name'], create_order) + os.linesep
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
    )


def create_randomizer():
    return (
        'module SereneRandomizer where' + os.linesep
        + 'import System.Random' + os.linesep
        + os.linesep
        + 'getGenerator :: Int -> StdGen' + os.linesep
        + 'getGenerator = mkStdGen' + os.linesep
        + os.linesep
        + 'getRandomInt :: StdGen -> Int -> (Int, StdGen)' + os.linesep
        + 'getRandomInt generator maxValue = randomR (0, maxValue) generator' + os.linesep
        + os.linesep
    )


STANDARD_IMPORTS = ('import BehaviorTreeCore' + os.linesep
                    + 'import BehaviorTreeBlackboard' + os.linesep
                    + 'import BehaviorTreeEnvironment' + os.linesep
                    + 'import SereneRandomizer' + os.linesep
                    + 'import SereneOperations' + os.linesep
                    + os.linesep)


def create_serene_operations():
    '''returns a string with SereneOperations'''
    return (
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
        + 'sereneCOUNT :: Bool -> Bool -> Int' + os.linesep
        + 'sereneCOUNT True True = 2' + os.linesep
        + 'sereneCOUNT True False = 1' + os.linesep
        + 'sereneCOUNT False True = 1' + os.linesep
        + 'sereneCOUNT False False = 0' + os.linesep
        + os.linesep
    )


def main():

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

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    validate_model(model, constants, metamodel)

    my_location = args.location + 'app/'

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/haskell_file/BehaviorTreeCore.hs', my_location + 'BehaviorTreeCore.hs')

    with open(my_location + 'SereneRandomizer.hs', 'w') as f:
        f.write(create_randomizer())

    with open(my_location + 'SereneOperations.hs', 'w') as f:
        f.write(create_serene_operations())

    with open(my_location + 'BehaviorTreeEnvironment.hs', 'w') as f:
        f.write(create_environment(model))

    with open(my_location + 'BehaviorTreeBlackboard.hs', 'w') as f:
        f.write(create_blackboard(model))

    with open(my_location + pascal_case(args.output_file) + '.hs', 'w') as f:
        f.write(create_tree(model, args.output_file))

    with open(my_location + 'Main.hs', 'w') as f:
        f.write(create_runner(model, args.output_file, args.max_iter))

    for action in model.action_nodes:
        with open(my_location + 'BTree' + pascal_case(action.name) + '.hs', 'w') as f:
            f.write(build_action_node(action))
    for check in model.check_nodes:
        with open(my_location + 'BTree' + pascal_case(check.name) + '.hs', 'w') as f:
            f.write(build_check_node(check))
    for check_env in model.environment_checks:
        # print(check_env)
        with open(my_location + 'BTree' + pascal_case(check_env.name) + '.hs', 'w') as f:
            f.write(build_check_environment_node(check_env))

    return


if __name__ == '__main__':
    main()
