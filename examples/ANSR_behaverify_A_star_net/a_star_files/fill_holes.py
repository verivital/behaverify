import os
import sys
from create_grid import create_grid
from mass_basic_a_star_2 import mass_a_star
from misc_util import create_tail_end, extract_info

def fill_holes(input_path):
    (min_val, max_val, fly_at, number_of_obstacles, max_size) = extract_info(input_path)
    tail_end = create_tail_end(max_val, fly_at, number_of_obstacles, max_size)
    grid = create_grid(input_path, min_val, max_val)
    obstacles = []
    obstacle_sizes = []
    start_x = int((max_val + min_val) / 2)
    start_y = start_x
    grid_cost = mass_a_star(grid, min_val, max_val, (start_x, start_y))
    print('Computed grid from ' + str((start_x, start_y)))
    for end_x in range(min_val, max_val + 1):
        for end_y in range(min_val, max_val + 1):
            if grid_cost[end_x][end_y]['cost'] == -1:
                obstacles.append('condition {(eq, index_var, ' + str(2 * obstacle_count) + ')} assign{result{' + str(end_x) + '}}condition {(eq, index_var, ' + str((2 * obstacle_count) + 1) + ')} assign{result{' + str(end_y) + '}}' + os.linesep)
                obstacle_sizes.append('condition {(eq, index_var, ' + str(obstacle_count) + ')} assign{result{0}}' + os.linesep)
                obstacle_count = obstacle_count + 1
    new_tail_end = create_tail_end(max_val, fly_at, obstacle_count, 0)
    if new_tail_end != tail_end:
        with open(input_path.replace(tail_end, new_tail_end), 'w', encoding = 'utf-8') as output_file:
            output_file.writelines(obstacles + ['##################################################################' + os.linesep] + obstacle_sizes)
    return

if __name__ == '__main__':
    fill_holes(sys.argv[1])
