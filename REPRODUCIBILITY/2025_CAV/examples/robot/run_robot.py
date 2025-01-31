import os
import robot_environment
import robot

simple_robot_tree = robot.create_tree()

# import py_trees

# py_trees.display.render_dot_tree(simple_robot_tree, with_blackboard_variables = True)
# py_trees.display.render_dot_tree(simple_robot_tree)

count = 0


def draw_board():
    print('_________________________________________')
    print('iteration: ' + str(count))
    to_print = ''
    for row in range(0, 10):
        for col in range(0, 10):
            if (row == simple_robot_environment.y_true) and (col == simple_robot_environment.x_true):
                to_print += 'R'
            elif (row == simple_robot_environment.y_goal) and (col == simple_robot_environment.x_goal) and (simple_robot_environment.remaining_goals > 0):
                to_print += 'F'
            else:
                to_print += '-'
        to_print += os.linesep
    print(to_print)
    print('goals left: ' + str(simple_robot_environment.remaining_goals))
    print('_________________________________________')
    return


break_count = 3
while (count < 50 and break_count > 0):
    count = count + 1
    robot_tree.tick_once()
    robot_environment.execute_delayed_action_queue()
    robot_environment.between_tick_environment_update()
    draw_board()
    if simple_robot_environment.remaining_goals == 0:
        break_count = break_count - 1
