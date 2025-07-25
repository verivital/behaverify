import re
import os
import sys
from misc_util import extract_info

def convert_table_to_training_data(input_path):
    (min_val, max_val, _, _, _) = extract_info(input_path)
    min_x = min_val
    min_y = min_val
    max_x = max_val
    max_y = max_val
    output_path_input = input_path.replace('table', 'inputs').replace('.txt', '.py')
    output_path_target = input_path.replace('table', 'targets').replace('.txt', '.py')
    print(output_path_input)
    print(output_path_target)

    input_lines = ['inputs = [' + os.linesep]
    target_lines = ['targets = [' + os.linesep]
    target_code = {
        'We': '[1.0, 0.0, 0.0, 0.0, 0.0]',
        'Ea' : '[0.0, 1.0, 0.0, 0.0, 0.0]',
        'No' : '[0.0, 0.0, 1.0, 0.0, 0.0]',
        'So' : '[0.0, 0.0, 0.0, 1.0, 0.0]',
        'XX' : '[0.0, 0.0, 0.0, 0.0, 1.0]'
    }
    # all_min_vals = [None, None, None, None]
    # all_max_vals = [None, None, None, None]
    input_code = {
        'x_d' : 0,
        'y_d' : 1,
        'x_g' : 2,
        'y_g' : 3
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
            # for index in range(4):
            #     all_min_vals[index] = min_vals[index] if all_min_vals[index] is None else min(all_min_vals[index], min_vals[index])
            #     all_max_vals[index] = max_vals[index] if all_max_vals[index] is None else max(all_max_vals[index], max_vals[index])
            for s_x in range(min_vals[0], max_vals[0] + 1):
                for s_y in range(min_vals[1], max_vals[1] + 1):
                    for e_x in range(min_vals[2], max_vals[2] + 1):
                        for e_y in range(min_vals[3], max_vals[3] + 1):
                            seen_values.add((s_x, s_y, e_x, e_y))
                            input_lines.append('    ['+ str(float(s_x)) + ', ' + str(float(s_y)) + ', ' + str(float(e_x)) + ', ' + str(float(e_y)) + '],' + os.linesep)
                            target_lines.append('    ' + result + ',' + os.linesep)
                            # if len(seen_values) % 1000 == 0:
                            #     print('iteration: ' + str(len(seen_values)))
    print(len(seen_values))
    result = target_code['XX']
    # for s_x in range(all_min_vals[0], all_max_vals[0] + 1):
    #     for s_y in range(all_min_vals[1], all_max_vals[1] + 1):
    #         for e_x in range(all_min_vals[2], all_max_vals[2] + 1):
    #             for e_y in range(all_min_vals[3], all_max_vals[3] + 1):
    for s_x in range(min_x, max_x + 1):
        for s_y in range(min_y, max_y + 1):
            for e_x in range(min_x, max_x + 1):
                for e_y in range(min_y, max_y + 1):
                    if (s_x, s_y, e_x, e_y) not in seen_values:
                        seen_values.add((s_x, s_y, e_x, e_y))
                        input_lines.append('    ['+ str(float(s_x)) + ', ' + str(float(s_y)) + ', ' + str(float(e_x)) + ', ' + str(float(e_y)) + '],' + os.linesep)
                        target_lines.append('    ' + result + ',' + os.linesep)
    print(len(seen_values))
    input_lines.append(']' + os.linesep)
    target_lines.append(']' + os.linesep)
    with open(output_path_input, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(input_lines)
    with open(output_path_target, 'w', encoding = 'utf-8') as output_file:
        output_file.writelines(target_lines)

if __name__ == '__main__':
    convert_table_to_training_data(sys.argv[1])
