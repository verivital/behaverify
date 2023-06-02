import textx
import argparse
import os
# import sys
import shutil
import itertools
from behaverify_common import haskell_indent as indent, create_node_name
import serene_functions


def pascal_case(variable_name):
    return ''.join(
        map(
            lambda x: x.capitalize()
            ,
            variable_name.split('_')
        )
    )


def camel_case(variable_name):
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


def format_function_before(function_name, code, global_init = False):
    return (
        '('
        + function_name + ' '
        + ' '.join([format_code(value, global_init) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, global_init = False):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, global_init) for value in code.function_call.values])
        + ')'
        )


def format_variable(variable, is_local, is_env, global_init = False):
    return (
        ('(localBoard' + pascal_case(variable.name) + ' nodeLocation blackboard)')
        if is_local
        else
        (
            (
                ('newVal' + pascal_case(variable.name))
                if global_init == 'env'
                else
                (
                    ('(env' + pascal_case(variable.name) + ' blackboard environment)')
                    if variable.model_as == 'DEFINE'
                    else
                    ('(env' + pascal_case(variable.name) + ' environment)')
                )
            )
            if is_env
            else
            (
                ('newVal' + pascal_case(variable.name))
                if global_init == 'board'
                else
                ('(board' + pascal_case(variable.name) + ' blackboard)')
            )
        )
    )


def format_code(code, global_init = False):
    return (
        (
            handle_constant(code.constant) if code.constant is not None else (
                (format_variable(code.variable, code.mode == 'local', code.mode == 'env', global_init)) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, global_init) + ')') if code.code_statement is not None else (
                        FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, global_init)
                    )
                )
            )
        )
    )


def handle_constant(constant, str_conversion = True):
    global constants
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


def build_range_func(code):
    return (
        (lambda x : handle_constant(code.constant, False)) if code.constant is not None else (
            (lambda x : x) if code.value else (
                build_range_func(code.code_statement) if code.code_statement is not None else (
                    (lambda x : RANGE_FUNCTION[code.function_call.function_name]([build_range_func(value) for value in code.function_call.values], x))
                )
            )
        )
    )


