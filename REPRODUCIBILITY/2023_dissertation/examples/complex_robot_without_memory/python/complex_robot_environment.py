import py_trees
import random
import serene_safe_assignment


delayed_action_queue = []


def delay_this_action(action, node):
    global delayed_action_queue
    delayed_action_queue.append((action, node))


def execute_delayed_action_queue():
    global delayed_action_queue
    for (delayed_action, node) in delayed_action_queue:
        delayed_action(node)
    delayed_action_queue = []
    return


blackboard_reader = py_trees.blackboard.Client()
blackboard_reader.register_key(key = 'zone', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'side', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'have_flag', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'need_side_reached', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.READ)


def between_tick_environment_update():
    global x, y, flag_x, flag_y, tile_progress, tile_tracker
    if (tile_tracker == tile_progress):
        tile_progress = 0
    else:
        tile_progress = tile_progress
    tile_tracker = tile_progress
    return


x = 0
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it

y = 0
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it

hole_1 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_2 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_3 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_4 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_5 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_6 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_7 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_8 = random.choice([0, 1, 2])
# this variable is a constant. do not change it

hole_9 = random.choice([0, 1, 2])
# this variable is a constant. do not change it


def active_hole():
    if ((x + min(0, blackboard_reader.forward())) == 4):
        _active_hole_value_to_return_ = hole_1
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 1)):
        _active_hole_value_to_return_ = hole_2
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 2)):
        _active_hole_value_to_return_ = hole_3
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 3)):
        _active_hole_value_to_return_ = hole_4
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 4)):
        _active_hole_value_to_return_ = hole_5
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 5)):
        _active_hole_value_to_return_ = hole_6
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 6)):
        _active_hole_value_to_return_ = hole_7
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 7)):
        _active_hole_value_to_return_ = hole_8
    elif ((x + min(0, blackboard_reader.forward())) == (4 + 8)):
        _active_hole_value_to_return_ = hole_9
    else:
        _active_hole_value_to_return_ = -1
    return _active_hole_value_to_return_


flag_x = random.choice([15, 16, 17, 18])
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it

flag_y = random.choice([0, 1, 2])
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it


def flag_returned():
    _flag_returned_value_to_return_ = (blackboard_reader.have_flag and (x <= 3))
    return _flag_returned_value_to_return_


tile_progress = 0
# this variable develops in the following way between ticks.
#         if (tile_tracker == tile_progress):
#             tile_progress = 0
#         else:
#             tile_progress = tile_progress
#

tile_tracker = 0
# this variable develops in the following way between ticks.
#         tile_tracker = tile_progress
#
def flag_not_returned(node):
    '''
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not (flag_returned())
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    return (
        not (flag_returned())
    )
def can_move_forward(node):
    '''
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    (((blackboard_reader.forward() + x) >= 0) and ((blackboard_reader.forward() + x) <= 18) and ((active_hole() == -1) or (active_hole() == y)))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    return (
        (((blackboard_reader.forward() + x) >= 0) and ((blackboard_reader.forward() + x) <= 18) and ((active_hole() == -1) or (active_hole() == y)))
    )
def can_move_side(node):
    '''
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    (((blackboard_reader.side + y) >= 0) and ((blackboard_reader.side + y) <= 2))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    return (
        (((blackboard_reader.side + y) >= 0) and ((blackboard_reader.side + y) <= 2))
    )


def go_forward_func__0(node):
    global x
    if (((blackboard_reader.forward() + x) >= 0) and ((blackboard_reader.forward() + x) <= 18) and ((active_hole() == -1) or (active_hole() == y))):
        update_val_x = (x + blackboard_reader.forward())
    else:
        update_val_x = x
    x = serene_safe_assignment.x(update_val_x)
    return


def go_side_func__0(node):
    global y
    if (((blackboard_reader.side + y) >= 0) and ((blackboard_reader.side + y) <= 2)):
        update_val_y = (y + blackboard_reader.side)
    else:
        update_val_y = y
    y = serene_safe_assignment.y(update_val_y)
    return


def search_tile_func__condition(node):
    return True


def search_tile_func__0(node):
    if (tile_progress == 2):
        to_return_tile_searched = True
    else:
        to_return_tile_searched = random.choice([True, False])
    return to_return_tile_searched


def search_tile_func__1(node):
    if blackboard_reader.have_flag:
        to_return_have_flag = True
    else:
        to_return_have_flag = (node.tile_searched and (x == flag_x) and (y == flag_y))
    return to_return_have_flag


def update_search_func__0(node):
    global tile_progress
    if node.tile_searched:
        update_val_tile_progress = 2
    else:
        update_val_tile_progress = min(2, (1 + tile_progress))
    tile_progress = serene_safe_assignment.tile_progress(update_val_tile_progress)
    return


def compute_zone_func__condition(node):
    return True


def compute_zone_func__0(node):
    if (x <= 3):
        to_return_zone = 'home'
    elif (x >= 15):
        to_return_zone = 'target'
    else:
        to_return_zone = 'maze'
    return to_return_zone
