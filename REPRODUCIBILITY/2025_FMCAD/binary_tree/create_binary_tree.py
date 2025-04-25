import os
import sys


def indent(n):
    return ' '*(4*n)

def create_constants(max_val):
    return (
        'configuration {}' + os.linesep
        + 'enumerations {}' + os.linesep
        + 'constants {min_val := 0, max_val := ' + str(max_val) + '} end_constants' + os.linesep
    )


def create_variables():
    return (
        'variables {' + os.linesep
        + indent(1) + 'variable { bl v VAR [min_val, max_val] assign { result {min_val} end_result} }' + os.linesep
        + indent(1) + 'variable { bl r VAR BOOLEAN assign { result {False} end_result} }' + os.linesep
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
        + indent(1) + 'check {AtVal arguments{a := INT}read_variables{v}condition{(eq, v, a)}}' + os.linesep
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'Inc' + os.linesep
        + indent(2) + 'arguments {}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables {v, r } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { r assign {result { True, False } } } end_variable_statement' + os.linesep
        + indent(3) + 'variable_statement { v assign {case{r}result{(min, max_val, (add, v, 1))}result{v}}} end_variable_statement' + os.linesep
        + indent(3) + 'return_statement {case{r}result{success}result{failure}} end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + '} end_actions' + os.linesep
    )


def create_tree_struct(indent_level, levels_left, leaf_number, composite_number):
    if levels_left == 0:
        return (
            indent(indent_level) + 'AtV' + str(leaf_number) + ' : AtVal {' + str(leaf_number) + '}' + os.linesep,
            leaf_number + 1,
            composite_number
        )
    (left_child, leaf_number, composite_number) = create_tree_struct(indent_level + 2, levels_left - 1, leaf_number, composite_number)
    (right_child, leaf_number, composite_number) = create_tree_struct(indent_level + 2, levels_left - 1, leaf_number, composite_number)
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + 'Sel' + str(composite_number) + os.linesep
        + indent(indent_level + 1) + 'selector' + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + left_child
        + right_child
        + indent(indent_level + 1) + '} end_children' + os.linesep
        + indent(indent_level) + '} end_composite' + os.linesep
        ,
        leaf_number,
        composite_number + 1
    )

def create_tree(levels):
    (tree, max_val, _) = create_tree_struct(3, levels, 0, 0)
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + indent(1) + 'composite {' + os.linesep
        + indent(2) + 'Root sequence children {' + os.linesep
        + tree
        + indent(3) + 'composite {' + os.linesep
        + indent(4) + 'Sel selector children {' + os.linesep
        + indent(5) + 'AtMax : AtVal{' + str(max_val) + '}' + os.linesep
        + indent(5) + 'Inc {}' + os.linesep
        + indent(4) + '}' + os.linesep
        + indent(3) + '}' + os.linesep
        + indent(2) + '}' + os.linesep
        + indent(1) + '}' + os.linesep
        + '} end_tree' + os.linesep,
        max_val
    )

def create_specifications():
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC {(globally, (implies, (success, AtMax), (globally, (not, (failure, AtMax)))))}' + os.linesep
        + indent(1) + 'CTLSPEC {(always_globally, (implies, (success, AtMax), (always_globally, (not, (failure, AtMax)))))}' + os.linesep
        + '} end_specifications' + os.linesep
    )

def create_bt(levels):
    (tree, max_val) = create_tree(levels)
    return (
        create_constants(max_val)
        + create_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + tree
        + create_specifications()
        )

def write_files(location, min_val, max_val, step_size):
    print('CREATING BINARY TREE FILES')
    if location[-1] != '/':
        location = location + '/'
    file_name = location + 'binary_tree_'

    for levels in range(min_val, max_val + 1, step_size):
        with open(file_name + str(levels) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(create_bt(levels))

if len(sys.argv) == 5:
    write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
elif len(sys.argv) == 3:
    FISH_CAP = sys.argv[2]
    write_files(sys.argv[1], int(FISH_CAP), int(FISH_CAP), 2)