def handle_variable_statement(statement, indent_level = 2, board_env_string = 'boardEnv'):
    variable_name = statement.variable.name
    update_env_board = (
        'updateEnv'
        if statement.mode == 'env'
        else
        (
            'localUpdateBoard'
            if statement.mode == 'local'
            else
            'updateBoard'
        )
    )
    update_generator = (
        'updateEnvGenerator'
        if statement.mode == 'env'
        else
        'updateBoardGenerator'
    )
    env_board = (
        ' environment '
        if statement.mode == 'env'
        else
        (
            ' nodeLocation blackboard '
            if statement.mode == 'local'
            else
            ' blackboard '
        )
    )
    env_board_generator = (
        'sereneEnvGenerator'
        if statement.mode == 'env'
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
        elif len(values) > 1:
            return (
                indent(indent_level + 2) + function_name + ' :: Int -> ' + var_type + os.linesep
                + ''.join(
                    [
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value) + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        else:
            return ''

    default = statement.default_result
    if len(statement.case_results) == 0:
        if (not default.range_mode) and len(default.values) == 1:
            return (
                ' = '
                + ('(blackboard, ' if statement.mode == 'env' else '(')
                + update_env_board + pascal_case(variable_name) + env_board + format_code(default.values[0])
                + (')' if statement.mode == 'env' else ', environment)')
                + os.linesep
                + post_script(indent_level)
            )
    var_type = ('Bool' if statement.variable.domain.boolean is not None else ('String' if statement.variable.domain.min_val is None else 'Int'))
    return_string = ('' if len(statement.case_results) == 0 else os.linesep)
    where_string = post_script(indent_level)
    unique_id = 0
    for case_result in statement.case_results:
        return_string += (
            indent(indent_level + 1) + '| ' + format_code(case_result.condition) + ' = '
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
            ('(blackboard, ' if statement.mode == 'env' else '(')
            + (
                (
                    update_env_board + pascal_case(variable_name) + env_board + format_code(case_result.values[0])
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
            + (')' if statement.mode == 'env' else ', environment)')
            + os.linesep
        )
        where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
    return_string += (
        (
            ' = '
        )
        if len(statement.case_results) == 0
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
        ('(blackboard, ' if statement.mode == 'env' else '(')
        + (
            (
                update_env_board + pascal_case(variable_name) + env_board + format_code(default.values[0])
            )
            if (not default.range_mode) and (len(default.values) == 1)
            else
            (
                update_generator + ' ('
                + update_env_board + pascal_case(variable_name) + env_board
                + '(' + function_name + ' (fst (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range)
                + ')))) (snd (getRandomInt (' + env_board_generator + ' blackboard) ' + str(random_range) + '))'
            )
        )
        + (')' if statement.mode == 'env' else ', environment)')
        + os.linesep
    )
    where_string += create_random_func(function_name, default.values, default.range_mode, var_type, cond_func, random_range, indent_level)
    return return_string + where_string


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


def handle_read_statement(statement, indent_level = 2):
    # todo: obviously not done.
    condition_code = (
        format_code(statement.condition)
        if statement.condition_variable is None
        else
        'conditionRandomInt == 1'
    )
    inject_string = (
        (indent(indent_level + 2) + 'privateTempBoardEnv0 = boardEnv' + os.linesep)
        if statement.condition_variable is None
        else
        (
            indent(indent_level + 2) + '(conditionRandomInt, conditionRandomGenerator) = getRandomInt (sereneBoardGenerator (fst boardEnv)) 1' + os.linesep
            + indent(indent_level + 2) + 'newBoardEnv = updateBoardGenerator (fst boardEnv) conditionRandomGenerator' + os.linesep
            + indent(indent_level + 2) + 'privateTempBoardEnv0 = newBoardEnv' + os.linesep
        )
    )
    return (
        [
            (
                os.linesep
                + indent(indent_level + 1) + '| ' + condition_code + ' = privateBoardEnv' + os.linesep
                + indent(indent_level + 1) + '| otherwise = boardEnv' + os.linesep  # this needs to be changed to handle non-determinism
                + indent(indent_level + 1) + 'where' + os.linesep
                + indent(indent_level + 2) + 'privateBoardEnv = privateTempBoardEnv' + str(len(statement.variable_statements)) + os.linesep
                + inject_string
                + ''.join(
                    [
                        (
                            indent(indent_level + 2) + 'privateTempBoardEnv' + str(x + 1)  # no os.linesep here intentionally, handled by varirable statement
                            + handle_variable_statement(variable_statement, indent_level + 2, 'privateTempBoardEnv' + str(x))
                        )
                        for x, variable_statement in enumerate(statement.variable_statements)
                    ]
                )
            )
        ],
        []
    )


def handle_write_statement(statement):
    return (
        [
            (
                handle_variable_statement(update)
            )
            for update in statement.update if update.instant
        ],
        [
            (
                handle_variable_statement(update)
            )
            for update in statement.update if not update.instant
        ]
    )


def format_returns(status_result):
    return status_result.status.capitalize()


def handle_return_statement(statement, indent_level = 2):
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
                            indent(indent_level + 1) + '| ' + format_code(case_result.condition) + ' = ' + format_returns(case_result) + os.linesep
                        )
                        for case_result in statement.case_results
                    ]
                )
                + indent(indent_level + 1) + '| otherwise = ' + format_returns(statement.default_result) + os.linesep
            )
        )
        + indent(indent_level + 1) + 'where' + os.linesep
        + indent(indent_level + 2) + '(blackboard, environment) = boardEnv' + os.linesep
    )  # todo: check if we're only handling the default case here.
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


def handle_statement(statement):
    return (
        ([handle_variable_statement(statement.variable_statement)], []) if statement.variable_statement is not None else (
            handle_read_statement(statement.read_statement) if statement.read_statement is not None else (
                handle_write_statement(statement.write_statement)
                )
            )
        )


def module_declaration(node_name):
    return ('module BTree' + pascal_case(node_name) + ' where' + os.linesep)


def check_function(node):
    return (
        camel_case(node.name) + ' :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
        + camel_case(node.name) + ' _ nodeLocation _ _ _ _ blackboard environment futureChanges' + os.linesep
        + indent(1) + '| ' + format_code(node.condition) + ' = (Success, [], [], blackboard, environment, futureChanges)' + os.linesep
        + indent(1) + '| otherwise = (Failure, [], [], blackboard, environment, futureChanges)'
    )


