import os
import sys


def indent(n):
    return ' '*(4*n)

FISH_CAP = '2001'
def create_constants():
    return (
        'configuration {}' + os.linesep
        + 'enumerations {}' + os.linesep
        + 'constants { fish_cap := ' + FISH_CAP + ' } end_constants' + os.linesep
    )


def create_variables():
    return ('variables {variable { bl biggest_fish VAR [0, fish_cap] assign { result {0} end_result} }}' + os.linesep)


def create_environment():
    return (
        'environment_update {} ' + os.linesep
    )


#def create_check(x):
def create_check():
    return (
        indent(1) + 'check {' + os.linesep
        #+ indent(2) + 'biggest_fish_is' + str(x) + os.linesep
        + indent(2) + 'biggest_fish_is_X' + os.linesep
        + indent(2) + 'arguments{x := INT}' + os.linesep
        + indent(2) + 'read_variables { biggest_fish } end_read_variables' + os.linesep
        #+ indent(2) + 'condition { (equal, biggest_fish, ' + str(x) + ') } end_condition' + os.linesep
        + indent(2) + 'condition { (eq, biggest_fish, x) } end_condition' + os.linesep
        + indent(1) + '} end_check' + os.linesep
    )


#def create_checks(x):
def create_checks():
    return (
        'checks {' + os.linesep
        #+ ''.join(map(create_check, range(x+1)))
        + create_check()
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {#{ check environment nodes are defined here }#} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'bigger_fish' + os.linesep
        + indent(2) + 'arguments {}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { biggest_fish } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { biggest_fish assign {result { (min, (add, 1, biggest_fish), fish_cap) } } } end_variable_statement' + os.linesep
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
        #+ indent(indent_level + 1) + 'child { biggest_fish_is' + str(x) + '}' + os.linesep
        + indent(indent_level + 1) + 'child { biggest_fish_is_' + str(x) + ' : biggest_fish_is_X {' + str(x) + '}}' + os.linesep
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
            create_decorator_failure_is_running(indent_level + 2, 0)
            if x == 4 else
            (
                ('')
                if x < 4 else
                (create_subtree_parallel(indent_level + 2, x - 4))
            )
        )
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_tree_parallel(x):
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + 'composite {' + os.linesep
        + indent(1) + 'biggest_fish_sequence' + os.linesep
        + indent(1) + 'sequence' + os.linesep
        + indent(1) + 'children {' + os.linesep
        + indent(2) + 'decorator {' + os.linesep
        + indent(3) + 'special_decorator' + os.linesep
        + indent(3) + 'X_is_Y X running Y failure' + os.linesep
        + indent(3) + 'child {' + os.linesep
        + create_subtree_parallel(3, x)
        + indent(2) + '}} end_decorator' + os.linesep
        + indent(2) + 'bigger_fish {}' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_decorator_inverter(indent_level, x):
    return (
        indent(indent_level) + 'decorator {' + os.linesep
        + indent(indent_level + 1) + 'decorator' + str(x) + os.linesep
        + indent(indent_level + 1) + 'inverter' + os.linesep
        #+ indent(indent_level + 1) + 'child { biggest_fish_is' + str(x) + '}' + os.linesep
        + indent(indent_level + 1) + 'child { biggest_fish_is_' + str(x) + ' : biggest_fish_is_X {' + str(x) + '}}' + os.linesep
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
            create_decorator_inverter(indent_level + 2, 0)
            if x == 4 else
            (
                ('')
                if x < 4 else
                (create_subtree_sequence(indent_level + 2, x - 4))
            )
        )
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_subtree_selector(indent_level, x):
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + 'selector' + str(x) + os.linesep
        + indent(indent_level + 1) + 'selector' + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + ''.join(
            [
                (indent(indent_level + 2) + 'biggest_fish_is_' + str(y) + ' : biggest_fish_is_X {' + str(y) + '}' + os.linesep)
                for y in range(max(0, x-3), x+1)
            ]
        )
        + (
            (indent(indent_level + 2) + 'biggest_fish_is_0 : biggest_fish_is_X {0}' + os.linesep)
            if x == 4 else
            (
                ('')
                if x < 4 else
                (create_subtree_selector(indent_level + 2, x - 4))
            )
        )
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
    )


def create_tree_sequence(x):
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + 'composite {' + os.linesep
        + indent(1) + 'biggest_fish_sequence' + os.linesep
        + indent(1) + 'sequence' + os.linesep
        + indent(1) + 'children {' + os.linesep
        + indent(2) + 'decorator {' + os.linesep
        + indent(3) + 'special_decorator' + os.linesep
        + indent(3) + 'inverter' + os.linesep
        + indent(3) + 'child{' + os.linesep
        + create_subtree_sequence(3, x)
        + indent(2) + '}} end_decorator' + os.linesep
        + indent(2) + 'bigger_fish {}' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_tree_selector(x):
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + 'composite {' + os.linesep
        + indent(1) + 'biggest_fish_sequence' + os.linesep
        + indent(1) + 'sequence' + os.linesep
        + indent(1) + 'children {' + os.linesep
        + create_subtree_selector(2, x)
        + indent(2) + 'bigger_fish {}' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )

