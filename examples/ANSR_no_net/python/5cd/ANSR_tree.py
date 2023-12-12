import not_at_destination_file
import y_too_small_file
import y_too_big_file
import x_too_small_file
import x_too_big_file
import update_destination_file
import move_file
import send_victory_file
import update_direction_file
import target_in_sight_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'cur_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'cur_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dest_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'dest_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'x_mode', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'y_dir', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'victory', access = py_trees.common.Access.WRITE)
    blackboard_reader.cur_x = serene_safe_assignment.cur_x(0)
    blackboard_reader.cur_y = serene_safe_assignment.cur_y(0)
    blackboard_reader.dest_x = serene_safe_assignment.dest_x(0)
    blackboard_reader.dest_y = serene_safe_assignment.dest_y(0)
    blackboard_reader.x_mode = serene_safe_assignment.x_mode(False)
    blackboard_reader.y_dir = serene_safe_assignment.y_dir(1)
    blackboard_reader.victory = serene_safe_assignment.victory(False)
    return blackboard_reader


def create_tree(environment):
    target_in_sight = target_in_sight_file.target_in_sight('target_in_sight', environment)
    send_victory = send_victory_file.send_victory('send_victory', environment)
    vision = py_trees.composites.Sequence(name = 'vision', memory = False, children = [target_in_sight, send_victory])
    not_at_destination = not_at_destination_file.not_at_destination('not_at_destination')
    update_direction = update_direction_file.update_direction('update_direction', environment)
    update_destination = update_destination_file.update_destination('update_destination', environment)
    new_destination = py_trees.composites.Sequence(name = 'new_destination', memory = False, children = [update_direction, update_destination])
    destination = py_trees.composites.Selector(name = 'destination', memory = False, children = [not_at_destination, new_destination])
    y_too_small = y_too_small_file.y_too_small('y_too_small')
    move = move_file.move('move', environment, 0, 1)
    try_up = py_trees.composites.Sequence(name = 'try_up', memory = False, children = [y_too_small, move])
    y_too_big = y_too_big_file.y_too_big('y_too_big')
    move_1 = move_file.move('move_1', environment, 0, (-1))
    try_down = py_trees.composites.Sequence(name = 'try_down', memory = False, children = [y_too_big, move_1])
    x_too_big = x_too_big_file.x_too_big('x_too_big')
    move_2 = move_file.move('move_2', environment, (-1), 0)
    try_left = py_trees.composites.Sequence(name = 'try_left', memory = False, children = [x_too_big, move_2])
    x_too_small = x_too_small_file.x_too_small('x_too_small')
    move_3 = move_file.move('move_3', environment, 1, 0)
    try_right = py_trees.composites.Sequence(name = 'try_right', memory = False, children = [x_too_small, move_3])
    movement = py_trees.composites.Selector(name = 'movement', memory = False, children = [try_up, try_down, try_left, try_right])
    destination_and_movement = py_trees.composites.Sequence(name = 'destination_and_movement', memory = False, children = [destination, movement])
    drone_control = py_trees.composites.Selector(name = 'drone_control', memory = False, children = [vision, destination_and_movement])
    return drone_control
