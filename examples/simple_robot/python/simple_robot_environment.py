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

remaining_goals = random.choice([1, 2, 3])
# this variable develops in the following way between ticks.
#         if ((x_goal == x_true) and (y_goal == y_true)):
#             remaining_goals = max(0, (remaining_goals - 1))
#         else:
#             remaining_goals = remaining_goals
#


def get_mission_func__condition(node):
    return True


def get_mission_func__0(node):
    to_return_target_x = x_goal
    return to_return_target_x


def get_mission_func__1(node):
    to_return_target_y = y_goal
    return to_return_target_y


def get_position_func__condition(node):
    return True


def get_position_func__0(node):
    to_return_x = x_true
    return to_return_x


def get_position_func__1(node):
    to_return_y = y_true
    return to_return_y


def go_right_func__0(node):
    global x_true
    update_val_x_true = min(9, (x_true + 1))
    x_true = serene_safe_assignment.x_true(update_val_x_true)
    return


def go_left_func__0(node):
    global x_true
    update_val_x_true = max(0, (x_true - 1))
    x_true = serene_safe_assignment.x_true(update_val_x_true)
    return


def go_up_func__0(node):
    global y_true
    update_val_y_true = min(9, (y_true + 1))
    y_true = serene_safe_assignment.y_true(update_val_y_true)
    return


def go_down_func__0(node):
    global y_true
    update_val_y_true = max(0, (y_true - 1))
    y_true = serene_safe_assignment.y_true(update_val_y_true)
    return
