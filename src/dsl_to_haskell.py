import textx
import argparse
import os
# import sys
import shutil
import itertools
from behaverify_common import haskell_indent as indent, create_node_name
import serene_functions


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
    'or' : ('||', format_function_before),
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


def format_variable(variable, is_local, is_env, global_init = False):
    return (
        ('(' + variable.name + ' blackboard)')  # todo: fix this. it's obviously not finished.
        if is_local
        else
        (
            ('(env' + variable.name.capitalize() + ' environment)')
            if is_env
            else
            ('(board' + variable.name.capitalize() + ' blackboard)')
        )
    )
    # return (
    #     (
    #         ('blackboard_reader.')
    #         if global_init else
    #         ('self.' + ('' if is_local else 'blackboard.'))
    #     )
    #     + variable.name
    #     + ('()' if variable.model_as == 'DEFINE' else '')
    # )


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
    # variable_name = (format_variable(statement.variable, statement.mode == 'local', global_init) if override_variable_name is None else override_variable_name)
    variable_name = statement.variable.name
    update_env_board = (
        'updateEnv'
        if statement.mode == 'env'
        else
        (
            'updateBoard'
        )
    )  # TODO: update this to handle local variables too
    env_board = (
        ' environment '
        if statement.mode == 'env'
        else
        (
            ' blackboard '
        )
    )  # TODO: update this to handle local variables too
    if len(statement.case_results) == 0:
        return (
            ' = '
            + ('(blackboard, ' if statement.mode == 'env' else '(')
            + update_env_board + variable_name.capitalize() + env_board + variable_assignment(statement.default_result.values, statement.default_result.range_mode, global_init)
            + (')' if statement.mode == 'env' else ', environment)')
            + os.linesep
        )
    return (
        os.linesep
        + ''.join(
            [
                (
                    indent(indent_level) + '| ' + format_code(case_result.condition, global_init)
                    + ' = '
                    + ('(blackboard, ' if statement.mode == 'env' else '(')
                    + update_env_board + variable_name.capitalize() + env_board + variable_assignment(statement.default_result.values, statement.default_result.range_mode, global_init)
                    + (')' if statement.mode == 'env' else ', environment)')
                    + os.linesep
                )
                for case_result in statement.case_results
            ]
        )
        + (
            indent(indent_level) + '| otherwise = '
            + ('(blackboard, ' if statement.mode == 'env' else '(')
            + update_env_board + variable_name.capitalize() + env_board + variable_assignment(statement.default_result.values, statement.default_result.range_mode, global_init)
            + (')' if statement.mode == 'env' else ', environment)')
            + os.linesep
        )
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
    if statement.condition_variable is None:
        condition_code = format_code(statement.condition)
        return (
            [
                (
                    '| ' + condition_code + ' = newEnvironment' + os.linesep
                    + '| otherwise = environment' + os.linesep
                    + handle_variable_statement(variable_statement)
                )
                for variable_statement in statement.variable_statements
            ],
            []
        )
    else:
        pass
    # return (indent(2) + 'temp_vals = ' +
    #         (
    #             ((statement.import_from + '.') if statement.import_from is not None else '') + statement.python_function
    #             + '('
    #             + ', '.join(sorted(list(set(
    #                 find_local_variables(statement.condition)
    #                 + flatten(
    #                     [
    #                         flatten(
    #                             [
    #                                 (find_local_variables(case_result.condition)
    #                                  + ([] if case_result.range_mode else flatten([find_local_variables(value) for value in case_result.values]))
    #                                  )
    #                                 for case_result in variable_statement.case_results
    #                             ]
    #                         )
    #                         + (
    #                                 [] if variable_statement.default_result.range_mode else flatten([find_local_variables(value) for value in variable_statement.default_result.values])
    #                         )
    #                         for variable_statement in statement.variable_statements
    #                     ]
    #                 )
    #             ))))
    #             + ')'
    #             + os.linesep
    #         )
    #         + indent(2) + 'if temp_vals[0]:' + os.linesep
    #         + indent(3) + '('
    #         + ', '.join(
    #             (['_'] if statement.condition_variable is None else [format_variable(statement.condition_variable, True)])
    #             +
    #             [format_variable(var_statement.variable, var_statement.mode == 'local') for var_statement in statement.variable_statements])
    #         + ') = temp_vals' + os.linesep
    #         + (
    #             (indent(2) + 'else:' + os.linesep
    #              + indent(3) + format_variable(statement.condition_variable, True) + ' = False' + os.linesep)
    #             if statement.condition_variable is not None else '')
    #         )


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
        + indent(indent_level + 2) + 'blackboard = fst boardEnv' + os.linesep
        + indent(indent_level + 2) + 'environment = snd boardEnv' + os.linesep
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
    return ('module ' + node_name.capitalize() + '_file where' + os.linesep)


def check_function(node):
    return (
        node.name + ' :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
        + node.name + ' nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges' + os.linesep
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
            indent(indent_level) + 'envUpdate' + str(index) + ' :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
            + indent(indent_level) + 'envUpdate' + str(index) + ' boardEnv'  # no os.linesep here. we handle that in the variable statement.
        )

    def code_decl(index, indent_level):
        return (
            indent(indent_level) + 'futureChanges' + str(index) + ' :: BTreeBlackboard -> BTreeEnvironment -> (BTreeBlackboard, BTreeEnvironment)' + os.linesep
            + indent(indent_level) + 'futureChanges' + str(index) + ' boardEnv'  # no os.linesep here. we handle that in the variable statement.
        )

    def post_script(indent_level):
        return (
            indent(indent_level + 1) + 'where' + os.linesep
            + indent(indent_level + 2) + 'blackboard = fst boardEnv' + os.linesep
            + indent(indent_level + 2) + 'environment = snd boardEnv' + os.linesep
        )

    return (
        node.name + ' :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput' + os.linesep
        + node.name + ' nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)' + os.linesep
        + indent(1) + 'where' + os.linesep
        + ('').join(
            [
                (env_decl(index, 2) + value + post_script(2))
                for index, value in enumerate(pre_updates)
            ]
        )
        + handle_return_statement(node.return_statement)
        + ('').join(
            [
                (env_decl(index + pre, 2) + value + post_script(2))
                for index, value in enumerate(post_updates)
            ]
        )
        + ('').join(
            [
                (code_decl(index, 2) + value + post_script(3))
                for index, value in enumerate(delay_updates)
            ]
        )
        + indent(2) + 'preStatusBoardEnv = ' + ' . '.join(map(lambda x : 'envUpdate' + x, map(str, reversed(range(pre))))) + (' $ ' if pre > 1 else ' ') + '(blackboard, environment)' + os.linesep
        + indent(2) + 'returnStatus = returnStatement preStatusBoardEnv' + os.linesep
        + indent(2) + 'postStatusBoardEnv = ' + ' . '.join(map(lambda x : 'envUpdate' + x, map(str, reversed(range(pre, pre + post))))) + (' $ ' if post > 1 else ' ') + 'preStatusBoardEnv' + os.linesep
        + indent(2) + 'newBlackboard = fst postStatusBoardEnv' + os.linesep
        + indent(2) + 'newEnvironment = snd postStatusBoardEnv' + os.linesep
        + indent(2) + 'newFutureChanges = futureChanges' + (' : ' if delay > 0 else '') + ' : '.join(map(lambda x : 'futureChanges' + x, map(str, range(delay)))) + os.linesep
    )


STANDARD_IMPORTS = ('import Behavior_tree_core' + os.linesep
                    + 'import Behavior_tree_blackboard' + os.linesep
                    + 'import Behavior_tree_environment' + os.linesep)


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
        + 'import ' + name.capitalize() + os.linesep
        + 'import Behavior_tree_core' + os.linesep
        + 'import Behavior_tree_environment' + os.linesep
        + 'import Behavior_tree_blackboard' + os.linesep
        + ''.join([('import ' + node.name.capitalize() + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
        + os.linesep + os.linesep
        + 'main :: IO ()' + os.linesep
        + 'main =' + os.linesep
        + indent(1) + 'do {' + os.linesep
        + indent(2) + 'print eachBoardEnv' + os.linesep
        + indent(1) + '}' + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'maxIteration = 100' + os.linesep
        + indent(2) + 'initBoard = initialBlackboard 0' + os.linesep
        + indent(2) + 'initEnv = initialEnvironment 0 initBoard' + os.linesep
        + indent(2) + 'treeRoot = ' + model.root.name + '__node' + os.linesep
        + indent(2) + 'executionChain :: Int -> MemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]' + os.linesep
        + indent(2) + 'executionChain count memory partial blackboard environment' + os.linesep
        + indent(3) + '| count >= maxIteration = [(blackboard, environment)]' + os.linesep
        + indent(3) + '| not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]' + os.linesep
        + indent(3) + '| otherwise = (blackboard, environment) : (executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv)' + os.linesep
        + indent(3) + 'where' + os.linesep
        + indent(4) + '(_, nextMemory, nextPartial, nextBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment' + os.linesep
        + indent(4) + 'nextEnv = betweenTickUpdate (applyFutureChanges tempEnv futureChanges)' + os.linesep
        + indent(2) + 'eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv'
    )


def create_tree(model, name):
    def node_function(node):
        if node.node_type == 'selector' or node.node_type == 'sequence':
            return node.node_type + ('Partial' if node.memory else '') + 'Func'
        elif node.node_type == 'parallel':
            return (
                '('
                + 'parallel'
                + ('Partial' if node.memory else '')
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
        print('NOT DONE NODE')
        return 'NOT DONE'

    def walk_tree_recursive(current_node, node_names, node_names_map, running_string, running_int, indent_level):
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
        if current_node.node_type == 'check' or current_node.node_type == 'check_environment' or current_node.node_type == 'action':
            running_string = running_string + (
                indent(indent_level) + node_name + ' = BTreeNode ' + current_node.name.replace(' ', '') + ' [] ' + str(my_int) + os.linesep
            )
        else:
            child_names = []
            for child in current_node.children:
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
        'module ' + name.capitalize() + ' where' + os.linesep
        + 'import Behavior_tree_core' + os.linesep
        + ''.join([('import ' + node.name.capitalize() + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes, model.environment_checks)])
        + node_declarations
    )


def handle_initial_value(initial_value, indent_level):
    # todo: actuall finish this. currently handling default case only.
    if len(initial_value.case_results) == 0:
        if (not initial_value.default_result.range_mode) and len(initial_value.default_result.values) == 1:
            return (' = (' + format_code(initial_value.default_result.values[0]) + ', curGen)' + os.linesep)
    default = initial_value.default_result
    return (
        os.linesep
        + ''.join(
            [
                (
                    ''.join(
                        [
                            (indent(indent_level + 1) + '| REPLACE_CONDITION && (fst (getRandomInt curGen REPLACE_RANGE) == ' + str(index) + ') = (' + str(value) + ', snd (getRandomInt curGen))' + os.linesep)
                            for index, value in enumerate(filter(cond_func, range(handle_constant(case_result.values[0]), handle_constant(case_result.values[1]) + 1)))
                        ]
                    ).replace('REPLACE_CONDITION',
                              format_code(case_result.condition)).replace('REPLACE_RANGE',
                                                                          str(len(filter(cond_func,
                                                                                         range(handle_constant(case_result.values[0]),
                                                                                               handle_constant(case_result.values[1]) + 1)
                                                                                         )
                                                                                  ) - 1
                                                                              )
                                                                          )
                    if case_result.range_mode and ((cond_func := build_range_func(case_result.values[2])) or True)
                    else
                    (
                        ''.join(
                            [
                                (indent(indent_level + 1) + '| REPLACE_CONDITION && (fst (getRandomInt curGen ' + str(len(case_result.values) - 1) + ') == ' + str(index) + ') = (' + format_code(value) + ', snd (getRandomInt curGen))' + os.linesep)
                                for index, value in case_result.values
                            ]
                        ).replace('REPLACE_CONDITION', format_code(case_result.condition))
                        if len(case_result.values) > 1
                        else
                        (indent(indent_level + 1) + '| ' + format_code(case_result.condition) + ' = (' + format_code(case_result.values[0]) + ', curGen)' + os.linesep)
                    )
                )
                for case_result in initial_value.case_results
            ]
        )
        + (
            ''.join(
                [
                    (indent(indent_level + 1) + '| fst (getRandomInt curGen REPLACE_RANGE) == ' + str(index) + ' = (' + str(value) + ', snd (getRandomInt curGen))' + os.linesep)
                    for index, value in enumerate(filter(cond_func, range(handle_constant(default.values[0]), handle_constant(default.values[1]) + 1)))
                ]
            ).replace('fst (getRandomInt curGen REPLACE_RANGE == '
                      + str(len(filter(cond_func,
                                       range(handle_constant(default.values[0]),
                                             handle_constant(default.values[1]) + 1)
                                       )
                                ) - 1
                            ),
                      'otherwise'
                      ).replace('REPLACE_RANGE',
                                str(len(filter(cond_func,
                                               range(handle_constant(default.values[0]),
                                                     handle_constant(default.values[1]) + 1)
                                               )
                                        ) - 1
                                    )
                                )
            if default.range_mode and ((cond_func := build_range_func(default.values[2])) or True)
            else
            (
                ''.join(
                    [
                        (indent(indent_level + 1) + '| fst (getRandomInt curGen ' + str(len(default.values) - 1) + ') == ' + str(index) + ' = (' + format_code(value) + ', snd (getRandomInt curGen))' + os.linesep)
                        for index, value in default.values
                    ]
                ).replace('fst (getRandomInt curGen ' + str(len(default.values) - 1) + ') == ' + str(len(default.values) - 1), 'otherwise')
                if len(default.values) > 1
                else
                (indent(indent_level + 1) + '| otherwise = (' + format_code(default.values[0]) + ', curGen)' + os.linesep)
            )
        )
    )


def create_environment(model):
    variables = {
        variable.name : ('Bool' if variable.domain.boolean is not None else ('ENUM' if variable.domain.min_val is None else 'Int'))
        for variable in model.environment_variables if variable.model_as != 'DEFINE'
    }
    initial_values = {
        variable.name : handle_initial_value(variable.initial_value, 2)
        for variable in model.environment_variables if variable.model_as != 'DEFINE'
    }
    return (
        'module Behavior_tree_environment where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + 'import Behavior_tree_blackboard' + os.linesep
        + os.linesep
        + 'data BTreeEnvironment = BTreeEnvironment {' + os.linesep
        + indent(1) + 'sereneGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(variables) > 0 else '')
        + (os.linesep + indent(1) + ', ').join(['board' + variable.capitalize() + ' :: ' + variables[variable] for variable in variables])
        + (os.linesep if len(variables) > 0 else '')
        + indent(1) + '} deriving (Show)' + os.linesep + os.linesep
        + ''.join(
            [
                ('updateEnv' + variable.name.capitalize() + ' :: BTreeEnvironment -> '
                 + ('Bool' if variable.domain.boolean is not None else ('ENUM' if variable.domain.min_val is None else 'Int'))
                 + ' -> BTreeEnvironment' + os.linesep
                 + 'updateEnv' + variable.name.capitalize() + ' environment value'
                 + (
                     (' = environment' + os.linesep)
                     if variable.model_as == 'FROZENVAR'
                     else
                     (
                         # todo: add nondeterminism here.
                         (' = environment { env' + variable.name.capitalize() + ' : value }' + os.linesep)
                         if variable.domain.boolean is not None or variable.domain.min_val is None
                         else
                         (
                             os.linesep
                             + indent(1) + '| ' + str(variable.domain.min_val) + ' > value || value > ' + str(variable.domain.max_val) + ' = error "' + variable.name + ' illegal value"' + os.linesep
                             + indent(1) + '| otherwise = environment { env' + variable.name.capitalize() + ' = value }' + os.linesep
                         )
                     )
                 )
                 + os.linesep
                 )
                for variable in model.environment_variables if variable.model_as != 'DEFINE'
            ]
        )
        + 'checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool' + os.linesep
        + 'checkTickConditionTermination blackboard environment = ' + (
            'True'
            if model.tick_condition is None
            else
            format_code(model.tick_condition)
        ) + os.linesep + os.linesep
        + 'applyFutureChanges :: BTreeEnvironment -> [BTreeEnvironment -> BTreeEnvironment] -> BTreeEnvironment' + os.linesep
        + 'applyFutureChanges environment futureChanges' + os.linesep
        + indent(1) + '| null futureChanges = environment' + os.linesep
        + indent(1) + '| otherwise = applyFutureChanges (head futureChanges environment) (tail futureChanges)' + os.linesep
        + os.linesep + os.linesep
        + 'betweenTickUpdate :: BTreeEnvironment -> BTreeEnvironment' + os.linesep
        + 'betweenTickUpdate environment = environment' + os.linesep  # TODO: obviously not done
        + os.linesep + os.linesep
        + 'initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment' + os.linesep
        + 'initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator ' + ' '.join(map(lambda x : 'newVal' + str(x).capitalize(), variables)) + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(variables)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + 'initVal' + variable.capitalize() + ' :: StdGen -> (' + variables[variable] + ', StdGen)' + os.linesep
                    + indent(2) + 'initVal' + variable.capitalize() + ' curGen' + initial_values[variable]
                    + indent(2) + '(newVal' + variable.capitalize() + ', tempGen' + str(index + 1) + ') = initVal' + variable.capitalize() + ' tempGen' + str(index) + os.linesep
                )
                for index, variable in enumerate(variables)
            ]
        ) + os.linesep
    )


