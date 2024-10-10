import sys
import os

MAX_VAL = int(sys.argv[1])
INPUT_FILE = sys.argv[2]
OUTPUT_FILE_C = sys.argv[3]
OUTPUT_FILE_H = sys.argv[4]

def create_file():
    with open(INPUT_FILE, 'r', encoding = 'utf-8') as in_file:
        obstacles = {}
        obstacle_sizes = {}
        obstacle_query = {(x_val, y_val) : False for x_val in range(MAX_VAL + 1) for y_val in range(MAX_VAL + 1)}
        for line in in_file.readlines():
            if 'self.obstacles[' in line:
                (left, right) = line.split('=', 1)
                left = left.split('[', 1)[1]
                left = left.split(']', 1)[0]
                index = int(left.strip())
                value = int(right.strip())
                obstacles[index] = value
            elif 'self.obstacle_sizes[' in line:
                (left, right) = line.split('=', 1)
                left = left.split('[', 1)[1]
                left = left.split(']', 1)[0]
                index = int(left.strip())
                value = int(right.strip())
                obstacle_sizes[index] = value
        for index in range(len(obstacle_sizes)):
            x_base = obstacles[2 * index]
            y_base = obstacles[(2 * index) + 1]
            size = obstacle_sizes[index]
            for x_mod in range(size + 1):
                for y_mod in range(size + 1):
                    obstacle_query[(max(0, x_base - x_mod), max(0, y_base - y_mod))] = True
    with open(OUTPUT_FILE_C, 'w', encoding = 'utf-8') as out_file:
        out_file.write(
            'int OBSTACLES[] = {' + ', '.join([str(obstacles[index]) for index in range(len(obstacles))]) + '};' + os.linesep
            + 'int OBSTACLE_SIZES[] = {' + ', '.join([str(obstacle_sizes[index]) for index in range(len(obstacle_sizes))]) + '};' + os.linesep
            + '_Bool OBSTACLE_QUERY[][' + str(MAX_VAL + 1) + '] = {'
            + ', '.join(
                [
                    ('{' + ', '.join([('1' if obstacle_query[(x_val, y_val)] else '0') for y_val in range(MAX_VAL + 1)]) + '}')
                    for x_val in range(MAX_VAL + 1)
                ]
            )
            + '};' + os.linesep
        )
    with open(OUTPUT_FILE_H, 'w', encoding = 'utf-8') as out_file:
        out_file.write(
            'extern int OBSTACLES[];' + os.linesep
            + 'extern int OBSTACLE_SIZES[];' + os.linesep
            + 'extern _Bool OBSTACLE_QUERY[][' + str(MAX_VAL + 1) + '];' + os.linesep
        )

create_file()