def action_function(node):
    pre = len(node.pre_update_statements)
    post = len(node.post_update_statements)
    pre_updates = []
    delay_updates = []
    post_updates = []
    for index in range(pre):
        (new_pre, new_delay) = handle_statement(node.pre_update_statements[index])
        pre_updates += new_pre
        delay_updates += new_delay
    for index in range(post):
        (new_post, new_delay) = handle_statement(node.post_update_statements[index])
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
        + camel_case(node.name) + ' _ nodeLocation _ _ _ _ blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)' + os.linesep
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
        + indent(2) + 'preStatusBoardEnv = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre))))) + (' $ ' if pre > 1 else ' ') + '(blackboard, environment)' + os.linesep
        + indent(2) + 'returnStatus = returnStatement preStatusBoardEnv' + os.linesep
        + indent(2) + '(newBlackboard, newEnvironment) = ' + ' . '.join(map(lambda x : 'boardEnvUpdate' + x, map(str, reversed(range(pre, pre + post))))) + (' $ ' if post > 1 else ' ') + 'preStatusBoardEnv' + os.linesep
        + indent(2) + 'newFutureChanges = ' + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, reversed(range(delay))))) + (' : ' if delay > 0 else '') + 'futureChanges' + os.linesep
    )


def build_check_node(node):
    return (module_declaration(node.name)
            + STANDARD_IMPORTS
            + os.linesep
            + os.linesep
            + check_function(node)
            )


def build_check_environment_node(node):
    return build_check_node(node)


def build_action_node(node):
    return (module_declaration(node.name)
            + STANDARD_IMPORTS
            + os.linesep
            + os.linesep
            + action_function(node)
            )


def create_runner(model, name):
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
        + indent(2) + 'treeRoot = bTreeNode' + pascal_case(model.root.name) + os.linesep
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
        + indent(2) + '; let (seed1, seed2) = seedFromArgs args in mapM_ print (executeFromSeeds seed1 seed2 10)' + os.linesep
        + indent(1) + '}' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'seedFromArgs :: [String] -> (Int, Int)' + os.linesep
        + indent(2) + 'seedFromArgs [] = (0, 0)' + os.linesep
        + indent(2) + 'seedFromArgs curArgs' + os.linesep
        + indent(3) + '| null (tail curArgs) = (read (head curArgs), 0)' + os.linesep
        + indent(3) + '| otherwise = (read (head curArgs), read (head (tail curArgs)))' + os.linesep
    )


def create_tree(model, name):
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
        if current_node.node_type == 'check' or current_node.node_type == 'check_environment' or current_node.node_type == 'action':
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


def handle_initial_value(statement, variable_name, var_type, indent_level, mode):
    if len(statement.case_results) == 0:
        if (not statement.default_result.range_mode) and len(statement.default_result.values) == 1:
            return (' = (' + format_code(statement.default_result.values[0], mode) + ', curGen)' + os.linesep)

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
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value, mode) + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        else:
            return ''

    default = statement.default_result
    return_string = ('' if len(statement.case_results) == 0 else os.linesep)
    where_string = ''
    unique_id = 0
    for case_result in statement.case_results:
        return_string += (
            indent(indent_level + 1) + '| ' + format_code(case_result.condition,  mode) + ' = '
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
                '(' + format_code(case_result.values[0], mode) + ', curGen)' + os.linesep
            )
            if (not case_result.range_mode) and (len(case_result.values) == 1)
            else
            (
                '(' + function_name + ' (fst (getRandomInt curGen ' + str(random_range) + ')), snd (getRandomInt curGen ' + str(random_range) + '))' + os.linesep
            )
        )
        where_string += create_random_func(function_name, case_result.values, case_result.range_mode, var_type, cond_func, random_range, indent_level)
    return_string += (
        (
            ' = '
        )
        if len(statement.case_results) == 0
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
            '(' + format_code(default.values[0], mode) + ', curGen)' + os.linesep
        )
        if (not default.range_mode) and (len(default.values) == 1)
        else
        (
            '(' + function_name + ' (fst (getRandomInt curGen ' + str(random_range) + ')), snd (getRandomInt curGen ' + str(random_range) + '))' + os.linesep
        )
    )
    where_string += create_random_func(function_name, default.values, default.range_mode, var_type, cond_func, random_range, indent_level)
    return return_string + ((post_script(indent_level) + where_string) if unique_id > 0 else '')


