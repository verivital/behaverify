import sys
import os

def indent(n):
    return ' ' * (2 * n)

def handle_file(file_name, output_name):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = []
        started = False
        for line in input_file.readlines():
            if '-> State:' in line:
                list_of_states.append({})
                started = True
                continue
            if not started:
                continue
            (left_half, right_half) = line.split('=', 1)
            var_id = left_half.strip()
            var_val = right_half.strip()
            list_of_states[-1][var_id] = var_val
    with open(output_name, 'w', encoding = 'utf-8') as output_file:
        output_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>' + os.linesep,
            '<counter-example type="0" id="1" desc="LTL Counterexample">' + os.linesep
        ]
        for (index, state) in enumerate(list_of_states):
            output_lines.append(indent(1) + '<node>' + os.linesep)
            output_lines.append(indent(2) + '<state id="' + str(index + 1) + '">' + os.linesep)
            output_lines += [
                (indent(3) + '<value variable="' + var_id + '">' + state[var_id] + '</value>' + os.linesep)
                for var_id in state
            ]
            output_lines.append(indent(2) + '</state>' + os.linesep)
            output_lines.append(indent(1) + '</node>' + os.linesep)
        output_lines.append('</counter-example>' + os.linesep)
        output_file.writelines(output_lines)
    return

#file_name, output_name, x_size, y_size
handle_file(sys.argv[1], sys.argv[2])
