import check_fairness_file
import turn_light_off_file
import swap_direction_file
import set_west_file
import set_east_file
import send_light_signal_file
import check_tunnel_empty_file
import check_west_and_east_cars_file
import check_west_cars_file
import check_east_cars_file
import py_trees
import serene_safe_assignment
import random


def create_blackboard():
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'fairness_counter', access = py_trees.common.Access.WRITE)
    blackboard_reader.register_key(key = 'direction', access = py_trees.common.Access.WRITE)
    blackboard_reader.fairness_counter = serene_safe_assignment.fairness_counter(0)
    blackboard_reader.direction = serene_safe_assignment.direction('east_to_west')
    return blackboard_reader


def create_tree(environment):
    check_tunnel_empty = check_tunnel_empty_file.check_tunnel_empty('check_tunnel_empty', environment)
    turn_light_off = turn_light_off_file.turn_light_off('turn_light_off', environment)
    tunnel_clear = py_trees.composites.Selector(name = 'tunnel_clear', memory = False, children = [check_tunnel_empty, turn_light_off])
    check_west_and_east_cars = check_west_and_east_cars_file.check_west_and_east_cars('check_west_and_east_cars', environment)
    check_fairness = check_fairness_file.check_fairness('check_fairness')
    swap_direction = swap_direction_file.swap_direction('swap_direction', environment)
    choose_fairly = py_trees.composites.Selector(name = 'choose_fairly', memory = False, children = [check_fairness, swap_direction])
    try_west_and_east = py_trees.composites.Sequence(name = 'try_west_and_east', memory = False, children = [check_west_and_east_cars, choose_fairly])
    check_west_cars = check_west_cars_file.check_west_cars('check_west_cars', environment)
    set_west = set_west_file.set_west('set_west', environment)
    try_west = py_trees.composites.Sequence(name = 'try_west', memory = False, children = [check_west_cars, set_west])
    check_east_cars = check_east_cars_file.check_east_cars('check_east_cars', environment)
    set_east = set_east_file.set_east('set_east', environment)
    try_east = py_trees.composites.Sequence(name = 'try_east', memory = False, children = [check_east_cars, set_east])
    select_direction = py_trees.composites.Selector(name = 'select_direction', memory = False, children = [try_west_and_east, try_west, try_east])
    send_light_signal = send_light_signal_file.send_light_signal('send_light_signal', environment)
    light_controller = py_trees.composites.Sequence(name = 'light_controller', memory = False, children = [tunnel_clear, select_direction, send_light_signal])
    return light_controller
