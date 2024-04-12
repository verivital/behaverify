import os
import sys
from generate_data import generate_sets

def in_region(point, lower_left, upper_right):
    return (
        lower_left[0] <= point[0] <= upper_right[0]
        and
        lower_left[1] <= point[1] <= upper_right[1]
    )

def create_grid(grid_size, lower_left, upper_right):
    return {x : {y : (1 if in_region((x, y), lower_left, upper_right) else 0) for y in range(grid_size)} for x in range(grid_size)}

def create_data(grid_size):
    input_lines = ['inputs = [' + os.linesep]
    target_lines = ['targets = [' + os.linesep]
    for ll_x in range(grid_size):
        for ll_y in range(grid_size):
            for ur_x in range(ll_x, grid_size):
                for ur_y in range(ll_y, grid_size):
                    grid = create_grid(grid_size, (ll_x, ll_y), (ur_x, ur_y))
                    print('----------------------------------------' + str(((ll_x, ll_y), (ur_x, ur_y))))
                    (left, right, up, down, no_action) = generate_sets(0, grid_size - 1, None, return_grid = False, grid = grid)
                    for (cur_set, cur_result) in ((left, '    [1.0, 0.0, 0.0, 0.0, 0.0]' + os.linesep),
                                               (right, '    [0.0, 1.0, 0.0, 0.0, 0.0]' + os.linesep),
                                               (up, '    [0.0, 0.0, 1.0, 0.0, 0.0]' + os.linesep),
                                               (down, '    [0.0, 0.0, 0.0, 1.0, 0.0]' + os.linesep),
                                               (no_action, '    [0.0, 0.0, 0.0, 0.0, 1.0]' + os.linesep)):
                        for (s_x, s_y, e_x, e_y) in cur_set:
                            input_lines.append('    ['
                                               + str(float(s_x)) + ', '
                                               + str(float(s_y)) + ', '
                                               + str(float(e_x)) + ', '
                                               + str(float(e_y)) + ', '
                                               + str(float(ll_x)) + ', '
                                               + str(float(ll_y)) + ', '
                                               + str(float(ur_x)) + ', '
                                               + str(float(ur_y)) +  ']' + os.linesep)
                            target_lines.append(cur_result)
    input_lines.append(']' + os.linesep)
    target_lines.append(']' + os.linesep)
    with open('ignore/noFlyInputs_' + str(grid_size) + '.py', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(input_lines)
    with open('ignore/noFlyTargets_' + str(grid_size) + '.py', 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(target_lines)


if __name__ == '__main__':
    create_data(int(sys.argv[1]))
