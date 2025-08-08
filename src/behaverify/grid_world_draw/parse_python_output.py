import sys
from draw_output import create_grid_from_states, draw_grid, draw_grid_line, create_gif

def handle_file(file_name, output_name, x_size, y_size):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = []
        started = False
        for line in input_file.readlines():
            if 'State' in line:
                list_of_states.append({})
                started = True
            elif not started:
                continue
            elif 'x_d' in line:
                list_of_states[-1]['x_d'] = int(line.split(':')[1].strip())
            elif 'y_d' in line:
                list_of_states[-1]['y_d'] = int(line.split(':')[1].strip())
            elif 'x_g' in line:
                list_of_states[-1]['x_g'] = int(line.split(':')[1].strip())
            elif 'y_g' in line:
                list_of_states[-1]['y_g'] = int(line.split(':')[1].strip())
            elif 'obstacles' in line:
                key = 'obstacles'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (_, right) = line.split(':')
                right = right.replace('[', '').replace(']', '')
                for (index, val) in enumerate(right.split(',')):
                    val = int(val.strip())
                    list_of_states[-1][key][index] = val
            elif 'obstacle_sizes' in line:
                key = 'obstacle_sizes'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (_, right) = line.split(':')
                right = right.replace('[', '').replace(']', '')
                for (index, val) in enumerate(right.split(',')):
                    val = int(val.strip())
                    list_of_states[-1][key][index] = val
        previous_states = list_of_states[0]
        if 'obstacles' not in previous_states:
            previous_states['obstacles'] = []
        if 'obstacle_sizes' not in previous_states:
            previous_states['obstacle_sizes'] = []
        index = 0
        for (index, states) in enumerate(list_of_states):
            if 'x_d' not in states:
                states['x_d'] = previous_states['x_d']
            if 'y_d' not in states:
                states['y_d'] = previous_states['y_d']
            if 'x_g' not in states:
                states['x_g'] = previous_states['x_g']
            if 'y_g' not in states:
                states['y_g'] = previous_states['y_g']
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
