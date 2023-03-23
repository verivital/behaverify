import simple_robot
import robot
import os

tree = simple_robot.create_tree()
count = 3
ticks_completed = 0
while count > 0:
    tree.tick_once()
    ticks_completed = ticks_completed + 1
    print('----------------------------------------------')
    print(ticks_completed)
    board_string = ''
    for x in range(5):
        for y in range(5):
            if robot.state['x'] == x and robot.state['y'] == y:
                board_string += 'R'
            elif robot.state['target_x'] == x and robot.state['target_y'] == y:
                board_string += 'T'
            else:
                board_string += '_'
        board_string += os.linesep
    print(board_string)
    print(robot.state['missions_remaining'])
    print('----------------------------------------------')
    if robot.state['missions_remaining'] == 0:
        count = count - 1
