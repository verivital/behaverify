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
blackboard_reader.register_key(key = 'x', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'y', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'target_x', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'target_y', access = py_trees.common.Access.READ)
blackboard_reader.register_key(key = 'mission', access = py_trees.common.Access.READ)


def between_tick_environment_update():
    global x_goal, y_goal, x_true, y_true, remaining_goals
    if ((x_goal == x_true) and (y_goal == y_true)):
        remaining_goals = max(0, (remaining_goals - 1))
    else:
        remaining_goals = remaining_goals
    if (0 == remaining_goals):
        x_goal = x_goal
    elif ((x_goal == x_true) and (y_goal == y_true)):
        x_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    else:
        x_goal = x_goal
    if (0 == remaining_goals):
        y_goal = y_goal
    elif ((x_goal == x_true) and (y_goal == y_true)):
        y_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    else:
        y_goal = y_goal
    return


x_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# this variable develops in the following way between ticks.
#         if (0 == remaining_goals):
#             x_goal = x_goal
#         elif ((x_goal == x_true) and (y_goal == y_true)):
#             x_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#         else:
#             x_goal = x_goal
#

y_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# this variable develops in the following way between ticks.
#         if (0 == remaining_goals):
#             y_goal = y_goal
#         elif ((x_goal == x_true) and (y_goal == y_true)):
#             y_goal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#         else:
#             y_goal = y_goal
#

x_true = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it

y_true = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# this variable does not change between ticks
# it should only change if a behavior tree leaf calls a method that changes it instantly or adds a method to the delayed action queue to change it

remaining_goals = random.choice([3])
# this variable develops in the following way between ticks.
#         if ((x_goal == x_true) and (y_goal == y_true)):
#             remaining_goals = max(0, (remaining_goals - 1))
#         else:
#             remaining_goals = remaining_goals
#


def get_mission():
    '''
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:to_return_target_x. Modeled using the following behavior:
                    blackboard_reader.target_x = x_goal

        2:to_return_target_y. Modeled using the following behavior:
                    blackboard_reader.target_y = y_goal

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    get_mission__return_condition = True
    if get_mission__return_condition:
        to_return_target_x = x_goal
        to_return_target_y = y_goal
        return (True, to_return_target_x, to_return_target_y)
    else:
        return (False, None, None)


def get_position():
    '''
    -- RETURN
    This method is expected to return a tuple.
    The values in the tuple should be as follows:
        0: True or False. Indicates if other variables will be updated.
        Modeled using the following behavior:
            True
        1:to_return_x. Modeled using the following behavior:
                    blackboard_reader.x = x_true

        2:to_return_y. Modeled using the following behavior:
                    blackboard_reader.y = y_true

    -- SIDE EFFECTS
    This method is expected to have no side effects (for the tree).
    '''
    # below we include an auto generated attempt at implmenting this
    get_position__return_condition = True
    if get_position__return_condition:
        to_return_x = x_true
        to_return_y = y_true
        return (True, to_return_x, to_return_y)
    else:
        return (False, None, None)


def go_right():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x_true. Modeled using the following behavior:
                    x_true = min(9, (x_true + 1))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__x_true():
        global x_true
        x_true = min(9, (x_true + 1))
        return
    delayed_action_queue.append(delayed_update_for__x_true)

    return


def go_left():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:x_true. Modeled using the following behavior:
                    x_true = max(0, (x_true - 1))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__x_true():
        global x_true
        x_true = max(0, (x_true - 1))
        return
    delayed_action_queue.append(delayed_update_for__x_true)

    return


def go_up():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y_true. Modeled using the following behavior:
                    y_true = min(9, (y_true + 1))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__y_true():
        global y_true
        y_true = min(9, (y_true + 1))
        return
    delayed_action_queue.append(delayed_update_for__y_true)

    return


def go_down():
    '''
    -- RETURN
    This method does not need to return any value (though it may).
    -- SIDE EFFECTS
    This method is expected to effect the environment.
    The following changes are expected:
        1:y_true. Modeled using the following behavior:
                    y_true = max(0, (y_true - 1))

    '''
    # below we include an auto generated attempt at implmenting this
    global delayed_action_queue

    def delayed_update_for__y_true():
        global y_true
        y_true = max(0, (y_true - 1))
        return
    delayed_action_queue.append(delayed_update_for__y_true)

    return
