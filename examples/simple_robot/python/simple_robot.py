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
import serene_safe_assignment


def create_tree():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'target_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'target_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'mission', access = py_trees.common.Access.WRITE)
    blackboard_reader.x = serene_safe_assignment.x(0)
    blackboard_reader.y = serene_safe_assignment.y(0)
    blackboard_reader.target_x = serene_safe_assignment.target_x(0)
    blackboard_reader.target_y = serene_safe_assignment.target_y(0)
    blackboard_reader.mission = serene_safe_assignment.mission(False)

    get_position = get_position_file.get_position('get_position')
    target_reached = target_reached_file.target_reached('target_reached')
    clear_mission = clear_mission_file.clear_mission('clear_mission')
    reset_completed_mission = py_trees.composites.Sequence(name = 'reset_completed_mission', memory = False, children = [target_reached, clear_mission])
    reset_completed_mission_FiS = py_trees.decorators.FailureIsSuccess(name = 'reset_completed_mission_FiS', child = reset_completed_mission)
    have_mission = have_mission_file.have_mission('have_mission')
    get_mission = get_mission_file.get_mission('get_mission')
    confirm_mission = py_trees.composites.Selector(name = 'confirm_mission', memory = False, children = [have_mission, get_mission])
    x_too_small = x_too_small_file.x_too_small('x_too_small')
    go_right = go_right_file.go_right('go_right')
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, go_right])
    x_too_big = x_too_big_file.x_too_big('x_too_big')
    go_left = go_left_file.go_left('go_left')
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, go_left])
    y_too_small = y_too_small_file.y_too_small('y_too_small')
    go_up = go_up_file.go_up('go_up')
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, go_up])
    y_too_big = y_too_big_file.y_too_big('y_too_big')
    go_down = go_down_file.go_down('go_down')
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, go_down])
    move_robot = py_trees.composites.Selector(name = 'move_robot', memory = False, children = [try_right, try_left, try_up, try_down])
    robot_control = py_trees.composites.Sequence(name = 'robot_control', memory = False, children = [get_position, reset_completed_mission_FiS, confirm_mission, move_robot])
    return robot_control