def handle_update_value(statement, variable_name, var_type, indent_level):
    if len(statement.case_results) == 0:
        if (not statement.default_result.range_mode) and len(statement.default_result.values) == 1:
            return (' = environment { env' + pascal_case(variable_name) + ' = ' + format_code(statement.default_result.values[0]) + '}' + os.linesep)

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
                        (indent(indent_level + 2) + function_name + ' ' + (str(index) if index < random_range else '_') + ' = ' + format_code(value) + os.linesep)
                        for index, value in enumerate(values)
                    ]
                )
            )
        else:
            return ''

    default = statement.default_result
    return_string = ('' if len(statement.case_results) == 0 else os.linesep)
    where_string = ''
    unique_id = 0
    for case_result in statement.case_results:
        return_string += (
            indent(indent_level + 1) + '| ' + format_code(case_result.condition) + ' = '
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
                'environment { env' + pascal_case(variable_name) + ' = ' + format_code(case_result.values[0]) + ' }' + os.linesep
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
        if len(statement.case_results) == 0
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
            'environment { env' + pascal_case(variable_name) + ' = ' + format_code(default.values[0]) + ' }' + os.linesep
        )
        if (not default.range_mode) and (len(default.values) == 1)
        else
        (
            'environment { sereneEnvGenerator = (snd (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')), env' + pascal_case(variable_name) + ' = ' + function_name + ' (fst (getRandomInt (sereneEnvGenerator environment) ' + str(random_range) + ')) }' + os.linesep
        )
    )
    where_string += create_random_func(function_name, default.values, default.range_mode, var_type, cond_func, random_range, indent_level)
    return return_string + ((post_script(indent_level) + where_string) if unique_id > 0 else '')


def create_macro(statement, indent_level):
    if len(statement.case_results) == 0:
        return ' = ' + format_code(statement.default_result.values[0]) + os.linesep
    return (
        os.linesep
        + ''.join(
            [
                (indent(indent_level + 1) + '| ' + format_code(case_result.condition) + ' = ' + format_code(case_result.values[0]) + os.linesep)
                for case_result in statement.case_results
            ]
        )
        + (indent(indent_level + 1) + '| otherwise = ' + format_code(statement.default_result.values[0]) + os.linesep)
    )


def variable_type(variable):
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
                                            (function_name + ' ' + str(number) + ' ' + board_type + ' ' + handle_constant(value) + ' = ' + board_type + ' { ' + field_name + str(number) + ' = ' + handle_constant(value) + ' }' + os.linesep)
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
                                    + indent(1) + '| ' + handle_constant(variable.domain.min_val) + ' > value || value > ' + handle_constant(variable.domain.max_val) + ' = error "local ' + variable.name + ' illegal value"' + os.linesep
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
                                    (function_name + ' ' + board_type + ' ' + handle_constant(value) + ' = ' + board_type + ' { ' + field_name + ' = ' + handle_constant(value) + ' }' + os.linesep)
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
                            + indent(1) + '| ' + handle_constant(variable.domain.min_val) + ' > value || value > ' + handle_constant(variable.domain.max_val) + ' = error "' + variable.name + ' illegal value"' + os.linesep
                            + indent(1) + '| otherwise = ' + board_type + ' { ' + field_name + ' = value }' + os.linesep
                        )
                    )
                )
            )
        )
        + os.linesep
    )


