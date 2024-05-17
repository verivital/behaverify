from pathlib import Path
import py_trees
import cell_changed_file
import not_at_destination_file
import new_destination_file
import next_action_file
import read_monitor_file
import read_position_file
import send_action_file


def create_blackboard(serene_randomizer):
    blackboard_reader = py_trees.blackboard.Client()
    blackboard_reader.register_key(key = 'serene_randomizer', access = py_trees.common.Access.WRITE)
    blackboard_reader.serene_randomizer = serene_randomizer
    blackboard_reader.register_key(key = 'drone_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_x = None
    blackboard_reader.register_key(key = 'drone_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_y = None
    blackboard_reader.register_key(key = 'drone_speed', access = py_trees.common.Access.WRITE)
    blackboard_reader.drone_speed = None
    blackboard_reader.register_key(key = 'destination_x', access = py_trees.common.Access.WRITE)
    blackboard_reader.destination_x = None
    blackboard_reader.register_key(key = 'destination_y', access = py_trees.common.Access.WRITE)
    blackboard_reader.destination_y = None
    blackboard_reader.register_key(key = 'cell_changed_var', access = py_trees.common.Access.WRITE)
    blackboard_reader.cell_changed_var = None
    blackboard_reader.register_key(key = 'current_action', access = py_trees.common.Access.WRITE)
    blackboard_reader.current_action = None
    blackboard_reader.register_key(key = 'fake_network', access = py_trees.common.Access.WRITE)
    blackboard_reader.fake_network = None
    return blackboard_reader

def initialize_blackboard(blackboard_reader):
    def long_if_0():
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 4) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'left'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((5 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 3)):
            return 'left'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (5 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 5) and (blackboard_reader.destination_x == 2) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 1)):
            return 'left'
        if ((5 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 4) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((5 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 5) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 4) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'left'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 2) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'left'
        if ((3 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 2) and (blackboard_reader.destination_y == 1)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 3)):
            return 'left'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 2) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 2)):
            return 'left'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 1) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (1 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'left'
        if ((5 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 1) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 4) and (blackboard_reader.destination_y == 1)):
            return 'left'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 2) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((5 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((blackboard_reader.drone_x == 5) and (blackboard_reader.drone_y == 2) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 2)):
            return 'left'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 0) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 2) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((3 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 2) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 5) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 1)):
            return 'left'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 2) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 2) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 5) and (blackboard_reader.destination_y == 2)):
            return 'left'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 0) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 3) and (blackboard_reader.destination_y == 1)):
            return 'left'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 3)):
            return 'left'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 2) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 0)):
            return 'left'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 4) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 4)):
            return 'left'
        if ((blackboard_reader.drone_x == 5) and (blackboard_reader.drone_y == 5) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 3) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 5) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 5) and (blackboard_reader.destination_y == 5)):
            return 'left'
        if ((blackboard_reader.drone_x == 6) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 6)):
            return 'left'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 1)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 1) and (3 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (1 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'right'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 4)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 6) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 2) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 2)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 5) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'right'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 2) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 5) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 4) and (blackboard_reader.destination_y == 5)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 3) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 5) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 5) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 5)):
            return 'right'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 2) and (blackboard_reader.drone_y == 0) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 4) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 2) and (5 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 2)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 1)):
            return 'right'
        if ((blackboard_reader.drone_x == 5) and (blackboard_reader.drone_y == 5) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 5)):
            return 'right'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 2) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 3) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 3) and (blackboard_reader.destination_y == 4)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 1) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 4) and (blackboard_reader.drone_y == 5) and (5 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 5)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 3) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'right'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 3) and (blackboard_reader.destination_y == 1)):
            return 'right'
        if ((blackboard_reader.drone_x == 2) and (blackboard_reader.drone_y == 4) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'right'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 2) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (3 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (blackboard_reader.drone_y == 1) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 1)):
            return 'right'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 5) and (blackboard_reader.drone_y == 1) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 1)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 4) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 5) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 5) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 5)):
            return 'right'
        if ((blackboard_reader.drone_x == 4) and (blackboard_reader.drone_y == 3) and (5 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'right'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 5) and (blackboard_reader.drone_y == 6) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 4) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'right'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 4)):
            return 'right'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 2) and (blackboard_reader.destination_y == 0)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 6) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 0) and (5 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'right'
        if ((blackboard_reader.drone_x == 3) and (blackboard_reader.drone_y == 5) and (blackboard_reader.destination_x == 4) and (blackboard_reader.destination_y == 5)):
            return 'right'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 5) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 4)):
            return 'right'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 4) and (2 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 4)):
            return 'right'
        if ((blackboard_reader.drone_x == 5) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 3)):
            return 'right'
        if ((blackboard_reader.drone_x == 5) and (blackboard_reader.drone_y == 2) and (blackboard_reader.destination_x == 6) and (blackboard_reader.destination_y == 2)):
            return 'right'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'right'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 3) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'up'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 4) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 5)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 3) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 3)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 2) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 3)):
            return 'up'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 6)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 2) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'up'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 5)):
            return 'up'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 0) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 4) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 5)):
            return 'up'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 3) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'up'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (4 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 6)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 2) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 4)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 1) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 2)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (1 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 6)):
            return 'up'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 4) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 5)):
            return 'up'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 0) and (blackboard_reader.destination_x == 0) and (blackboard_reader.destination_y == 6)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 1) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 2)):
            return 'up'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 3) and (blackboard_reader.destination_x == 0) and (5 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'up'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 0) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 0) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 1)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 0) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'up'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 2) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (5 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'up'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (0 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (4 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 6)):
            return 'up'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (1 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (1 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 2)):
            return 'down'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 4) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (blackboard_reader.drone_y == 3) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 2)):
            return 'down'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 5) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'down'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'down'
        if ((blackboard_reader.drone_x == 1) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'down'
        if ((blackboard_reader.drone_x == 0) and (1 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 5)):
            return 'down'
        if ((blackboard_reader.drone_x == 1) and (1 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (5 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 6) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 4)):
            return 'down'
        if ((2 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (5 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 1)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 2) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 3)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (1 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 1) and (blackboard_reader.drone_y == 2) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 3)):
            return 'down'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 5) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (2 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'down'
        if ((1 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 3) and (blackboard_reader.drone_y == 1) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 0)):
            return 'down'
        if ((0 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (blackboard_reader.drone_y == 6) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (0 <= blackboard_reader.destination_y) and (blackboard_reader.destination_y <= 3)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 1)):
            return 'down'
        if ((blackboard_reader.drone_x == 0) and (blackboard_reader.drone_y == 6) and (1 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 4)):
            return 'down'
        if ((blackboard_reader.drone_x == 1) and (blackboard_reader.drone_y == 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 1)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (3 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 4) and (4 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 6) and (blackboard_reader.destination_y == 2)):
            return 'down'
        if ((blackboard_reader.drone_x == 0) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 1)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 6) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 3) and (blackboard_reader.destination_y == 1)):
            return 'down'
        if ((4 <= blackboard_reader.drone_x) and (blackboard_reader.drone_x <= 6) and (2 <= blackboard_reader.drone_y) and (blackboard_reader.drone_y <= 3) and (0 <= blackboard_reader.destination_x) and (blackboard_reader.destination_x <= 1) and (blackboard_reader.destination_y == 2)):
            return 'down'
        return 'no_action'
    blackboard_reader.drone_x = 0
    blackboard_reader.drone_y = 0
    blackboard_reader.drone_speed = 1
    blackboard_reader.destination_x = blackboard_reader.drone_x
    blackboard_reader.destination_y = blackboard_reader.drone_y
    blackboard_reader.cell_changed_var = False
    blackboard_reader.current_action = 'no_action'


    def fake_network():
        return long_if_0()

    blackboard_reader.fake_network = fake_network
    return


def create_tree(environment):
    read_position = read_position_file.read_position('read_position', environment)
    read_monitor = read_monitor_file.read_monitor('read_monitor', environment)
    cell_changed = cell_changed_file.cell_changed('cell_changed')
    not_at_destination = not_at_destination_file.not_at_destination('not_at_destination')
    new_destination = new_destination_file.new_destination('new_destination', environment)
    destination_selector = py_trees.composites.Selector(name = 'destination_selector', memory = False, children = [not_at_destination, new_destination])
    next_action = next_action_file.next_action('next_action', environment)
    send_action = send_action_file.send_action('send_action', environment)
    drone_control = py_trees.composites.Sequence(name = 'drone_control', memory = False, children = [read_position, read_monitor, cell_changed, destination_selector, next_action, send_action])
    return drone_control
