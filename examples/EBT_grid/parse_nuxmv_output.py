import sys
from PIL import Image, ImageDraw


COLORS = {'D': 'blue', 'T': 'green', 'O': 'black', '-': 'white', 'L' : 'purple'}


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
            elif 'drone_x_stage_0' in line:
                list_of_states[-1]['drone_x'] = int(line.split('=')[1].strip())
            elif 'drone_y_stage_0' in line:
                list_of_states[-1]['drone_y'] = int(line.split('=')[1].strip())
            elif 'waypoint_x_stage_0' in line:
                list_of_states[-1]['target_x'] = int(line.split('=')[1].strip())
            elif 'waypoint_y_stage_0' in line:
                list_of_states[-1]['target_y'] = int(line.split('=')[1].strip())
            elif 'landmark_index_stage_0' in line:
                list_of_states[-1]['landmark_index'] = int(line.split('=')[1].strip())
            elif 'landmark_index_stage_1' in line:
                continue
            elif 'node' in line:
                continue
            elif 'status' in line:
                continue
            elif 'active' in line:
                continue
            elif 'current_landmark' in line:
                continue
            elif 'landmark' in line:
                key = 'landmark'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (left, right) = line.split('=')
                list_of_states[-1][key][int(left.rsplit('_', 1)[1].strip())] = int(right.strip())
            elif 'obstacles_sort_x' in line:
                key = 'obstacles'
                if key not in list_of_states[-1]:
                    list_of_states[-1][key] = {}
                (left, right) = line.split('=')
                list_of_states[-1][key][int(left.rsplit('_', 1)[1].strip())] = int(right.strip())
        draw_grid_line(list_of_states, output_name, x_size, y_size)
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
            if 'landmark_index' not in states:
                states['landmark_index'] = previous_states['landmark_index']
            if 'landmark' not in states:
                states['landmark'] = previous_states['landmark']
            else:
                for internal_index in range(len(previous_states['landmark'])):
                    if internal_index not in states['landmark']:
                        states['landmark'][internal_index] = previous_states['landmark'][internal_index]
            if 'obstacles' not in states:
                states['obstacles'] = previous_states['obstacles']
            else:
                for internal_index in range(len(previous_states['obstacles'])):
                    if internal_index not in states['obstacles']:
                        states['obstacles'][internal_index] = previous_states['obstacles'][internal_index]
            draw_grid(create_grid_from_states(states, x_size, y_size), (states['landmark'][states['landmark_index'] * 2], states['landmark'][(states['landmark_index'] * 2) + 1], states['landmark_index']), index, output_name, x_size, y_size)
            previous_states = states
        create_gif(index, output_name)
    return

def create_grid_from_states(states, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    for index in range(len(states['obstacles']) // 2):
        grid[states['obstacles'][2 * index]][states['obstacles'][(2 * index) + 1]] = 'O'
    grid[states['target_x']][states['target_y']] = 'T'
    grid[states['drone_x']][states['drone_y']] = 'D'
    return grid

def draw_grid_line(list_of_states, output_name, x_size, y_size):
    tile_side = int(400 / max(x_size, y_size))
    line_size = int(tile_side/20) + 1
    size = (x_size * tile_side + 2*line_size, y_size * tile_side + 2*line_size)

    image = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(image)

    first_grid = create_grid_from_states(list_of_states[0], x_size, y_size)
    for x in range(x_size):
        for y in range(y_size):
            cell_value = first_grid[x][y]
            draw.rectangle([(x * tile_side, y * tile_side), ((x + 1) * tile_side, (y + 1) * tile_side)], fill=COLORS[cell_value])
    for x in range(x_size + 1):
        draw.line([(tile_side * x, 0), (tile_side * x, size[1])], fill = 'black', width = line_size)
        draw.line([(tile_side * x + line_size, 0), (tile_side * x + line_size, size[1])], fill = 'black', width = line_size)
    for y in range(y_size + 1):
        draw.line([(0, tile_side * y), (size[0], tile_side * y)], fill = 'black', width = line_size)
        draw.line([(0, tile_side * y + line_size), (size[0], tile_side * y + line_size)], fill = 'black', width = line_size)
    drone_line = [(list_of_states[0]['drone_x'] * tile_side + int(tile_side/2), list_of_states[0]['drone_y'] * tile_side + int(tile_side/2))]
    for index in range(1, len(list_of_states)):
        current_states = list_of_states[index]
        if 'drone_x' in current_states or 'drone_y' in current_states:
            drone_line.append(
                ((current_states['drone_x'] * tile_side + int(tile_side/2)) if 'drone_x' in current_states else drone_line[-1][0],
                 (current_states['drone_y'] * tile_side + int(tile_side/2)) if 'drone_y' in current_states else drone_line[-1][1])
            )
    draw.line(drone_line, fill = COLORS['D'], width = line_size)
    for index in range(len(list_of_states[0]['landmark']) // 2):
        landmark = (list_of_states[0]['landmark'][index * 2], list_of_states[0]['landmark'][(2 * index) + 1])
        draw.text((landmark[0] * tile_side + int(tile_side/2), landmark[1] * tile_side), str(index + 1), fill = COLORS['L'], font_size = 18)
    image.save(output_name + '_line.png')

def draw_grid(grid, landmark, index, output_name, x_size, y_size):
    (landmark_x, landmark_y, landmark_index) = landmark
    tile_side = int(400 / max(x_size, y_size))
    line_size = int(tile_side/20) + 1
    size = (x_size * tile_side + 2*line_size, y_size * tile_side + 2*line_size)

    image = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(image)

    for x in range(x_size):
        for y in range(y_size):
            cell_value = grid[x][y]
            draw.rectangle([(x * tile_side, y * tile_side), ((x + 1) * tile_side, (y + 1) * tile_side)], fill=COLORS[cell_value])
    for x in range(x_size + 1):
        draw.line([(tile_side * x, 0), (tile_side * x, size[1])], fill = 'black', width = line_size)
        draw.line([(tile_side * x + line_size, 0), (tile_side * x + line_size, size[1])], fill = 'black', width = line_size)
    for y in range(y_size + 1):
        draw.line([(0, tile_side * y), (size[0], tile_side * y)], fill = 'black', width = line_size)
        draw.line([(0, tile_side * y + line_size), (size[0], tile_side * y + line_size)], fill = 'black', width = line_size)
    draw.text((landmark_x * tile_side + int(tile_side/2), landmark_y * tile_side), str(landmark_index), fill = COLORS['L'], font_size = 18)
    image.save(output_name + '_' + str(index) + '.png')

def create_gif(index, output_name):
    if index < 1:
        return
    frames = [Image.open(output_name + '_' + str(image) + '.png') for image in range(index)]
    frame_one = frames[0]
    frame_one.save(output_name + '_animate.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)

#file_name, output_name, x_size, y_size
handle_file(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