def create_environment(model):
    names_to_types = {
        variable.name : variable_type(variable)
        for variable in model.environment_variables if variable.model_as != 'DEFINE'
    }
    initial_values = {
        variable.name : handle_initial_value(variable.initial_value, variable.name, names_to_types[variable.name], 2, 'env')
        for index, variable in enumerate(model.environment_variables) if variable.model_as != 'DEFINE'
    }
    return (
        'module BehaviorTreeEnvironment where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + 'import BehaviorTreeBlackboard' + os.linesep
        + os.linesep
        + 'data BTreeEnvironment = BTreeEnvironment {' + os.linesep
        + indent(1) + 'sereneEnvGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(names_to_types) > 0 else '')
        + (os.linesep + indent(1) + ', ').join([('env' + pascal_case(variable_name) + ' :: ' + names_to_types[variable_name]) for variable_name in names_to_types])
        + (os.linesep if len(names_to_types) > 0 else '')
        # + indent(1) + '} deriving (Show)' + os.linesep + os.linesep
        + indent(1) + '}' + os.linesep + os.linesep
        + (
            'instance Show BTreeEnvironment where' + os.linesep
            + indent(1) + 'show (BTreeEnvironment _ '
            + ' '.join([('env' + pascal_case(variable_name)) for variable_name in names_to_types])
            + ') = '
            + '"Env = {"'
            + ' ++ '
            + ' ++ '.join(
                [
                    ('"env' + pascal_case(variable_name) + ': " ++ show env' + pascal_case(variable_name))
                    if index == 0
                    else
                    ('", env' + pascal_case(variable_name) + ': " ++ show env' + pascal_case(variable_name))
                    for index, variable_name in enumerate(names_to_types)
                ]
            )
            + (' ++ ' if len(names_to_types) > 0 else '')
            + '"}"' + os.linesep
        )
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'env' + pascal_case(variable.name) + ' :: BTreeBlackboard -> BTreeEnvironment -> ' + variable_type(variable) + os.linesep
                    + 'env' + pascal_case(variable.name) + ' blackboard environment' + create_macro(variable.initial_value, 0)
                )
                for variable in model.environment_variables if variable.model_as == 'DEFINE'
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
                       var.model_as != 'DEFINE'
                       ,
                       model.environment_variables
                       )
            )
        )
        + 'checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool' + os.linesep
        + 'checkTickConditionTermination blackboard environment = ' + (
            'True'
            if model.tick_condition is None
            else
            format_code(model.tick_condition)
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
                    indent(2) + 'tickUpdate' + pascal_case(update.variable.name) + ' :: BTreeEnvironment -> BTreeEnvironment' + os.linesep
                    + indent(2) + 'tickUpdate' + pascal_case(update.variable.name) + ' environment' + handle_update_value(update, update.variable.name, variable_type(update.variable), 2)
                    + os.linesep
                    + indent(2) + 'tempEnvironment' + str(index + 1) + ' = tickUpdate' + pascal_case(update.variable.name) + ' tempEnvironment' + str(index) + os.linesep
                    + os.linesep
                )
                for index, update in enumerate(model.update)
            ]
        ) + os.linesep
        + 'betweenTickUpdate environment = environment' + os.linesep  # TODO: obviously not done
        + os.linesep + os.linesep
        + 'initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment' + os.linesep
        + 'initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator ' + ' '.join(map(lambda x : 'newVal' + pascal_case(x), names_to_types)) + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(names_to_types)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + 'initVal' + pascal_case(variable_name) + ' :: StdGen -> (' + names_to_types[variable_name] + ', StdGen)' + os.linesep
                    + indent(2) + 'initVal' + pascal_case(variable_name) + ' curGen' + initial_values[variable_name]
                    + os.linesep
                    + indent(2) + '(newVal' + pascal_case(variable_name) + ', tempGen' + str(index + 1) + ') = initVal' + pascal_case(variable_name) + ' tempGen' + str(index) + os.linesep
                    + os.linesep
                )
                for index, variable_name in enumerate(names_to_types)
            ]
        ) + os.linesep
    )


