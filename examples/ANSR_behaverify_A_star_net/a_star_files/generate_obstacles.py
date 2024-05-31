import sys
import random
import os
from misc_util import create_tail_end, handle_path
START_LOC = 'mid'

def generate_obstacles(number_of_obstacles, min_val, max_val, max_size):
    lines = []
    for index in range(number_of_obstacles):
        x_val = random.randint(min_val, max_val)
        y_val = random.randint(min_val, max_val)
        if START_LOC == 'top':
            while x_val == max_val and y_val == max_val:
                x_val = random.randint(min_val, max_val)
                y_val = random.randint(min_val, max_val)
        if START_LOC == 'mid':
            mid_val = (max_val + min_val) // 2
            while ((x_val - max_size) <= mid_val <= x_val) and ((y_val - max_size) <= mid_val <= y_val):
                x_val = random.randint(min_val, max_val)
                y_val = random.randint(min_val, max_val)
        lines.append('condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}'
                     + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(random.randint(min_val, max_val)) + '}}' + os.linesep)
    lines.append('##################################################################' + os.linesep)
    for index in range(number_of_obstacles):
        lines.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{' + str(random.randint(0, max_size)) + '}}' + os.linesep)
    tail_end = create_tail_end(max_val, None, number_of_obstacles, max_size)
    with open(handle_path('ignore/obstacles' + tail_end + '.txt'), 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)

def generate_set_obstacles(meta_dim):
    lines = []
    number_of_obstacles = 8 * meta_dim * meta_dim
    max_val = (meta_dim * 5) - 1
    max_size = 0
    index = 0
    pairs = (
        (0, 1),
        (0, 3),
        (1, 1),
        (2, 4),
        (3, 0),
        (3, 3),
        (4, 1),
        (4, 3)
    )
    for meta_x in range(meta_dim):
        for meta_y in range(meta_dim):
            x_base = meta_x * 5
            y_base = meta_y * 5
            for (x_mod, y_mod) in pairs:
                x_val = x_base + x_mod
                y_val = y_base + y_mod
                lines.append('condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(x_val) + '}}'
                             + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(y_val) + '}}' + os.linesep)
                index = index + 1
    lines.append('##################################################################' + os.linesep)
    for index in range(number_of_obstacles):
        lines.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{0}}' + os.linesep)
    tail_end = create_tail_end(max_val, None, number_of_obstacles, max_size)
    with open(handle_path('ignore/obstacles' + tail_end + '.txt'), 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        generate_set_obstacles(int(sys.argv[1]))
    else:
        generate_obstacles(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
