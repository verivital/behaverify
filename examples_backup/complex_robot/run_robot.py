import complex_robot
import complex_robot_environment
import os

blackboard_reader = complex_robot.create_blackboard()
environment = complex_robot_environment.complex_robot_environment(blackboard_reader)
tree = complex_robot.create_tree(environment)


def full_tick():
    tree.tick_once()
    environment.execute_delayed_action_queue()
    environment.between_tick_environment_update()
    return


def print_blackboard():
    print('blackboard:')
    print('  zone: ' + str(blackboard_reader.zone))
    print('  side: ' + str(blackboard_reader.side))
    print('  have_flag: ' + str(blackboard_reader.have_flag))
    print('  need_side_reached: ' + str(blackboard_reader.need_side_reached))
    print('  forward: ' + str(blackboard_reader.forward()))
    return


def print_environment():
    print('environment:')
    print('  x: ' + str(environment.x))
    print('  y: ' + str(environment.y))
    print('  hole_1: ' + str(environment.hole_1))
    print('  hole_2: ' + str(environment.hole_2))
    print('  hole_3: ' + str(environment.hole_3))
    print('  hole_4: ' + str(environment.hole_4))
    print('  hole_5: ' + str(environment.hole_5))
    print('  hole_6: ' + str(environment.hole_6))
    print('  hole_7: ' + str(environment.hole_7))
    print('  hole_8: ' + str(environment.hole_8))
    print('  hole_9: ' + str(environment.hole_9))
    print('  active_hole: ' + str(environment.active_hole()))
    print('  flag_x: ' + str(environment.flag_x))
    print('  flag_y: ' + str(environment.flag_y))
    print('  flag_returned: ' + str(environment.flag_returned()))
    print('  tile_progress: ' + str(environment.tile_progress))
    print('  tile_tracker: ' + str(environment.tile_tracker))
    return


holes = [environment.hole_1,
         environment.hole_2,
         environment.hole_3,
         environment.hole_4,
         environment.hole_5,
         environment.hole_6,
         environment.hole_7,
         environment.hole_8,
         environment.hole_9]


def draw_board(count):
    print('_________________________________________')
    print('iteration: ' + str(count))
    to_print = ''
    for row in range(0, 2+1):
        for col in range(0, 18+1):
            if (row == environment.y) and (col == environment.x):
                to_print += 'R'
            elif (row == environment.flag_y) and (col == environment.flag_x) and (blackboard_reader.have_flag):
                to_print += 'f'
            elif (row == environment.flag_y) and (col == environment.flag_x):
                to_print += 'F'
            elif (col < 4 or col > 12):
                to_print += '-'
            if (col >= 4 and col <= 12):
                space = '' if (col == environment.x and row == environment.y) else ' '
                if row == holes[col - 4]:
                    to_print += space + '\\'
                else:
                    to_print += space + '|'
        to_print += os.linesep
    print(to_print)
    print('_________________________________________')
    return


for count in range(100):
    # print('------------------------')
    # print('iteration: ' + str(count))
    # print_blackboard()
    # print_environment()
    draw_board(count)
    if environment.check_tick_condition():
        full_tick()
    else:
        break
