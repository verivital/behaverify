import os
import sys


def indent(n):
    return ' '*(4*n)


def create_constants(grid_size):
    return (
        'configuration {}' + os.linesep
        + 'enumerations {}' + os.linesep
        + 'constants { x_max := ' + str(grid_size - 1) + ', y_max := ' + str(grid_size - 1) + '} end_constants' + os.linesep
    )


def create_variables():
    return (
        'variables {' + os.linesep
        + 'variable { bl x_true VAR [0, x_max] assign {result {0} } }' + os.linesep
        + 'variable { bl y_true VAR [0, y_max] assign {result {0} } }' + os.linesep
        + 'variable { bl x_goal VAR [0, x_max] assign {result {0} } }' + os.linesep
        + 'variable { bl y_goal VAR [0, y_max] assign {result {0} } }' + os.linesep
        + 'variable { bl remaining_goals VAR [0, 4] assign {result {4} } }' + os.linesep
        + 'variable { bl change_val VAR BOOLEAN assign {result {False}}}' + os.linesep
        + '}' + os.linesep
    )

def create_environment():
    return (
        'environment_update {} ' + os.linesep
    )

#def create_checks(x):
def create_checks():
    return (
        'checks {' + os.linesep
        + 'check {' + os.linesep
	+ 'x_too_small' + os.linesep
	+ 'arguments {}' + os.linesep
	+ 'read_variables {x_true, x_goal} end_read_variables' + os.linesep
	+ 'condition { (lt, x_true, x_goal) } end_condition' + os.linesep
        + '}' + os.linesep
        + 'check {' + os.linesep
	+ 'x_too_big' + os.linesep
	+ 'arguments {}' + os.linesep
	+ 'read_variables {x_true, x_goal} end_read_variables' + os.linesep
	+ 'condition { (gt, x_true, x_goal) } end_condition' + os.linesep
        + '}' + os.linesep
        + 'check {' + os.linesep
	+ 'y_too_small' + os.linesep
	+ 'arguments {}' + os.linesep
	+ 'read_variables {y_true, y_goal} end_read_variables' + os.linesep
	+ 'condition { (lt, y_true, y_goal) } end_condition' + os.linesep
        + '}' + os.linesep
        + 'check {' + os.linesep
	+ 'y_too_big' + os.linesep
	+ 'arguments {}' + os.linesep
	+ 'read_variables {y_true, y_goal} end_read_variables' + os.linesep
	+ 'condition { (gt, y_true, y_goal) } end_condition' + os.linesep
        + '}' + os.linesep
        + 'check {' + os.linesep
        + 'move4bt_check' + os.linesep
        + 'arguments {}' + os.linesep
        + 'read_variables {remaining_goals}' + os.linesep
        + 'condition { (eq, 0, remaining_goals) }' + os.linesep
        + '}' + os.linesep
        + 'check {' + os.linesep
        + 'not_at_goal' + os.linesep
        + 'arguments {}' + os.linesep
        + 'read_variables {x_true, y_true, x_goal, y_goal}' + os.linesep
        + 'condition { (or, (neq, x_true, x_goal), (neq, y_true, y_goal)) }' + os.linesep
        + '}' + os.linesep
        + '} end_checks' + os.linesep
    )


def create_environment_checks():
    return ('environment_checks {#{ check environment nodes are defined here }#} end_environment_checks' + os.linesep)


def create_actions():
    return (
        'actions {' + os.linesep
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'set_x_goal' + os.linesep
        + indent(2) + 'arguments {new_val := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { change_val, x_goal } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { change_val assign {result {True, False} } } end_variable_statement' + os.linesep
        + indent(3) + 'variable_statement { x_goal assign {case{change_val} result{new_val} result{x_goal} } } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { case{change_val}result { success } result{failure} } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        #
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'set_y_goal' + os.linesep
        + indent(2) + 'arguments {new_val := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { change_val, y_goal } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { change_val assign {result {True, False} } } end_variable_statement' + os.linesep
        + indent(3) + 'variable_statement { y_goal assign {case{change_val} result{new_val} result{y_goal} } } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { case{change_val}result { success } result{failure} } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        #
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'set_x_goal_final' + os.linesep
        + indent(2) + 'arguments {new_val := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { x_goal } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { x_goal assign{result{new_val}} } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { result { success } } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        #
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'set_y_goal_final' + os.linesep
        + indent(2) + 'arguments {new_val := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { y_goal } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { y_goal  assign{result{new_val}} } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { result { success } } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        #
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'update_remaining_goals' + os.linesep
        + indent(2) + 'arguments {}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { remaining_goals } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { remaining_goals  assign{result{(max, 0, (sub, remaining_goals, 1))}} } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { result { success } } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        #
        + indent(1) + 'action {' + os.linesep
        + indent(2) + 'move' + os.linesep
        + indent(2) + 'arguments {x_dir := INT, y_dir := INT}' + os.linesep
        + indent(2) + 'local_variables {} end_local_variables' + os.linesep
        + indent(2) + 'read_variables {} end_read_variables' + os.linesep
        + indent(2) + 'write_variables { x_true, y_true } end_write_variables' + os.linesep
        + indent(2) + 'initial_values {} end_initial_values' + os.linesep
        + indent(2) + 'update {' + os.linesep
        + indent(3) + 'variable_statement { x_true  assign{result{(max, 0, (min, x_max, (add, x_true, x_dir)))}} } end_variable_statement' + os.linesep
        + indent(3) + 'variable_statement { y_true  assign{result{(max, 0, (min, y_max, (add, y_true, y_dir)))}} } end_variable_statement' + os.linesep
        + indent(3) + 'return_statement { result { success } } end_return_statement' + os.linesep
        + indent(2) + '} end_update' + os.linesep
        + indent(1) + '} end_action' + os.linesep
        + '} end_actions' + os.linesep
    )