def create_blackboard(model):
    names_to_types = {
        variable.name : variable_type(variable)
        for variable in model.blackboard_variables if variable.model_as != 'DEFINE'
    }
    initial_values = {
        variable.name : handle_initial_value(variable.initial_value, variable.name, names_to_types[variable.name], 2, 'board')
        for index, variable in enumerate(model.blackboard_variables) if variable.model_as != 'DEFINE'
    }

    def walk_tree_recursive(current_node, node_names, node_names_map, running_list, running_int):
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
                    pass
                else:
                    cur_type = variable_type(variable)
                    running_list.append(
                        {
                            'name' : variable.name,
                            'type' : cur_type,
                            'init' : handle_initial_value(variable.initial_value, variable.name, len(names_to_types) + my_int, cur_type, 2, 'board'),
                            'number' : my_int,
                            'variable' : variable
                        }
                    )
        elif current_node.node_type == 'check' or current_node.node_type == 'check_environment':
            # can't have local variables in checks.
            pass
        else:
            node_children = (current_node.children if hasattr(current_node, 'children') else [current_node.child])
            for child in node_children:
                (cur_node_names, cur_node_names_map, running_list, running_int) = walk_tree_recursive(child, cur_node_names, cur_node_names_map, running_list, running_int)
        return (
            (
                (
                    cur_node_names,
                    cur_node_names_map,
                    running_list,
                    running_int
                )
            )
        )

    (_, _, local_list, _) = walk_tree_recursive(model.root, set(), {}, [], -1)
    local_var_to_nodes = {}
    names_to_local_var = {}
    for local_v in local_list:
        name = local_v['name']
        if name in local_var_to_nodes:
            local_var_to_nodes[name].append(local_v['number'])
        else:
            names_to_local_var[name] = local_v['variable']
            local_var_to_nodes[name] = [local_v['number']]
    return (
        'module BehaviorTreeBlackboard where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + os.linesep
        + 'data BTreeBlackboard = BTreeBlackboard {' + os.linesep
        + indent(1) + 'sereneBoardGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(names_to_types) > 0 else '')
        + (os.linesep + indent(1) + ', ').join([('board' + pascal_case(variable_name) + ' :: ' + names_to_types[variable_name]) for variable_name in names_to_types])
        + (os.linesep if len(names_to_types) > 0 else '')
        + ((indent(1) + ', ') if len(local_list) > 0 else '')
        + (os.linesep + indent(1) + ', ').join([('localBoard' + pascal_case(local_v['name']) + str(local_v['number']) + ' :: ' + local_v['type']) for local_v in local_list])
        + (os.linesep if len(local_list) > 0 else '')
        + indent(1) + '}' + os.linesep + os.linesep
        + (
            'instance Show BTreeBlackboard where' + os.linesep
            + indent(1) + 'show (BTreeBlackboard _ '
            + ' '.join([('board' + pascal_case(variable_name)) for variable_name in names_to_types])
            + ' '
            + ' '.join([('localBoard' + pascal_case(local_v['name']) + str(local_v['number'])) for local_v in local_list])
            + ') = '
            + '"Board = {"'
            + ' ++ '
            + ' ++ '.join(
                [
                    ('"board' + pascal_case(variable_name) + ': " ++ show board' + pascal_case(variable_name))
                    if index == 0
                    else
                    ('", board' + pascal_case(variable_name) + ': " ++ show board' + pascal_case(variable_name))
                    for index, variable_name in enumerate(names_to_types)
                ]
            )
            + (' ++ ' if len(names_to_types) > 0 else '')
            + ' ++ '.join(
                [
                    ('"localBoard' + pascal_case(local_v['name']) + str(local_v['number']) + ': " ++ show localBoard' + pascal_case(local_v['name']) + str(local_v['number']))
                    if index == 0 and len(names_to_types) == 0
                    else
                    ('", localBoard' + pascal_case(local_v['name']) + str(local_v['number']) + ': " ++ show localBoard' + pascal_case(local_v['name']) + str(local_v['number']))
                    for index, local_v in enumerate(local_list)
                ]
            )
            + (' ++ ' if len(local_list) > 0 else '')
            + '"}"' + os.linesep
        )
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'localBoard' + pascal_case(var_name) + ' :: Int -> BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + ''.join(
                        [
                            ('localBoard' + pascal_case(var_name) + ' ' + str(number) + ' = localBoard' + pascal_case(var_name) + str(number) + os.linesep)
                            for number in local_var_to_nodes[var_name]
                        ]
                    )
                    + 'localBoard' + pascal_case(var_name) + ' _ = error "' + var_name + ' illegal local reference"' + os.linesep
                )
                for var_name in local_var_to_nodes if ((variable := names_to_local_var[var_name]) or True)
            ]
        )
        + os.linesep + os.linesep
        + ''.join(
            [
                (
                    'board' + pascal_case(variable.name) + ' :: BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + 'board' + pascal_case(variable.name) + ' blackboard' + create_macro(variable.initial_value, 0)
                )
                for variable in model.blackboard_variables if variable.model_as == 'DEFINE'
            ]
        )
        + ''.join(
            [
                (
                    'localBoard' + pascal_case(variable.name) + ' :: Int -> BTreeBlackboard -> ' + variable_type(variable) + os.linesep
                    + 'localBoard' + pascal_case(variable.name) + ' nodeLocation blackboard' + create_macro(variable.initial_value, 0)
                )
                for variable in model.local_variables if variable.model_as == 'DEFINE'
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
                       var.model_as != 'DEFINE'
                       ,
                       model.blackboard_variables
                       )
            )
        )
        + ''.join(
            map(
                lambda var_name :
                safe_update(names_to_local_var[var_name], False, True, local_var_to_nodes[var_name])
                ,
                local_var_to_nodes
            )
        )
        + os.linesep + os.linesep
        + 'initialBlackboard :: Int -> BTreeBlackboard' + os.linesep
        + 'initialBlackboard seed = BTreeBlackboard newSereneGenerator ' + ' '.join(map(lambda x : 'newVal' + pascal_case(x), names_to_types))
        + ' '
        + ' '.join(map(lambda x : 'localNewVal' + pascal_case(x['name']) + str(x['number']), local_list)) + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(names_to_types) + len(local_list)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + 'initVal' + pascal_case(variable_name) + ' :: StdGen -> (' + names_to_types[variable_name] + ', StdGen)' + os.linesep
                    + indent(2) + 'initVal' + pascal_case(variable_name) + ' curGen' + initial_values[variable_name]
                    + os.linesep
                    + indent(2) + '(newVal' + pascal_case(variable_name) + ', tempGen' + str(index + 1) + ') = initVal' + pascal_case(variable_name) + ' tempGen' + str(index) + os.linesep
                    + os.linesep
                )
                for index, variable_name in enumerate(names_to_types)
            ]
        )
        + ''.join(
            [
                (
                    indent(2) + 'localInitVal' + pascal_case(local_v['name']) + str(local_v['number']) + ' :: StdGen -> (' + local_v['type'] + ', StdGen)' + os.linesep
                    + indent(2) + 'localInitVal' + pascal_case(local_v['name']) + str(local_v['number']) + ' curGen' + local_v['init']
                    + indent(2) + '(localNewVal' + pascal_case(local_v['name']) + str(local_v['number']) + ', tempGen' + str(index + 1 + len(names_to_types)) + ') = localInitVal' + pascal_case(local_v['name']) + str(local_v['number']) + ' tempGen' + str(index + len(names_to_types)) + os.linesep
                )
                for index, local_v in enumerate(local_list)
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
    'xor' : ('operator.xor', format_function_between),
    'xnor' : ('xnor', format_function_between),
    'implies' : ('->', format_function_between),
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
    'division' : ('/', format_function_between),
    'mod' : ('%', format_function_between),
    'count' : ('count', format_function_before)
}


STANDARD_IMPORTS = ('import BehaviorTreeCore' + os.linesep
                    + 'import BehaviorTreeBlackboard' + os.linesep
                    + 'import BehaviorTreeEnvironment' + os.linesep
                    + 'import SereneRandomizer' + os.linesep
                    + os.linesep)


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('output_file')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }

    my_location = args.location + 'app/'

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/haskell_file/BehaviorTreeCore.hs', my_location + 'BehaviorTreeCore.hs')

    with open(my_location + 'SereneRandomizer.hs', 'w') as f:
        f.write(create_randomizer())

    with open(my_location + 'BehaviorTreeEnvironment.hs', 'w') as f:
        f.write(create_environment(model))

    with open(my_location + 'BehaviorTreeBlackboard.hs', 'w') as f:
        f.write(create_blackboard(model))

    with open(my_location + pascal_case(args.output_file) + '.hs', 'w') as f:
        f.write(create_tree(model, args.output_file))

    with open(my_location + 'Main.hs', 'w') as f:
        f.write(create_runner(model, args.output_file))

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
