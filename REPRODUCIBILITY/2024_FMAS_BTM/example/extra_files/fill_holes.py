import os
import sys
from create_grid import create_grid
from mass_basic_a_star_2 import mass_a_star
from misc_util import create_tail_end, extract_info

def fill_holes(input_path):
    (min_val, max_val, fly_at, number_of_obstacles, max_size) = extract_info(input_path)
    tail_end = create_tail_end(max_val, fly_at, number_of_obstacles, max_size)
    grid = create_grid(input_path, min_val, max_val)
    start_x = int((max_val + min_val) / 2)
    start_y = start_x
    grid_cost = mass_a_star(grid, min_val, max_val, (start_x, start_y))
    print('Computed grid from ' + str((start_x, start_y)))
    new_grid = {x : {y : 0 for y in range(min_val, max_val + 1)} for x in range(min_val, max_val + 1)}
    for end_x in range(min_val, max_val + 1):
        for end_y in range(min_val, max_val + 1):
            if grid_cost[end_x][end_y]['cost'] == -1:
                new_grid[end_x][end_y] = 1
    lines_obstacles = []
    lines_sizes = []
    max_size = 0
    used = set()
    index = -1 #start at -1
    for cur_x in reversed(range(max_val + 1)):
        for cur_y in reversed(range(max_val + 1)):
            if (cur_x, cur_y) in used or new_grid[cur_x][cur_y] == 0:
                # if we already added this point, skip it
                # if this point doesn't have an obstacle, skip it
                continue
            index = index + 1 # keep track of where we are.
            cur_size = 0  # how big can we make this obstacle?
            done = False
            while not done:
                next_size = cur_size + 1 # try and make the obstacle one bigger
                for x_mod in range(next_size + 1): #shift by 1 because size 0 means just the cell.
                    for y_mod in range(next_size + 1):
                        # for each x and y in the relevant range, check that
                        # 1. we didn't go out of bounds
                        # 2. we didn't find a tile that wasn't an obstacle.
                        if cur_x - x_mod < 0 or cur_y - y_mod < 0:
                            done = True
                        elif new_grid[cur_x - x_mod][cur_y - y_mod] == 0:
                            done = True
                if not done:
                    # since we didn't find any errors, we update the size.
                    cur_size = next_size
            for x_mod in range(cur_size + 1):
                for y_mod in range(cur_size + 1):
                    # mark each used tile as used.
                    used.add((cur_x - x_mod, cur_y - y_mod))
            max_size = max(max_size, cur_size) # update our size tracker.
            lines_obstacles.append('condition {(eq, index_var, ' + str(2 * index) + ')} assign{result{' + str(cur_x) + '}}'
                                   + 'condition {(eq, index_var, ' + str((2 * index) + 1) + ')} assign{result{' + str(cur_y) + '}}' + os.linesep)
            lines_sizes.append('condition {(eq, index_var, ' + str(index) + ')} assign{result{' + str(cur_size) + '}}' + os.linesep)
    number_of_obstacles = index + 1
    if number_of_obstacles == 1:
        lines_obstacles.append(lines_obstacles[0])
        lines_sizes.append(lines_sizes[0])
        number_of_obstacles += 1
    new_tail_end = create_tail_end(max_val, fly_at, number_of_obstacles, max_size)
    new_tail_end = 'Filled' + new_tail_end
    if tail_end in input_path:
        (left, right) = input_path.rsplit(tail_end, 1)
        output_path = left + new_tail_end + right
        with open(output_path, 'w', encoding = 'utf-8') as output_file:
            output_file.writelines(lines_obstacles + ['##################################################################' + os.linesep] + lines_sizes)
        return
    print('Check input file name: could not replace tail end. Not writing.')
    return

if __name__ == '__main__':
    fill_holes(sys.argv[1])
