import os
import sys


def indent(n):
    return ' '*(4*n)

TURN_LIMIT = '10'
def create_constants():
    return (
        'configuration {}' + os.linesep
        + 'enumerations {}' + os.linesep
        + 'constants { turn_limit := ' + TURN_LIMIT + ' } end_constants' + os.linesep
    )


def create_variables():
    return (
        'variables {' + os.linesep
        + indent(1) + 'variable { bl yes_no VAR BOOLEAN assign { result {True} end_result} }' + os.linesep
        + indent(1) + 'variable { bl counter VAR [0, turn_limit] assign { result {0} end_result} }' + os.linesep
        + '}' + os.linesep
    )


def create_environment():
    return (
        'environment_update {}' + os.linesep
        # 'environment_update {variable_statement{counter assign{result{(min, turn_limit, (add, counter, 1))}}}}' + os.linesep
    )





#def create_checks(x):
def create_checks():
    return (
        'checks {' + os.linesep
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'change' + os.linesep
        + indent(2) + 'arguments {val := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { counter } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { counter assign {result { (min, turn_limit, (max, 0, (add, counter, val))) } } } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement {result { success } } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        ###########
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'volatile' + os.linesep
        + indent(2) + 'arguments {}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { yes_no } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { yes_no assign {result { True, False } } } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement {case{yes_no}result { success } result{failure} } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + '} end_actions' + os.linesep
    )


def create_tree_struct(parallel_mode, indent_level, levels_left, node_number):
    if levels_left == 0:
        return (
            indent(indent_level) + 'leaf_' + str(node_number) + ' : volatile {}' + os.linesep,
            node_number + 1
        )
    (left_child, node_number) = create_tree_struct(parallel_mode, indent_level + 2, levels_left - 1, node_number)
    (right_child, node_number) = create_tree_struct(parallel_mode, indent_level + 2, levels_left - 1, node_number)
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + ('parallel' if parallel_mode else 'sequence') + str(node_number) + os.linesep
        + indent(indent_level + 1) + ('parallel policy success_on_one' if parallel_mode else 'sequence') + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + left_child
        + right_child
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
        ,
        node_number + 1
    )

def create_tree(parallel_mode, levels):
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + indent(1) + 'composite {' + os.linesep
        + indent(2) + 'overall sequence children{' + os.linesep
        + indent(3) + 'inc : change {1}' + os.linesep
        + create_tree_struct(parallel_mode, 3, levels, 1)[0]
        + indent(3) + 'dec : change {-1}' + os.linesep
        + indent(2) + '}' + os.linesep
        + indent(1) + '}' + os.linesep
        + '} end_tree' + os.linesep
    )


def create_specifications():
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (globally, (eq, counter at 0, turn_limit))) } end_LTLSPEC' + os.linesep
        + indent(1) + 'CTLSPEC { (always_finally, (always_globally, (eq, counter at 0, turn_limit))) } end_CTLSPEC' + os.linesep
        + '} end_specifications'
    )

def create_bt(parallel_mode, levels):
    return (
        create_constants()
        + create_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + create_tree(parallel_mode, levels)
        + create_specifications()
        )

def write_files(location, mode, min_val, max_val, step_size):
    print('CREATING BINARY TREE FILES')
    if location[-1] != '/':
        location = location + '/'
    if 'parallel' in mode:
        file_name = location + 'binary_tree_1_parallel_'
        parallel_mode = True
    else:
        file_name = location + 'binary_tree_1_sequence_'
        parallel_mode = False

    for levels in range(min_val, max_val + 1, step_size):
        with open(file_name + str(levels) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(create_bt(parallel_mode, levels))

if len(sys.argv) == 6:
    write_files(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
elif len(sys.argv) == 4:
    FISH_CAP = sys.argv[3]
    write_files(sys.argv[1], sys.argv[2], int(FISH_CAP), int(FISH_CAP), 2)
