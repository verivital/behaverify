import sys
from draw_output import create_grid_from_states, draw_grid, draw_grid_line, create_gif


def handle_file(file_name, output_name, x_size, y_size):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = [{}]
        started = False
        for line in input_file.readlines():
            if 'State' in line:
                if len(list_of_states[-1]) != 0:
                    list_of_states.append({})
                started = True
            elif not started:
                continue
            elif 'drone_x_stage_0' in line:
                list_of_states[-1]['drone_x'] = int(line.split('=')[1].strip())
            elif 'drone_y_stage_0' in line:
                list_of_states[-1]['drone_y'] = int(line.split('=')[1].strip())
            elif 'destination_x_stage_0' in line:
                list_of_states[-1]['target_x'] = int(line.split('=')[1].strip())
            elif 'destination_y_stage_0' in line:
                list_of_states[-1]['target_y'] = int(line.split('=')[1].strip())
            elif 'node' in line:
                continue
            elif 'status' in line:
                continue
            elif 'active' in line:
                continue
            elif 'obstacles' in line:
                key = 'obstacles'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (left, right) = line.split('=')
                list_of_states[-1][key][int(left.rsplit('_', 1)[1].strip())] = int(right.strip())
            elif 'obstacle_sizes' in line:
                key = 'obstacle_sizes'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (left, right) = line.split('=')
                list_of_states[-1][key][int(left.rsplit('_', 1)[1].strip())] = int(right.strip())
        previous_states = list_of_states[0]
        index = 0
        for (index, states) in enumerate(list_of_states):
            if 'drone_x' not in states:
                states['drone_x'] = previous_states['drone_x']
            if 'drone_y' not in states:
                states['drone_y'] = previous_states['drone_y']
            if 'target_x' not in states:
                states['target_x'] = previous_states['target_x']
            if 'target_y' not in states:
                states['target_y'] = previous_states['target_y']
            if 'obstacles' not in states:
                states['obstacles'] = previous_states['obstacles']
            else:
                for internal_index in range(len(previous_states['obstacles'])):
                    if internal_index not in states['obstacles']:
                        states['obstacles'][internal_index] = previous_states['obstacles'][internal_index]
            if 'obstacle_sizes' not in states:
                states['obstacle_sizes'] = previous_states['obstacle_sizes']
            else:
                for internal_index in range(len(previous_states['obstacle_sizes'])):
                    if internal_index not in states['obstacle_sizes']:
                        states['obstacle_sizes'][internal_index] = previous_states['obstacle_sizes'][internal_index]
            draw_grid(create_grid_from_states(states, x_size, y_size), index, output_name, x_size, y_size)
            previous_states = states
        draw_grid_line(list_of_states, output_name, x_size, y_size)
        create_gif(index, output_name)
    return

#file_name, output_name, x_size, y_size
handle_file(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
