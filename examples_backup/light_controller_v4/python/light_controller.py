import check_fairness_file
import prepare_round_file
import turn_light_off_file
import swap_direction_file
import set_direction_file
import send_light_signal_file
import check_tunnel_in_use_file
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
    blackboard_reader.register_key(key = 'signal', access = py_trees.common.Access.WRITE)
    blackboard_reader.fairness_counter = serene_safe_assignment.fairness_counter(0)
    blackboard_reader.direction = serene_safe_assignment.direction('west_to_east')
    blackboard_reader.signal = serene_safe_assignment.signal(False)
    return blackboard_reader


def create_tree(environment):
    prepare_round = prepare_round_file.prepare_round('prepare_round', environment)
    check_tunnel_in_use = check_tunnel_in_use_file.check_tunnel_in_use('check_tunnel_in_use', environment)
    turn_light_off = turn_light_off_file.turn_light_off('turn_light_off', environment)
    tunnel_in_use = py_trees.composites.Sequence(name = 'tunnel_in_use', memory = False, children = [check_tunnel_in_use, turn_light_off])
    check_west_and_east_cars = check_west_and_east_cars_file.check_west_and_east_cars('check_west_and_east_cars', environment)
    check_fairness = check_fairness_file.check_fairness('check_fairness')
    swap_direction = swap_direction_file.swap_direction('swap_direction', environment)
    choose_fairly = py_trees.composites.Selector(name = 'choose_fairly', memory = False, children = [check_fairness, swap_direction])
    try_west_and_east = py_trees.composites.Sequence(name = 'try_west_and_east', memory = False, children = [check_west_and_east_cars, choose_fairly])
    check_west_cars = check_west_cars_file.check_west_cars('check_west_cars', environment)
    set_direction = set_direction_file.set_direction('set_direction', environment, 'west_to_east')
    try_west = py_trees.composites.Sequence(name = 'try_west', memory = False, children = [check_west_cars, set_direction])
    check_east_cars = check_east_cars_file.check_east_cars('check_east_cars', environment)
    set_direction_1 = set_direction_file.set_direction('set_direction_1', environment, 'east_to_west')
    try_east = py_trees.composites.Sequence(name = 'try_east', memory = False, children = [check_east_cars, set_direction_1])
    select_direction = py_trees.composites.Selector(name = 'select_direction', memory = False, children = [tunnel_in_use, try_west_and_east, try_west, try_east])
    send_light_signal = send_light_signal_file.send_light_signal('send_light_signal', environment)
    light_controller = py_trees.composites.Parallel(name = 'light_controller', policy = py_trees.common.ParallelPolicy.SuccessOnOne(), children = [prepare_round, select_direction, send_light_signal])
    return light_controller
