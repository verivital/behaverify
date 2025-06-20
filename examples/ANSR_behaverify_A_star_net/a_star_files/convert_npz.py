import sys
import os
import math
import numpy
from misc_util import create_tail_end

def get_map_vals(file_path):
    data = numpy.load(file_path)
    print(data.__dir__())
    print(data.keys())
    print(data['data'])
    print(data['center'])
    print(data['resolution'])
    print(numpy.max(data['data']))
    print(numpy.min(data['data']))
    return data['data']


def convert_to_obstacles(map_vals, block_size, threshold, x_len = 1000, y_len = 1000):
    def new_value(x_loc, y_loc):
        cur_max = 0
        for x_mod in range(block_size):
            for y_mod in range(block_size):
                cur_max = max(cur_max, map_vals[min(x_len - 1, (x_loc * block_size) + x_mod)][min(y_len - 1, (y_loc * block_size) + y_mod)])
        return cur_max

    new_x_len = math.ceil(x_len / block_size)
    new_y_len = math.ceil(y_len / block_size)
    new_map_vals = [[new_value(cur_x, cur_y) for cur_y in range(new_y_len)] for cur_x in range(new_x_len)]

    threshold_map = { cur_x : { cur_y : (1 if new_map_vals[cur_x][cur_y] >= threshold else 0) for cur_y in range(new_y_len)} for cur_x in range(new_x_len)}
    # threshold_map stores each location as a 0 if no obstacle and 1 if obstacle
    lines_obstacles = []
    lines_sizes = []
    max_size = 0
    used = set()
    index = -1 # number_of_obstacles
    for cur_x in reversed(range(new_x_len)):
        for cur_y in reversed(range(new_y_len)):
            if (cur_x, cur_y) in used or threshold_map[cur_x][cur_y] == 0:
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
                        elif threshold_map[cur_x - x_mod][cur_y - y_mod] == 0:
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
    lines_obstacles.append('##################################################################' + os.linesep)
    lines = lines_obstacles + lines_sizes
    number_of_obstacles = index + 1
    tail_end = create_tail_end(max(new_x_len, new_y_len) - 1, threshold, number_of_obstacles, max_size)
    with open('obstacles' + tail_end + '.txt', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(lines)
    with open('map_' + str(block_size) + '_' + str(threshold) + '.txt', 'w', encoding = 'utf-8') as output_file:
        output_file.write('obstacles' + tail_end + '.txt')

if __name__ == '__main__':
    if len(sys.argv) > 4:
        convert_to_obstacles(get_map_vals(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    else:
        convert_to_obstacles(get_map_vals(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
