import os
import sys


def indent(n):
    return ' '*(4*n)


def create_constants():
    return ('constants { } end_constants' + os.linesep)


def create_blackboard_variables():
    return ('blackboard_variables {blackboard_variable { biggest_fish VAR [0, 199] initial_value { result {0} end_result} end_initial_value} end_blackboard_variable} end_blackboard_variables' + os.linesep)


def create_local_variables():
    return ('local_variables {#comment# Local Variable declarations go here #end_comment#} end_local_variables' + os.linesep)


def create_environment():
    return (
        'environment {environment_variables {#comment# Local Variable declarations go here #end_comment#} end_environment_variables update_values { #comment# update values for environment #end_comment#} end_update_values} end_environment' + os.linesep
    )


def create_check(x):
    return (
        indent(1) + 'check {' + os.linesep
        + indent(2) + 'biggest_fish_is' + str(x) + os.linesep
        + indent(2) + 'read_variables { biggest_fish } end_read_variables' + os.linesep
        + indent(2) + 'condition { (equal, bl biggest_fish, ' + str(x) + ') } end_condition' + os.linesep
        + indent(1) + '} end_check' + os.linesep
    )


def create_checks(x):
    return (
        'checks {' + os.linesep
        + ''.join(map(create_check, range(x+1)))
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {#comment# check environment nodes are defined here #end_comment#} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'bigger_fish' + os.linesep
        + indent(2) + 'imports {} end_imports' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { biggest_fish } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { bl biggest_fish result { (min, (addition, 1, bl biggest_fish), 199) } end_result } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { result { success } end_result } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + '} end_actions' + os.linesep
    )


def create_decorator_failure_is_running(indent_level, x):
    return (
        indent(indent_level) + 'decorator {' + os.linesep
        + indent(indent_level + 1) + 'decorator' + str(x) + os.linesep
        + indent(indent_level + 1) + 'X_is_Y X failure Y running' + os.linesep
        + indent(indent_level + 1) + 'child biggest_fish_is' + str(x) + os.linesep
        + indent(indent_level) + '} end_decorator' + os.linesep
    )


def create_subtree_parallel(indent_level, x):
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + 'parallel' + str(x) + os.linesep
        + indent(indent_level + 1) + 'parallel policy success_on_one' + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + ''.join(
            [
                (create_decorator_failure_is_running(indent_level + 2, y))
                for y in range(max(0, x-3), x+1)
            ]
        )
        + (
            (create_decorator_failure_is_running(indent_level + 2, 0)
             if x == 4 else
             (
                 ('')
                 if x < 4 else
                 (create_subtree_parallel(indent_level + 2, x-4))
             )
             )
        )
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_tree_parallel(x):
    return (
        'sub_trees {#comment# subtrees go here. #end_comment#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + 'composite {' + os.linesep
        + indent(1) + 'biggest_fish_sequence' + os.linesep
        + indent(1) + 'sequence' + os.linesep
        + indent(1) + 'children {' + os.linesep
        + indent(2) + 'decorator {' + os.linesep
        + indent(3) + 'special_decorator' + os.linesep
        + indent(3) + 'X_is_Y X running Y failure' + os.linesep
        + indent(3) + 'child' + os.linesep
        + create_subtree_parallel(3, x)
        + indent(2) + '} end_decorator' + os.linesep
        + indent(2) + 'bigger_fish' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_decorator_inverter(indent_level, x):
    return (
        indent(indent_level) + 'decorator {' + os.linesep
        + indent(indent_level + 1) + 'decorator' + str(x) + os.linesep
        + indent(indent_level + 1) + 'inverter' + os.linesep
        + indent(indent_level + 1) + 'child biggest_fish_is' + str(x) + os.linesep
        + indent(indent_level) + '} end_decorator' + os.linesep
    )


def create_subtree_sequence(indent_level, x):
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + 'sequence' + str(x) + os.linesep
        + indent(indent_level + 1) + 'sequence' + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + ''.join(
            [
                (create_decorator_inverter(indent_level + 2, y))
                for y in range(max(0, x-3), x+1)
            ]
        )
        + (
            (create_decorator_inverter(indent_level + 2, 0)
             if x == 4 else
             (
                 ('')
                 if x < 4 else
                 (create_subtree_sequence(indent_level + 2, x-4))
             )
             )
        )
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_tree_sequence(x):
    return (
        'sub_trees {#comment# subtrees go here. #end_comment#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + 'composite {' + os.linesep
        + indent(1) + 'biggest_fish_sequence' + os.linesep
        + indent(1) + 'sequence' + os.linesep
        + indent(1) + 'children {' + os.linesep
        + indent(2) + 'decorator {' + os.linesep
        + indent(3) + 'special_decorator' + os.linesep
        + indent(3) + 'inverter' + os.linesep
        + indent(3) + 'child' + os.linesep
        + create_subtree_sequence(3, x)
        + indent(2) + '} end_decorator' + os.linesep
        + indent(2) + 'bigger_fish' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_specifications(x):
    return (
        'specifications {' + os.linesep
        # + indent(1) + 'LTLSPEC { (finally, (globally, (not, (success, biggest_fish_sequence)))) } end_LTLSPEC' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (globally, (equal, bl biggest_fish 0, ' + str(x + 1) + '))) } end_LTLSPEC' + os.linesep
        # + indent(1) + 'CTLSPEC { (always_finally, (always_globally, (not, (success, biggest_fish_sequence)))) } end_CTLSPEC' + os.linesep
        + indent(1) + 'CTLSPEC { (always_finally, (always_globally, (equal, bl biggest_fish 0, ' + str(x + 1) + '))) } end_CTLSPEC' + os.linesep
        + '} end_specifications'
    )


def create_fish_parallel(x):
    return (
        create_constants()
        + create_blackboard_variables()
        + create_local_variables()
        + create_environment()
        + create_checks(x)
        + create_environment_checks()
        + create_actions()
        + create_tree_parallel(x)
        + create_specifications(x)
        )


def create_fish_sequence(x):
    return (
        create_constants()
        + create_blackboard_variables()
        + create_local_variables()
        + create_environment()
        + create_checks(x)
        + create_environment_checks()
        + create_actions()
        + create_tree_sequence(x)
        + create_specifications(x)
        )


def write_files(location):
    for x in range(9, 200, 10):
        with open(location + 'bigger_fish_parallel_' + str(x) + '.tree', 'w') as f:
            f.write(create_fish_parallel(x))
        with open(location + 'bigger_fish_sequence_' + str(x) + '.tree', 'w') as f:
            f.write(create_fish_sequence(x))


write_files(sys.argv[1])
