import re
import os
import sys
from misc_util import extract_info
from generate_data import generate_sets

def convert_table_to_training_data(input_path):
    (min_val, max_val, _, _, _) = extract_info(input_path)
    min_x = min_val
    min_y = min_val
    max_x = max_val
    max_y = max_val
    output_path_input = input_path.replace('obstacle', 'inputsSmall').replace('.txt', '.py')
    output_path_target = input_path.replace('obstacle', 'targetsSmall').replace('.txt', '.py')
    (left, right, up, down, no_action, grid) = generate_sets(min_val, max_val, input_path, return_grid = True)

    input_lines = ['inputs = [' + os.linesep]
    target_lines = ['targets = [' + os.linesep]
    set_associations = (
        (left, '[1.0, 0.0, 0.0, 0.0, 0.0]'),
        (right, '[0.0, 1.0, 0.0, 0.0, 0.0]'),
        (up, '[0.0, 0.0, 1.0, 0.0, 0.0]'),
        (down, '[0.0, 0.0, 0.0, 1.0, 0.0]'),
        (no_action, '[0.0, 0.0, 0.0, 0.0, 1.0]')
    )
    training_size = 0
    for s_x in range(min_val, max_val + 1):
        for s_y in range(min_val, max_val + 1):
            if grid[s_x][s_y] == 1:
                continue # don't create training date for when the drone is inside an obstacle. Who cares after all.
            for e_x in range(min_val, max_val + 1):
                for e_y in range(min_val, max_val + 1):
                    found_set = False
                    for (cur_set, result) in set_associations:
                        if ((s_x, s_y), (e_x, e_y)) in cur_set:
                            input_lines.append('    ['+ str(float(s_x)) + ', ' + str(float(s_y)) + ', ' + str(float(e_x)) + ', ' + str(float(e_y)) + '],' + os.linesep)
                            target_lines.append('    ' + result + ',' + os.linesep)
                            found_set = True
                            break
                    training_size = training_size + 1
                    if not found_set:
                        print(((s_x, s_y), (e_x, e_y)))
                        raise RuntimeError('Tuple not member of any set')
    input_lines.append(']' + os.linesep)
    target_lines.append(']' + os.linesep)
    print(training_size)
    print((max_val + 1 - min_val) ** 4)
    with open(output_path_input, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(input_lines)
    with open(output_path_target, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(target_lines)

if __name__ == '__main__':
    convert_table_to_training_data(sys.argv[1])
