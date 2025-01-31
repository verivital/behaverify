import os
import sys


def indent(n):
    return ' '*(4*n)

def create_constants():
    return (
        'configuration {}' + os.linesep
        + 'enumerations {}' + os.linesep
        + 'constants {} end_constants' + os.linesep
    )


def create_variables():
    return (
        'variables {' + os.linesep
        + indent(1) + 'variable { bl yes_no VAR BOOLEAN assign { result {True} end_result} }' + os.linesep
        + '}' + os.linesep
    )


def create_environment():
    return (
        'environment_update {}' + os.linesep
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
        + indent(2) + 'token' + os.linesep
        + indent(2) + 'arguments {}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables {} end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
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
            indent(indent_level) + 'composite {' + os.linesep
            + indent(indent_level + 1) + 'selector' + str(node_number) + ' selector children{ volatile' + str(node_number) + ' : volatile {} token' + str(node_number) + ' : token {}}' + os.linesep
            + indent(indent_level) + '}' + os.linesep
            ,
            node_number + 1
            ,
            create_spec(node_number)
        )
    (left_child, node_number, left_specs) = create_tree_struct(parallel_mode, indent_level + 2, levels_left - 1, node_number)
    (right_child, node_number, right_specs) = create_tree_struct(parallel_mode, indent_level + 2, levels_left - 1, node_number)
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
        ,
        left_specs + right_specs
    )

def create_tree(parallel_mode, levels):
    (tree, _, specs) = create_tree_struct(parallel_mode, 1, levels, 1)
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + tree
        + '} end_tree' + os.linesep
        ,
        specs
    )

def create_spec(node_number):
    v = 'volatile' + str(node_number)
    t = 'token' + str(node_number)
    core = '(implies, (failure, ' + v + ' at -1), (success, ' + t + ' at -1))'
    return (
        indent(1) + 'INVARSPEC {' + core + '}' + os.linesep
        + indent(1) + 'LTLSPEC { (globally, ' + core + ') }' + os.linesep
        + indent(1) + 'CTLSPEC { (always_globally, ' + core + ') }' + os.linesep
    )

def create_specifications(specs):
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + specs
        + '} end_specifications' + os.linesep
    )

def create_bt(parallel_mode, levels):
    (tree, specs) = create_tree(parallel_mode, levels)
    return (
        create_constants()
        + create_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + tree
        + create_specifications(specs)
        )

def write_files(location, mode, min_val, max_val, step_size):
    print('CREATING BINARY TREE FILES')
    if location[-1] != '/':
        location = location + '/'
    if 'parallel' in mode:
        file_name = location + 'binary_tree_2_parallel_'
        parallel_mode = True
    else:
        file_name = location + 'binary_tree_2_sequence_'
        parallel_mode = False

    for levels in range(min_val, max_val + 1, step_size):
        with open(file_name + str(levels) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(create_bt(parallel_mode, levels))

if len(sys.argv) == 6:
    write_files(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
elif len(sys.argv) == 4:
    FISH_CAP = sys.argv[3]
    write_files(sys.argv[1], sys.argv[2], int(FISH_CAP), int(FISH_CAP), 2)
