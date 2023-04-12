x =         x = 0

# this variable does not change bewteen ticks

y =         y = 0

# this variable does not change bewteen ticks

hole_1 = None
# this variable does not change bewteen ticks

hole_2 = None
# this variable does not change bewteen ticks

hole_3 = None
# this variable does not change bewteen ticks

hole_4 = None
# this variable does not change bewteen ticks

hole_5 = None
# this variable does not change bewteen ticks

hole_6 = None
# this variable does not change bewteen ticks

hole_7 = None
# this variable does not change bewteen ticks

hole_8 = None
# this variable does not change bewteen ticks

hole_9 = None
# this variable does not change bewteen ticks

hole_10 = None
# this variable does not change bewteen ticks

flag_x =         flag_x = random.choice([30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])

# this variable does not change bewteen ticks

flag_y = None
# this variable does not change bewteen ticks

flag_returned =         flag_returned = (blackboard.have_flag and (x <= 10))

# this variable does not change bewteen ticks

tile_progress = None
# this variable does not change bewteen ticks


def check_flag_not_returned():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not(flag_returned)
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


def can_move_forward(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard.forward
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not((((x == 0) and (blackboard.forward == -1)) or ((x == 40) and (blackboard.forward == 1)) or ((((x == 14) and (blackboard.forward == 1)) or ((x == 15) and (blackboard.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard.forward == 1)) or ((x == 16) and (blackboard.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard.forward == 1)) or ((x == 17) and (blackboard.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard.forward == 1)) or ((x == 18) and (blackboard.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard.forward == 1)) or ((x == 19) and (blackboard.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard.forward == 1)) or ((x == 20) and (blackboard.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard.forward == 1)) or ((x == 21) and (blackboard.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard.forward == 1)) or ((x == 22) and (blackboard.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard.forward == 1)) or ((x == 23) and (blackboard.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard.forward == 1)) or ((x == 24) and (blackboard.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard.forward == 1)) or ((x == 25) and (blackboard.forward == -1))) and (y != hole_10))))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


def can_move_side(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard.side
    -- RETURN
    This method is expected to return True or False.
    This method is being modeled using the following behavior:
    not((((y == 0) and (blackboard.side == -1)) or ((y == 40) and (blackboard.side == 1))))
    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


def go_forward(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard.forward
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x. Modeled using the following behavior:
                    if ((x == 0) and (blackboard.forward == -1)):
            x = 0
        elif ((x == 40) and (blackboard.forward == 1)):
            x = 40
        elif (((((x == 14) and (blackboard.forward == 1)) or ((x == 15) and (blackboard.forward == -1))) and (y != hole_1)) or ((((x == 15) and (blackboard.forward == 1)) or ((x == 16) and (blackboard.forward == -1))) and (y != hole_2)) or ((((x == 16) and (blackboard.forward == 1)) or ((x == 17) and (blackboard.forward == -1))) and (y != hole_3)) or ((((x == 17) and (blackboard.forward == 1)) or ((x == 18) and (blackboard.forward == -1))) and (y != hole_4)) or ((((x == 18) and (blackboard.forward == 1)) or ((x == 19) and (blackboard.forward == -1))) and (y != hole_5)) or ((((x == 19) and (blackboard.forward == 1)) or ((x == 20) and (blackboard.forward == -1))) and (y != hole_6)) or ((((x == 20) and (blackboard.forward == 1)) or ((x == 21) and (blackboard.forward == -1))) and (y != hole_7)) or ((((x == 21) and (blackboard.forward == 1)) or ((x == 22) and (blackboard.forward == -1))) and (y != hole_8)) or ((((x == 22) and (blackboard.forward == 1)) or ((x == 23) and (blackboard.forward == -1))) and (y != hole_8)) or ((((x == 23) and (blackboard.forward == 1)) or ((x == 24) and (blackboard.forward == -1))) and (y != hole_9)) or ((((x == 24) and (blackboard.forward == 1)) or ((x == 25) and (blackboard.forward == -1))) and (y != hole_10))):
            x = x
        else:
            x = (x + blackboard.forward)

    '''
    pass


def go_side(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : blackboard.side
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y. Modeled using the following behavior:
                    if ((y == 0) and (blackboard.side == -1)):
            y = 0
        elif ((y == 40) and (blackboard.side == 1)):
            y = 40
        else:
            y = (y + blackboard.side)

    '''
    pass


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

        2:blackboard.have_flag. Modeled using the following behavior:
                    if blackboard.have_flag:
            blackboard.have_flag = True
        else:
            blackboard.have_flag = (search_tile.tile_searched and (x == flag_x) and (y == flag_y))

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


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
    pass


def compute_zone():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:blackboard.zone. Modeled using the following behavior:
                    if (x <= 13):
            blackboard.zone = 'home'
        elif (x >= 26):
            blackboard.zone = 'target'
        else:
            blackboard.zone = 'maze'

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass
