import os
import sys

def process_information(goal_loc, robot_loc, code, loc):
    return (
        '@'
        if goal_loc == robot_loc and robot_loc == loc
        else
        (
            '$'
            if robot_loc == loc
            else
            (' ' if code == 'safe' else ('X' if code == 'hole' else '?'))
        )
    )

def process_line(line):
    if len(line) < len('(Board') or  line[:len('(Board')] != '(Board':
        return ''
    goal_loc = int(line.split('envGoalLoc:')[1].split(',')[0].strip())
    robot_loc = int(line.split('envLoc:')[1].split(',')[0].strip())
    return (
        '-----------------------' + os.linesep
        + 'goal := ' + str(goal_loc) + os.linesep
        + 'robot := ' + str(robot_loc) + os.linesep
        + 'hole := ' + line.split('envHoleLoc:')[1].split(',')[0] + os.linesep
        + os.linesep
        + ('_' * 7 + os.linesep).join(
            map(
                lambda row:
                '|'.join(
                    map(
                        lambda col:
                        process_information(goal_loc, robot_loc, line.split('boardTilesIndex' + str(col + (row * 4)) + ':')[1].split(',')[0].strip().replace('"', ''), col + (row * 4))
                        , range(4)
                    )
                ) + os.linesep, range(4)
            )
        )
        + '-----------------------' + os.linesep
    )

def process_file(file_name):
    with open(file_name, 'r', encoding = 'utf-8') as read_file:
        return ''.join(map(process_line, read_file.readlines()))

print(process_file(sys.argv[1]))