def create_blackboard(model):
    variables = {
        variable.name : ('Bool' if variable.domain.boolean is not None else ('ENUM' if variable.domain.min_val is None else 'Int'))
        for variable in model.blackboard_variables if variable.model_as != 'DEFINE'
    }
    initial_values = {
        variable.name : handle_initial_value(variable.initial_value, 2)
        for variable in model.blackboard_variables if variable.model_as != 'DEFINE'
    }
    return (
        'module Behavior_tree_blackboard where' + os.linesep
        + 'import SereneRandomizer' + os.linesep
        + 'import System.Random' + os.linesep
        + os.linesep
        + 'data BTreeBlackboard = BTreeBlackboard {' + os.linesep
        + indent(1) + 'sereneGenerator :: StdGen' + os.linesep
        + ((indent(1) + ', ') if len(variables) > 0 else '')
        + (os.linesep + indent(1) + ', ').join(['board' + variable.capitalize() + ' :: ' + variables[variable] for variable in variables])
        + (os.linesep if len(variables) > 0 else '')
        + indent(1) + '} deriving (Show)' + os.linesep + os.linesep
        + ''.join(
            [
                ('updateBoard' + variable.name.capitalize() + ' :: BTreeBlackboard -> '
                 + ('Bool' if variable.domain.boolean is not None else ('ENUM' if variable.domain.min_val is None else 'Int'))
                 + ' -> BTreeBlackboard' + os.linesep
                 + 'updateBoard' + variable.name.capitalize() + ' blackboard value'
                 + (
                     (' = blackboard' + os.linesep)
                     if variable.model_as == 'FROZENVAR'
                     else
                     (
                         # todo: add nondeterminism here.
                         (' = blackboard { board' + variable.name.capitalize() + ' : value }' + os.linesep)
                         if variable.domain.boolean is not None or variable.domain.min_val is None
                         else
                         (
                             os.linesep
                             + indent(1) + '| ' + str(variable.domain.min_val) + ' > value || value > ' + str(variable.domain.max_val) + ' = error "' + variable.name + ' illegal value"' + os.linesep
                             + indent(1) + '| otherwise = blackboard { board' + variable.name.capitalize() + ' = value }' + os.linesep
                         )
                     )
                 )
                 + os.linesep
                 )
                for variable in model.blackboard_variables if variable.model_as != 'DEFINE'
            ]
        )
        + os.linesep + os.linesep
        + 'initialBlackboard :: Int -> BTreeBlackboard' + os.linesep
        + 'initialBlackboard seed = BTreeBlackboard newSereneGenerator ' + ' '.join(map(lambda x : 'newVal' + str(x).capitalize(), variables)) + os.linesep
        + indent(1) + 'where' + os.linesep
        + indent(2) + 'tempGen0 = getGenerator seed' + os.linesep
        + indent(2) + 'newSereneGenerator = tempGen' + str(len(variables)) + os.linesep
        + ''.join(
            [
                (
                    indent(2) + 'initVal' + variable.capitalize() + ' :: StdGen -> (' + variables[variable] + ', StdGen)' + os.linesep
                    + indent(2) + 'initVal' + variable.capitalize() + ' curGen' + initial_values[variable]
                    + indent(2) + '(newVal' + variable.capitalize() + ', tempGen' + str(index + 1) + ') = initVal' + variable.capitalize() + ' tempGen' + str(index) + os.linesep
                )
                for index, variable in enumerate(variables)
            ]
        ) + os.linesep
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

    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/haskell_file/Behavior_tree_core.hs', my_location + 'Behavior_tree_core.hs')

    with open(my_location + 'SereneRandomizer.hs', 'w') as f:
        f.write(create_randomizer())

    with open(my_location + 'Behavior_tree_environment.hs', 'w') as f:
        f.write(create_environment(model))

    with open(my_location + 'Behavior_tree_blackboard.hs', 'w') as f:
        f.write(create_blackboard(model))

    with open(my_location + args.output_file.capitalize() + '.hs', 'w') as f:
        f.write(create_tree(model, args.output_file))

    with open(my_location + 'Main.hs', 'w') as f:
        f.write(create_runner(model, args.output_file))

    for action in model.action_nodes:
        with open(my_location + action.name.capitalize() + '_file.hs', 'w') as f:
            f.write(build_action_node(action))
    for check in model.check_nodes:
        with open(my_location + check.name.capitalize() + '_file.hs', 'w') as f:
            f.write(build_check_node(check))
    for check_env in model.environment_checks:
        # print(check_env)
        with open(my_location + check_env.name.capitalize() + '_file.hs', 'w') as f:
            f.write(build_check_environment_node(check_env))

    return


if __name__ == '__main__':
    main()
