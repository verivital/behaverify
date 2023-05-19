import os
import robot
import create_tree

robot_tree = create_tree.create_tree()

count = 0


def draw_board():
    print('_________________________________________')
    print('iteration: ' + str(count))
    to_print = ''
    for row in range(0, 2+1):
        for col in range(0, 18+1):
            if (row == robot.y_true) and (col == robot.x_true):
                to_print += 'R'
            elif (row == robot.y_goal) and (col == robot.x_goal) and (robot.remaining_goals > 0):
                to_print += 'F'
            else:
                to_print += '-'
        to_print += os.linesep
    print(to_print)
    print('_________________________________________')
    return


while (count < 50):
    count = count + 1
    robot_tree.tick_once()
    robot.execute_delayed_action_queue()
    robot.between_tick_environment_update()
    draw_board()
