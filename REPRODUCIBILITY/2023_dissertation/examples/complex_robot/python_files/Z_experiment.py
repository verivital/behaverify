import os
import complex_robot
import complex_robot_environment

robot = complex_robot.create_tree()

count = 0

holes = [complex_robot_environment.hole_1,
         complex_robot_environment.hole_2,
         complex_robot_environment.hole_3,
         complex_robot_environment.hole_4,
         complex_robot_environment.hole_5,
         complex_robot_environment.hole_6,
         complex_robot_environment.hole_7,
         complex_robot_environment.hole_8,
         complex_robot_environment.hole_9]


def draw_board():
    print('_________________________________________')
    print('iteration: ' + str(count))
    to_print = ''
    for row in range(0, 2+1):
        for col in range(0, 18+1):
            if (row == complex_robot_environment.y) and (col == complex_robot_environment.x):
                to_print += 'R'
            elif (row == complex_robot_environment.flag_y) and (col == complex_robot_environment.flag_x) and (complex_robot_environment.blackboard_reader.have_flag):
                to_print += 'f'
            elif (row == complex_robot_environment.flag_y) and (col == complex_robot_environment.flag_x):
                to_print += 'F'
            elif (col < 4 or col > 12):
                to_print += '-'
            if (col >= 4 and col <= 12):
                space = '' if (col == complex_robot_environment.x and row == complex_robot_environment.y) else ' '
                if row == holes[col - 4]:
                    to_print += space + '\\'
                else:
                    to_print += space + '|'
        to_print += os.linesep
    print(to_print)
    print('_________________________________________')
    return


while (count < 300):
    count = count + 1
    robot.tick_once()
    complex_robot_environment.execute_delayed_action_queue()
    complex_robot_environment.between_tick_environment_update()
    draw_board()
    if complex_robot_environment.flag_returned():
        break
