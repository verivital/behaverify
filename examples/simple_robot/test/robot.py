x_goal = None
# this variable develops in the following way between ticks
#         if (0 == remaining_goals):
#             x_goal = x_goal
#         elif ((x_goal == x_true) and (y_goal == y_true)):
#             x_goal = random.choice([0, 1, 2, 3, 4])
#         else:
#             x_goal = x_goal
#

y_goal = None
# this variable develops in the following way between ticks
#         if (0 == remaining_goals):
#             y_goal = y_goal
#         elif ((x_goal == x_true) and (y_goal == y_true)):
#             y_goal = random.choice([0, 1, 2, 3, 4])
#         else:
#             y_goal = y_goal
#

x_true = None
# this variable does not change bewteen ticks

y_true = None
# this variable does not change bewteen ticks

remaining_goals = None
# this variable develops in the following way between ticks
#         if ((x_goal == x_true) and (y_goal == y_true)):
#             remaining_goals = max(0, (remaining_goals - 1))
#         else:
#             remaining_goals = remaining_goals
#


def get_mission():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            modeled nondeterministically. no restriction
        1:blackboard.target_x. Modeled using the following behavior:
                    blackboard.target_x = x_goal

        2:blackboard.target_y. Modeled using the following behavior:
                    blackboard.target_y = y_goal

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


def get_position():
    '''
    -- ARGUMENTS
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:blackboard.x. Modeled using the following behavior:
                    blackboard.x = x_true

        2:blackboard.y. Modeled using the following behavior:
                    blackboard.y = y_true

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    pass


def go_x(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : 1
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x_true. Modeled using the following behavior:
                    x_true = min(4, (x_true + 1))

    '''
    '''
    -- ARGUMENTS
    @ arg0 : -1
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x_true. Modeled using the following behavior:
                    x_true = max(0, (x_true - 1))

    '''
    pass


def go_y(arg0):
    '''
    -- ARGUMENTS
    @ arg0 : 1
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y_true. Modeled using the following behavior:
                    y_true = min(4, (y_true + 1))

    '''
    '''
    -- ARGUMENTS
    @ arg0 : -1
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y_true. Modeled using the following behavior:
                    y_true = max(0, (y_true - 1))

    '''
    pass
