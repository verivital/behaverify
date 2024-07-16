from pathlib import Path
import py_trees
import ebt.bt.goal_requested_check_file as goal_requested_check_file
import ebt.bt.not_at_goal_file as not_at_goal_file
import ebt.bt.valid_goal_check_file as valid_goal_check_file
import ebt.bt.valid_position_check_file as valid_position_check_file
import ebt.bt.compute_waypoint_file as compute_waypoint_file
import ebt.bt.read_goal_file as read_goal_file
import ebt.bt.read_map_file as read_map_file
import ebt.bt.read_position_file as read_position_file
import ebt.bt.send_invalid_goal_request_file as send_invalid_goal_request_file
import ebt.bt.send_next_goal_request_file as send_next_goal_request_file
import ebt.bt.send_waypoint_file as send_waypoint_file


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'goal', access = py_trees.common.Access.WRITE)
    blackboard_reader.goal = None
    blackboard_reader.register_key(key = 'goal_requested', access = py_trees.common.Access.WRITE)
    blackboard_reader.goal_requested = None
    blackboard_reader.register_key(key = 'map_exists', access = py_trees.common.Access.WRITE)
    blackboard_reader.map_exists = None
    blackboard_reader.register_key(key = 'position', access = py_trees.common.Access.WRITE)
    blackboard_reader.position = None
    blackboard_reader.register_key(key = 'valid_goal', access = py_trees.common.Access.WRITE)
    blackboard_reader.valid_goal = None
    blackboard_reader.register_key(key = 'valid_position', access = py_trees.common.Access.WRITE)
    blackboard_reader.valid_position = None
    blackboard_reader.register_key(key = 'waypoint', access = py_trees.common.Access.WRITE)
    blackboard_reader.waypoint = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.goal = [0 for _ in range(3)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.goal[index] = val
    blackboard_reader.goal_requested = False
    blackboard_reader.map_exists = False
    blackboard_reader.position = [0 for _ in range(3)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.position[index] = val
    blackboard_reader.valid_goal = False
    blackboard_reader.valid_position = False
    blackboard_reader.waypoint = [0 for _ in range(3)]
    __temp_var__ = []
    for (index, val) in __temp_var__:
        blackboard_reader.waypoint[index] = val
    return


def create_tree(environment):
    read_position = read_position_file.read_position('read_position', environment)
    not_at_goal = not_at_goal_file.not_at_goal('not_at_goal')
    valid_goal_check = valid_goal_check_file.valid_goal_check('valid_goal_check')
    current_goal = py_trees.composites.Sequence(name = 'current_goal', memory = False, children = [not_at_goal, valid_goal_check])
    read_goal = read_goal_file.read_goal('read_goal', environment)
    goal_requested_check = goal_requested_check_file.goal_requested_check('goal_requested_check')
    send_next_goal_request = send_next_goal_request_file.send_next_goal_request('send_next_goal_request', environment)
    new_goal = py_trees.composites.Selector(name = 'new_goal', memory = False, children = [goal_requested_check, send_next_goal_request])
    cannot_continue = py_trees.decorators.SuccessIsFailure(name = 'cannot_continue', child = new_goal)
    validate_goal = py_trees.composites.Selector(name = 'validate_goal', memory = False, children = [current_goal, read_goal, cannot_continue])
    read_map = read_map_file.read_map('read_map', environment)
    map_and_goal = py_trees.composites.Parallel(name = 'map_and_goal', policy = py_trees.common.ParallelPolicy.SuccessOnAll(False), children = [validate_goal, read_map])
    valid_position_check = valid_position_check_file.valid_position_check('valid_position_check')
    compute_waypoint = compute_waypoint_file.compute_waypoint('compute_waypoint', environment)
    send_invalid_goal_request = send_invalid_goal_request_file.send_invalid_goal_request('send_invalid_goal_request', environment)
    plot_waypoint = py_trees.composites.Selector(name = 'plot_waypoint', memory = False, children = [compute_waypoint, send_invalid_goal_request])
    send_waypoint = send_waypoint_file.send_waypoint('send_waypoint', environment)
    drone_control = py_trees.composites.Sequence(name = 'drone_control', memory = False, children = [read_position, map_and_goal, valid_position_check, plot_waypoint, send_waypoint])
    return drone_control
