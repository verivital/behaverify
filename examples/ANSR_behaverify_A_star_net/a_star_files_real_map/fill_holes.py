import os
import sys
from create_grid import create_grid
from mass_basic_a_star_2 import mass_a_star

def fill_holes(input_path, output_folder):
    min_val = 0
    max_val_ = input_path.split('/')[-1].split('_')[1]
    max_val = int(max_val_)
    fly_at = input_path.split('/')[-1].split('_')[2]
    grid = create_grid(input_path, min_val, max_val)
    obstacle_count = 0
    obstacles = []
    obstacle_sizes = []
    start_x = (max_val + min_val) // 2
    start_y = start_x
    grid_cost = mass_a_star(grid, min_val, max_val, (start_x, start_y))
    print('Computed grid from ' + str((start_x, start_y)))
    for end_x in range(min_val, max_val + 1):
        for end_y in range(min_val, max_val + 1):
            if grid_cost[end_x][end_y]['cost'] == -1:
                obstacles.append('condition {(eq, index_var, ' + str(2 * obstacle_count) + ')} assign{result{' + str(end_x) + '}}condition {(eq, index_var, ' + str((2 * obstacle_count) + 1) + ')} assign{result{' + str(end_y) + '}}' + os.linesep)
                obstacle_sizes.append('condition {(eq, index_var, ' + str(obstacle_count) + ')} assign{result{0}}' + os.linesep)
                obstacle_count = obstacle_count + 1
    with open(output_folder + '/obstacles_' + max_val_ + '_' + fly_at + '_' + str(obstacle_count) + '_0.txt', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(obstacles + ['##################################################################' + os.linesep] + obstacle_sizes)
    return

if __name__ == '__main__':
    fill_holes(sys.argv[1], sys.argv[2])
