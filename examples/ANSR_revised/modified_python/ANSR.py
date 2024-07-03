from pathlib import Path
import py_trees
import not_at_destination_file
import valid_destination_check_file
import read_position_file
import read_destination_file
import request_new_destination_file
import read_map_file
import compute_next_file
import send_next_file


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'map_exists', access = py_trees.common.Access.WRITE)
    blackboard_reader.map_exists = None
    blackboard_reader.register_key(key = 'drone_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_x = None
    blackboard_reader.register_key(key = 'drone_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_y = None
    blackboard_reader.register_key(key = 'drone_z', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_z = None
    blackboard_reader.register_key(key = 'previous_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.previous_x = None
    blackboard_reader.register_key(key = 'previous_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.previous_y = None
    blackboard_reader.register_key(key = 'previous_z', access = py_trees.common.Access.WRITE)
    blackboard_reader.previous_z = None
    blackboard_reader.register_key(key = 'drone_x_delta', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_x_delta = None
    blackboard_reader.register_key(key = 'drone_y_delta', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_y_delta = None
    blackboard_reader.register_key(key = 'destination_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.destination_x = None
    blackboard_reader.register_key(key = 'destination_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.destination_y = None
    blackboard_reader.register_key(key = 'destination_z', access = py_trees.common.Access.WRITE)
    blackboard_reader.destination_z = None
    blackboard_reader.register_key(key = 'valid_destination', access = py_trees.common.Access.WRITE)
    blackboard_reader.valid_destination = None
    blackboard_reader.register_key(key = 'next_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.next_x = None
    blackboard_reader.register_key(key = 'next_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.next_y = None
    blackboard_reader.register_key(key = 'next_z', access = py_trees.common.Access.WRITE)
    blackboard_reader.next_z = None
    blackboard_reader.register_key(key = 'next_x_delta', access = py_trees.common.Access.WRITE)
    blackboard_reader.next_x_delta = None
    blackboard_reader.register_key(key = 'next_y_delta', access = py_trees.common.Access.WRITE)
    blackboard_reader.next_y_delta = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    blackboard_reader.map_exists = False
    blackboard_reader.drone_x = 0
    blackboard_reader.drone_y = 0
    blackboard_reader.drone_z = 0
    blackboard_reader.previous_x = 0
    blackboard_reader.previous_y = 0
    blackboard_reader.previous_z = 0
    blackboard_reader.drone_x_delta = 0
    blackboard_reader.drone_y_delta = 0
    blackboard_reader.destination_x = 0
    blackboard_reader.destination_y = 0
    blackboard_reader.destination_z = 0
    blackboard_reader.valid_destination = False
    blackboard_reader.next_x = 0
    blackboard_reader.next_y = 0
    blackboard_reader.next_z = 0
    blackboard_reader.next_x_delta = 0
    blackboard_reader.next_y_delta = 0
    return


def create_tree(environment):
    read_map = read_map_file.read_map('read_map', environment)
    read_position = read_position_file.read_position('read_position', environment)
    not_at_destination = not_at_destination_file.not_at_destination('not_at_destination')
    valid_destination_check = valid_destination_check_file.valid_destination_check('valid_destination_check')
    current_destination = py_trees.composites.Sequence(name = 'current_destination', memory = False, children = [not_at_destination, valid_destination_check])
    read_destination = read_destination_file.read_destination('read_destination', environment)
    destination_selector = py_trees.composites.Selector(name = 'destination_selector', memory = False, children = [current_destination, read_destination])
    compute_next = compute_next_file.compute_next('compute_next', environment)
    request_new_destination = request_new_destination_file.request_new_destination('request_new_destination', environment)
    plot_course = py_trees.composites.Selector(name = 'plot_course', memory = False, children = [compute_next, request_new_destination])
    send_next = send_next_file.send_next('send_next', environment)
    drone_control = py_trees.composites.Sequence(name = 'drone_control', memory = False, children = [read_map, read_position, destination_selector, plot_course, send_next])
    return drone_control
