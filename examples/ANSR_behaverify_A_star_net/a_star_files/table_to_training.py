import re
import os
import sys

def convert_table_to_training_data(input_path, output_path_input, output_path_target):
    input_lines = ['inputs = [' + os.linesep]
    target_lines = ['targets = [' + os.linesep]
    target_code = {
        'left': '[1.0, 0.0, 0.0, 0.0, 0.0]',
        'right' : '[0.0, 1.0, 0.0, 0.0, 0.0]',
        'up' : '[0.0, 0.0, 1.0, 0.0, 0.0]',
        'down' : '[0.0, 0.0, 0.0, 1.0, 0.0]',
        'no_action' : '[0.0, 0.0, 0.0, 0.0, 1.0]'
    }
    all_min_vals = [None, None, None, None]
    all_max_vals = [None, None, None, None]
    input_code = {
        'drone_x' : 0,
        'drone_y' : 1,
        'destination_x' : 2,
        'destination_y' : 3
    }
    cleanse_string = r'[()\{\}]|(case)|(and)'
    seen_values = set()
    with open(input_path, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if 'case' not in line:
                continue
            min_vals = [None, None, None, None]
            max_vals = [None, None, None, None]
            (case, result) = re.sub(cleanse_string, '', line).split('result', 1)
            result = target_code[result.replace("'", '').strip()]
            case = case.replace(',', '', 1).strip()
            split_case = case.split(',')
            index = 0
            while index < len(split_case):
                if split_case[index].strip() == 'eq':
                    cur_code = input_code[split_case[index + 1].strip()]
                    cur_val = int(split_case[index + 2].strip())
                    min_vals[cur_code] = cur_val
                    max_vals[cur_code] = cur_val
                    index = index + 3
                    continue
                cur_code = input_code[split_case[index + 2].strip()]
                min_vals[cur_code] = int(split_case[index + 1].strip())
                max_vals[cur_code] = int(split_case[index + 5].strip())
                index = index + 6
                continue
            for index in range(4):
                all_min_vals[index] = min_vals[index] if all_min_vals[index] is None else min(all_min_vals[index], min_vals[index])
                all_max_vals[index] = max_vals[index] if all_max_vals[index] is None else max(all_max_vals[index], max_vals[index])
            for s_x in range(min_vals[0], max_vals[0] + 1):
                for s_y in range(min_vals[1], max_vals[1] + 1):
                    for e_x in range(min_vals[2], max_vals[2] + 1):
                        for e_y in range(min_vals[3], max_vals[3] + 1):
                            seen_values.add((s_x, s_y, e_x, e_y))
                            input_lines.append('    ['+ str(float(s_x)) + ', ' + str(float(s_y)) + ', ' + str(float(e_x)) + ', ' + str(float(e_y)) + '],' + os.linesep)
                            target_lines.append('    ' + result + ',' + os.linesep)
                            if len(seen_values) % 1000 == 0:
                                print('iteration: ' + str(len(seen_values)))
    result = target_code['no_action']
    for s_x in range(all_min_vals[0], all_max_vals[0] + 1):
        for s_y in range(all_min_vals[1], all_max_vals[1] + 1):
            for e_x in range(all_min_vals[2], all_max_vals[2] + 1):
                for e_y in range(all_min_vals[3], all_max_vals[3] + 1):
                    if (s_x, s_y, e_x, e_y) not in seen_values:
                        input_lines.append('    ['+ str(float(s_x)) + ', ' + str(float(s_y)) + ', ' + str(float(e_x)) + ', ' + str(float(e_y)) + '],' + os.linesep)
                        target_lines.append('    ' + result + ',' + os.linesep)
    input_lines.append(']' + os.linesep)
    target_lines.append(']' + os.linesep)
    with open(output_path_input, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(input_lines)
    with open(output_path_target, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(target_lines)

if __name__ == '__main__':
    convert_table_to_training_data(sys.argv[1], sys.argv[2], sys.argv[3])