def create_tree_move4bt(x):
    # number_of_nodes = x
    # number_of_nodes = number_of_checks + move4bt_selector + move4bt_check + biggest_fish_sequence + bigger_fish + find_biggest_fish
    # number_of_nodes = number_of_checks + 5
    # qed
    # number_of_checks = x - 5
    number_of_checks = x - 5
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + indent(1) + 'composite {' + os.linesep
        + indent(2) + 'move4bt_selector selector' + os.linesep
        + indent(2) + 'children {' + os.linesep
        + indent(3) + 'composite {' + os.linesep
        + indent(4) + 'biggest_fish_sequence sequence' + os.linesep
        + indent(4) + 'children {' + os.linesep
        + indent(5) + 'composite {' + os.linesep
        + indent(6) + 'find_biggest_fish selector' + os.linesep
        + indent(6) + 'children {' + os.linesep
        + ''.join([
            (indent(7) + 'biggest_fish_is_' + str(y) + ' : biggest_fish_is_X {' + str(y) + '}' + os.linesep)
            for y in range(number_of_checks)
        ])
        + indent(6) + '} end_children' + os.linesep
        + indent(5) + '} end_composite' + os.linesep
        + indent(5) + 'bigger_fish {}' + os.linesep
        + indent(4) + '} end_children' + os.linesep
        + indent(3) + '} end_composite' + os.linesep
        + indent(2) + 'move4bt_check : biggest_fish_is_X {' + str(number_of_checks) + '}' + os.linesep
        + indent(1) + '} end_children' + os.linesep
        + indent(1) + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )

def create_tree_bigger_fish(x):
    # number_of_nodes = x
    # number_of_nodes = number_of_checks + move4bt_selector + move4bt_check + biggest_fish_sequence + bigger_fish + find_biggest_fish
    # number_of_nodes = number_of_checks + 5
    # qed
    # number_of_checks = x - 5
    number_of_checks = x - 5
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + indent(3) + 'composite {' + os.linesep
        + indent(4) + 'biggest_fish_sequence sequence' + os.linesep
        + indent(4) + 'children {' + os.linesep
        + indent(5) + 'composite {' + os.linesep
        + indent(6) + 'find_biggest_fish selector' + os.linesep
        + indent(6) + 'children {' + os.linesep
        + ''.join([
            (indent(7) + 'biggest_fish_is_' + str(y) + ' : biggest_fish_is_X {' + str(y) + '}' + os.linesep)
            for y in range(number_of_checks)
        ])
        + indent(6) + '} end_children' + os.linesep
        + indent(5) + '} end_composite' + os.linesep
        + indent(5) + 'bigger_fish {}' + os.linesep
        + indent(4) + '} end_children' + os.linesep
        + indent(3) + '} end_composite' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_specifications(x):
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (globally, (eq, biggest_fish at 0, ' + str(x + 1) + '))) } end_LTLSPEC' + os.linesep
        + indent(1) + 'CTLSPEC { (always_finally, (always_globally, (eq, biggest_fish at 0, ' + str(x + 1) + '))) } end_CTLSPEC' + os.linesep
        + '} end_specifications'
    )
def create_specifications_bigger_fish(x):
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (globally, (eq, biggest_fish at 0, ' + str(x - 5) + '))) } end_LTLSPEC' + os.linesep
        + indent(1) + 'CTLSPEC { (always_finally, (always_globally, (eq, biggest_fish at 0, ' + str(x - 5) + '))) } end_CTLSPEC' + os.linesep
        + '} end_specifications'
    )
def create_specifications_move4bt(_):
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (success, move4bt_check)) } end_LTLSPEC' + os.linesep
        + '} end_specifications'
    )

def create_fish(x, tree_func, spec_func):
    return (
        create_constants()
        + create_variables()
        + create_environment()
        #+ create_checks(x)
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + tree_func(x)
        + spec_func(x)
        )

def write_files(location, mode, min_val, max_val, step_size):
    if location[-1] != '/':
        location = location + '/'
    if 'parallel' in mode:
        file_name = location + 'bigger_fish_parallel_'
        tree_func = create_tree_parallel
        spec_func = create_specifications
    elif 'sequence' in mode:
        file_name = location + 'bigger_fish_sequence_'
        tree_func = create_tree_sequence
        spec_func = create_specifications
    elif 'selector' in mode:
        file_name = location + 'bigger_fish_selector_'
        tree_func = create_tree_selector
        spec_func = create_specifications
    elif 'bigger_fish' in mode:
        file_name = location + 'bigger_fish_'
        tree_func = create_tree_bigger_fish
        spec_func = create_specifications_bigger_fish
    elif 'MoVe4BT' in mode:
        file_name = location + 'CHANGED_bigger_fish_'
        tree_func = create_tree_move4bt
        spec_func = create_specifications_move4bt
    else:
        print('unknown mode, exiting: ' + str(mode))
        sys.exit()

    for x in range(min_val, max_val + 1, step_size):
        with open(file_name + str(x) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(create_fish(x, tree_func, spec_func))

if len(sys.argv) == 6:
    write_files(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
elif len(sys.argv) == 4:
    FISH_CAP = sys.argv[3]
    write_files(sys.argv[1], sys.argv[2], int(FISH_CAP), int(FISH_CAP), 2)
