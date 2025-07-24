import sys
from draw_SIMPLE_output import create_grid_from_states, draw_grid, draw_grid_line, create_gif


def handle_file(file_name, output_name, x_size, y_size):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = [{}]
        started = False
        vals = {}
        for line in input_file.readlines():
            if 'State' in line:
                vals = {'x_d' : -1, 'y_d' : -1, 'x_g' : -1, 'y_g' : -1}
                if len(list_of_states[-1]) != 0:
                    list_of_states.append({})
                started = True
            elif not started:
                continue
            elif 'x_d_stage_' in line:
                stage_num = int(((line.split('=')[0]).split('_')[-1]).strip())
                if vals['x_d'] < stage_num:
                    list_of_states[-1]['x_d'] = int(line.split('=')[1].strip())
                    vals['x_d'] = stage_num
            elif 'y_d_stage_' in line:
                stage_num = int(((line.split('=')[0]).split('_')[-1]).strip())
                if vals['y_d'] < stage_num:
                    list_of_states[-1]['y_d'] = int(line.split('=')[1].strip())
                    vals['y_d'] = stage_num
            elif 'x_g_stage_' in line:
                stage_num = int(((line.split('=')[0]).split('_')[-1]).strip())
                if vals['x_g'] < stage_num:
                    list_of_states[-1]['x_g'] = int(line.split('=')[1].strip())
                    vals['x_g'] = stage_num
            elif 'y_g_stage_' in line:
                stage_num = int(((line.split('=')[0]).split('_')[-1]).strip())
                if vals['y_g'] < stage_num:
                    list_of_states[-1]['y_g'] = int(line.split('=')[1].strip())
                    vals['y_g'] = stage_num
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
