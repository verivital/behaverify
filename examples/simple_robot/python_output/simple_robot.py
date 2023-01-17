import have_mission_file
import target_reached_file
import x_too_small_file
import x_too_big_file
import y_too_small_file
import y_too_big_file
import get_mission_file
import get_position_file
import clear_mission_file
import go_right_file
import go_left_file
import go_up_file
import go_down_file
import py_trees


def create_tree():
    robot_control = py_trees.composites.Sequence('robot_control', False)
    get_position = get_position_file.get_position('get_position')
    reset_completed_mission = py_trees.composites.Sequence('reset_completed_mission', False)
    target_reached = target_reached_file.target_reached('target_reached')
    clear_mission = clear_mission_file.clear_mission('clear_mission')
    reset_completed_mission.add_children([target_reached, clear_mission])
    reset_completed_mission_FiS = py_trees.decorators.FailureIsSuccess(reset_completed_mission, 'reset_completed_mission_FiS')
    confirm_mission = py_trees.composites.Selector('confirm_mission', False)
    have_mission = have_mission_file.have_mission('have_mission')
    get_mission = get_mission_file.get_mission('get_mission')
    confirm_mission.add_children([have_mission, get_mission])
    move_robot = py_trees.composites.Selector('move_robot', False)
    try_right = py_trees.composites.Sequence('try_right', False)
    x_too_small = x_too_small_file.x_too_small('x_too_small')
    go_right = go_right_file.go_right('go_right')
    try_right.add_children([x_too_small, go_right])
    try_left = py_trees.composites.Sequence('try_left', False)
    x_too_big = x_too_big_file.x_too_big('x_too_big')
    go_left = go_left_file.go_left('go_left')
    try_left.add_children([x_too_big, go_left])
    try_up = py_trees.composites.Sequence('try_up', False)
    y_too_small = y_too_small_file.y_too_small('y_too_small')
    go_up = go_up_file.go_up('go_up')
    try_up.add_children([y_too_small, go_up])
    try_down = py_trees.composites.Sequence('try_down', False)
    y_too_big = y_too_big_file.y_too_big('y_too_big')
    go_down = go_down_file.go_down('go_down')
    try_down.add_children([y_too_big, go_down])
    move_robot.add_children([try_right, try_left, try_up, try_down])
    robot_control.add_children([get_position, reset_completed_mission_FiS, confirm_mission, move_robot])
    return robot_control
