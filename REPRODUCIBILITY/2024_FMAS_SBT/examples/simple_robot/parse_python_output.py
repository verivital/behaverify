import sys
from PIL import Image, ImageDraw


COLORS = {'D': 'blue', 'T': 'gray', 'O': 'green', '-': 'white'}


def handle_file(file_name, output_name, x_size, y_size):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = []
        for line in input_file.readlines():
            if 'State' in line:
                list_of_states.append({})
            if 'x_true' in line:
                list_of_states[-1]['drone_x'] = int(line.split(':')[1].strip())
            if 'y_true' in line:
                list_of_states[-1]['drone_y'] = int(line.split(':')[1].strip())
            if 'x_goal' in line:
                list_of_states[-1]['target_x'] = int(line.split(':')[1].strip())
            if 'y_goal' in line:
                list_of_states[-1]['target_y'] = int(line.split(':')[1].strip())
        draw_grid(list_of_states, output_name, x_size, y_size)
    return

def create_grid_from_list_of_states(states, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    grid[states['drone_x']][states['drone_y']] = 'D'
    return grid

def draw_grid(list_of_states, output_name, x_size, y_size):
    tile_side = int(400 / max(x_size, y_size))
    line_size = int(tile_side/20) + 1
    size = (x_size * tile_side + 2*line_size, y_size * tile_side + 2*line_size)

    image = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(image)

    first_grid = create_grid_from_list_of_states(list_of_states[0], x_size, y_size)
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
        if current_states['drone_x'] != drone_line[-1][0] or current_states['drone_y'] != drone_line[-1][1]:
            drone_line.append((current_states['drone_x'] * tile_side + int(tile_side/2), current_states['drone_y'] * tile_side + int(tile_side/2)))
    draw.line(drone_line, fill = COLORS['D'], width = line_size)
    target_count = 0
    target = (-1, -1)
    for index in range(1, len(list_of_states)):
        current_states = list_of_states[index]
        if current_states['target_x'] != target[0] or current_states['target_y'] != target[1]:
            target_count = target_count + 1
            target = (current_states['target_x'], current_states['target_y'])
            draw.text((target[0] * tile_side + int(tile_side/2), target[1] * tile_side), str(target_count), fill = COLORS['T'], font_size = 18)
    image.save(output_name + '.png')

handle_file(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
