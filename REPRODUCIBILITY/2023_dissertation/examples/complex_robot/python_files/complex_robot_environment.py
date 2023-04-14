import py_trees
import random


delayed_action_queue = []


def execute_delayed_action_queue():
    global delayed_action_queue
    for delayed_action in delayed_action_queue:
        delayed_action()
    return


blackboard_reader = py_trees.blackboard.Client()
blackboard_reader.register_key(key = 'zone', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'forward', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'side', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'have_flag', access = py_trees.common.Access.READ)

x = 0
# this variable does not change between ticks

y = 0
# this variable does not change between ticks

hole_1 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_2 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_3 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_4 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_5 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_6 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_7 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_8 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_9 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

hole_10 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

flag_x = random.choice([30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks

flag_y = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
# this variable does not change between ticks


def flag_returned():
    _flag_returned_value_to_return_ = (blackboard_reader.have_flag and (x <= 10))
    return _flag_returned_value_to_return_
# this variable does not change between ticks


tile_progress = random.choice([0, 1, 2])
# this variable does not change between ticks


def check_flag_not_returned():
    '''
    -- ARGUMENTS
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


def can_move_forward(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard_reader.forward
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not ((((x == 0) and (blackboard_reader.forward == -1)) or ((x == 40) and (blackboard_reader.forward == 1)) or ((((x == 14) and (blackboard_reader.forward == 1)) or ((x == 15) and (blackboard_reader.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard_reader.forward == 1)) or ((x == 16) and (blackboard_reader.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard_reader.forward == 1)) or ((x == 17) and (blackboard_reader.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard_reader.forward == 1)) or ((x == 18) and (blackboard_reader.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard_reader.forward == 1)) or ((x == 19) and (blackboard_reader.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard_reader.forward == 1)) or ((x == 20) and (blackboard_reader.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard_reader.forward == 1)) or ((x == 21) and (blackboard_reader.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard_reader.forward == 1)) or ((x == 22) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard_reader.forward == 1)) or ((x == 23) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard_reader.forward == 1)) or ((x == 24) and (blackboard_reader.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard_reader.forward == 1)) or ((x == 25) and (blackboard_reader.forward == -1))) and (y != hole_10))))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    return (
        not ((((x == 0) and (blackboard_reader.forward == -1)) or ((x == 40) and (blackboard_reader.forward == 1)) or ((((x == 14) and (blackboard_reader.forward == 1)) or ((x == 15) and (blackboard_reader.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard_reader.forward == 1)) or ((x == 16) and (blackboard_reader.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard_reader.forward == 1)) or ((x == 17) and (blackboard_reader.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard_reader.forward == 1)) or ((x == 18) and (blackboard_reader.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard_reader.forward == 1)) or ((x == 19) and (blackboard_reader.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard_reader.forward == 1)) or ((x == 20) and (blackboard_reader.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard_reader.forward == 1)) or ((x == 21) and (blackboard_reader.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard_reader.forward == 1)) or ((x == 22) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard_reader.forward == 1)) or ((x == 23) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard_reader.forward == 1)) or ((x == 24) and (blackboard_reader.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard_reader.forward == 1)) or ((x == 25) and (blackboard_reader.forward == -1))) and (y != hole_10))))
    )


def can_move_side(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard_reader.side
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not ((((y == 0) and (blackboard_reader.side == -1)) or ((y == 40) and (blackboard_reader.side == 1))))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    return (
        not ((((y == 0) and (blackboard_reader.side == -1)) or ((y == 40) and (blackboard_reader.side == 1))))
    )


def go_forward(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard_reader.forward
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x. Modeled using the following behavior:
                    if ((x == 0) and (blackboard_reader.forward == -1)):
            x = 0
        elif ((x == 40) and (blackboard_reader.forward == 1)):
            x = 40
        elif (((((x == 14) and (blackboard_reader.forward == 1)) or ((x == 15) and (blackboard_reader.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard_reader.forward == 1)) or ((x == 16) and (blackboard_reader.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard_reader.forward == 1)) or ((x == 17) and (blackboard_reader.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard_reader.forward == 1)) or ((x == 18) and (blackboard_reader.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard_reader.forward == 1)) or ((x == 19) and (blackboard_reader.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard_reader.forward == 1)) or ((x == 20) and (blackboard_reader.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard_reader.forward == 1)) or ((x == 21) and (blackboard_reader.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard_reader.forward == 1)) or ((x == 22) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard_reader.forward == 1)) or ((x == 23) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard_reader.forward == 1)) or ((x == 24) and (blackboard_reader.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard_reader.forward == 1)) or ((x == 25) and (blackboard_reader.forward == -1))) and (y != hole_10))):
            x = x
        else:
            x = (x + blackboard_reader.forward)

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__x():
        global x
        if ((x == 0) and (blackboard_reader.forward == -1)):
            x = 0
        elif ((x == 40) and (blackboard_reader.forward == 1)):
            x = 40
        elif (((((x == 14) and (blackboard_reader.forward == 1)) or ((x == 15) and (blackboard_reader.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard_reader.forward == 1)) or ((x == 16) and (blackboard_reader.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard_reader.forward == 1)) or ((x == 17) and (blackboard_reader.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard_reader.forward == 1)) or ((x == 18) and (blackboard_reader.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard_reader.forward == 1)) or ((x == 19) and (blackboard_reader.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard_reader.forward == 1)) or ((x == 20) and (blackboard_reader.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard_reader.forward == 1)) or ((x == 21) and (blackboard_reader.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard_reader.forward == 1)) or ((x == 22) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard_reader.forward == 1)) or ((x == 23) and (blackboard_reader.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard_reader.forward == 1)) or ((x == 24) and (blackboard_reader.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard_reader.forward == 1)) or ((x == 25) and (blackboard_reader.forward == -1))) and (y != hole_10))):
            x = x
        else:
            x = (x + blackboard_reader.forward)
        return
    delayed_action_queue.append(delayed_update_for__x)

    return


def go_side(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard_reader.side
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y. Modeled using the following behavior:
                    if ((y == 0) and (blackboard_reader.side == -1)):
            y = 0
        elif ((y == 40) and (blackboard_reader.side == 1)):
            y = 40
        else:
            y = (y + blackboard_reader.side)

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__y():
        global y
        if ((y == 0) and (blackboard_reader.side == -1)):
            y = 0
        elif ((y == 40) and (blackboard_reader.side == 1)):
            y = 40
        else:
            y = (y + blackboard_reader.side)
        return
    delayed_action_queue.append(delayed_update_for__y)

    return


def search_tile():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:search_tile.tile_searched. Modeled using the following behavior:
                    if (tile_progress == 2):
            search_tile.tile_searched = True
        else:
            search_tile.tile_searched = random.choice([True, False])

        2:blackboard_reader.have_flag. Modeled using the following behavior:
                    if blackboard_reader.have_flag:
            blackboard_reader.have_flag = True
        else:
            blackboard_reader.have_flag = (search_tile.tile_searched and (x == flag_x) and (y == flag_y))

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    search_tile__return_condition = True
    if search_tile__return_condition:
        if (tile_progress == 2):
            search_tile.tile_searched = True
        else:
            search_tile.tile_searched = random.choice([True, False])
        if blackboard_reader.have_flag:
            blackboard_reader.have_flag = True
        else:
            blackboard_reader.have_flag = (search_tile.tile_searched and (x == flag_x) and (y == flag_y))
        return (True, search_tile.tile_searched, blackboard_reader.have_flag)
    else:
        return (False, None, None)


def update_search(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : (search_tile.tile_searched)
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:tile_progress. Modeled using the following behavior:
                    if search_tile.tile_searched:
            tile_progress = 2
        else:
            tile_progress = min(2, (1 + tile_progress))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__tile_progress():
        global tile_progress
        if search_tile.tile_searched:
            tile_progress = 2
        else:
            tile_progress = min(2, (1 + tile_progress))
        return
    delayed_action_queue.append(delayed_update_for__tile_progress)

    return


def compute_zone():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:blackboard_reader.zone. Modeled using the following behavior:
                    if (x <= 13):
            blackboard_reader.zone = 'home'
        elif (x >= 26):
            blackboard_reader.zone = 'target'
        else:
            blackboard_reader.zone = 'maze'

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    compute_zone__return_condition = True
    if compute_zone__return_condition:
        if (x <= 13):
            blackboard_reader.zone = 'home'
        elif (x >= 26):
            blackboard_reader.zone = 'target'
        else:
            blackboard_reader.zone = 'maze'
        return (True, blackboard_reader.zone)
    else:
        return (False, None)
