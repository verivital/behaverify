import py_trees
import random


delayed_action_queue = []


def execute_delayed_action_queue():
    global delayed_action_queue
    for delayed_action in delayed_action_queue:
        delayed_action()
    delayed_action_queue = []
    return


blackboard_reader = py_trees.blackboard.Client()
blackboard_reader.register_key(key = 'zone', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'side', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'have_flag', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.READ)


def between_tick_environment_update():
    global x, y, flag_x, flag_y, tile_progress
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
    _flag_returned_value_to_return_ = (blackboard_reader.have_flag and (x < 3))
    return _flag_returned_value_to_return_


tile_progress = 0
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it


def check_flag_not_returned():
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


def can_move_forward():
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


def can_move_side():
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


def go_forward():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x. Modeled using the following behavior:
                    if (((blackboard_reader.forward() + x) >= 0) and ((blackboard_reader.forward() + x) <= 18) and ((active_hole() == -1) or (active_hole() == y))):
            x = (x + blackboard_reader.forward())
        else:
            x = x

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__x():
        global x
        if (((blackboard_reader.forward() + x) >= 0) and ((blackboard_reader.forward() + x) <= 18) and ((active_hole() == -1) or (active_hole() == y))):
            x = (x + blackboard_reader.forward())
        else:
            x = x
        return
    delayed_action_queue.append(delayed_update_for__x)

    return


def go_side():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y. Modeled using the following behavior:
                    if (((blackboard_reader.side + y) >= 0) and ((blackboard_reader.side + y) <= 2)):
            y = (y + blackboard_reader.side)
        else:
            y = y

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__y():
        global y
        if (((blackboard_reader.side + y) >= 0) and ((blackboard_reader.side + y) <= 2)):
            y = (y + blackboard_reader.side)
        else:
            y = y
        return
    delayed_action_queue.append(delayed_update_for__y)

    return


def search_tile(tile_searched):
    '''
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:to_return_tile_searched. Modeled using the following behavior:
                    if (tile_progress == 2):
            tile_searched = True
        else:
            tile_searched = random.choice([True, False])

        2:to_return_have_flag. Modeled using the following behavior:
                    if blackboard_reader.have_flag:
            blackboard_reader.have_flag = True
        else:
            blackboard_reader.have_flag = (tile_searched and (x == flag_x) and (y == flag_y))

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    search_tile__return_condition = True
    if search_tile__return_condition:
        if (tile_progress == 2):
            to_return_tile_searched = True
        else:
            to_return_tile_searched = random.choice([True, False])
        if blackboard_reader.have_flag:
            to_return_have_flag = True
        else:
            to_return_have_flag = (tile_searched and (x == flag_x) and (y == flag_y))
        return (True, to_return_tile_searched, to_return_have_flag)
    else:
        return (False, None, None)


def update_search(tile_searched):
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:tile_progress. Modeled using the following behavior:
                    if tile_searched:
            tile_progress = 2
        else:
            tile_progress = min(2, (1 + tile_progress))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__tile_progress():
        global tile_progress
        if tile_searched:
            tile_progress = 2
        else:
            tile_progress = min(2, (1 + tile_progress))
        return
    delayed_action_queue.append(delayed_update_for__tile_progress)

    return


def compute_zone():
    '''
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:to_return_zone. Modeled using the following behavior:
                    if (x <= 3):
            blackboard_reader.zone = 'home'
        elif (x >= 15):
            blackboard_reader.zone = 'target'
        else:
            blackboard_reader.zone = 'maze'

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    compute_zone__return_condition = True
    if compute_zone__return_condition:
        if (x <= 3):
            to_return_zone = 'home'
        elif (x >= 15):
            to_return_zone = 'target'
        else:
            to_return_zone = 'maze'
        return (True, to_return_zone)
    else:
        return (False, None)