def create_tree_move4bt(grid_size):
    return (
        'sub_trees {#{ subtrees go here. }#} end_sub_trees' + os.linesep
        + 'tree {' + os.linesep
        + indent(1) + 'composite {' + os.linesep
        + indent(2) + 'move4bt_selector selector' + os.linesep
        + indent(2) + 'children {' + os.linesep
        + indent(3) + 'move4bt_check {}' + os.linesep
        + indent(3) + 'composite { world_seq sequence children {' + os.linesep
        + indent(5) + 'composite { env_sel selector children {' + os.linesep
        + indent(7) + 'not_at_goal {}' + os.linesep
        + indent(7) + 'composite { env_upd sequence children {' + os.linesep
        + indent(9) + 'update_remaining_goals {}' + os.linesep
        + indent(9) + 'composite { env_x_upd selector children {' + os.linesep
        + ''.join([
            (indent(11) + 'set_x_goal_' + str(val) + ' : set_x_goal {' + str(val) + '}' + os.linesep)
            for val in range(grid_size - 1)
        ])
        + indent(11) + 'set_x_goal_' + str(grid_size - 1) + ' : set_x_goal_final {' + str(grid_size - 1) + '}' + os.linesep
        + indent(9) + '}}' + os.linesep
        + indent(9) + 'composite { env_y_upd selector children {' + os.linesep
        + ''.join([
            (indent(11) + 'set_y_goal_' + str(val) + ' : set_y_goal {' + str(val) + '}' + os.linesep)
            for val in range(grid_size - 1)
        ])
        + indent(11) + 'set_y_goal_' + str(grid_size - 1) + ' : set_y_goal_final {' + str(grid_size - 1) + '}' + os.linesep
        + indent(9) + '}}' + os.linesep
        + indent(7) + '}}' + os.linesep
        + indent(5) + '}}' + os.linesep
        + indent(5) + 'composite { move_robot selector children{' + os.linesep
        + indent(7) + 'composite { try_right sequence children {' + os.linesep
        + indent(9) + 'x_too_small {} go_right : move {1, 0}' + os.linesep
        + indent(7) + '}}' + os.linesep
        + indent(7) + 'composite { try_left sequence children {' + os.linesep
        + indent(9) + 'x_too_big {} go_left : move {-1, 0}' + os.linesep
        + indent(7) + '}}' + os.linesep
        + indent(7) + 'composite { try_up sequence children {' + os.linesep
        + indent(9) + 'y_too_small {} go_up : move {0, 1}' + os.linesep
        + indent(7) + '}}' + os.linesep
        + indent(7) + 'composite { try_down sequence children {' + os.linesep
        + indent(9) + 'y_too_big {} go_down : move {0, -1}' + os.linesep
        + indent(7) + '}}' + os.linesep
        + indent(5) + '}}' + os.linesep
        + indent(3) + '}}' + os.linesep
        + indent(1) + '}}' + os.linesep
        + '} end_tree' + os.linesep
    )
def create_specifications_move4bt():
    return (
        'tick_prerequisite { True }' + os.linesep
        + 'specifications {' + os.linesep
        + indent(1) + 'LTLSPEC { (finally, (success, move4bt_check)) } end_LTLSPEC' + os.linesep
        + '} end_specifications'
    )

def create_simple_robot(grid_size):
    return (
        create_constants(grid_size)
        + create_variables()
        + create_environment()
        + create_checks()
        + create_environment_checks()
        + create_actions()
        + create_tree_move4bt(grid_size)
        + create_specifications_move4bt()
        )

def write_files(location, min_val, max_val, step_size):
    if location[-1] != '/':
        location = location + '/'
    file_name = location + 'CHANGED_simple_robot_'
    for x in range(min_val, max_val + 1, step_size):
        with open(file_name + str(x) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(create_simple_robot(x))

if len(sys.argv) == 5:
    write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
if len(sys.argv) == 3:
    write_files(sys.argv[1], int(sys.argv[2]), int(sys.argv[2]), 2)
