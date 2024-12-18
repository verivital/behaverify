import sys
from PIL import Image, ImageDraw


COLORS = {'D': 'blue', 'T': 'gray', 'O': 'green', '-': 'white'}


def handle_file(file_name, output_name, x_size, y_size):
    with open(file_name, 'r', encoding = 'utf-8') as input_file:
        list_of_states = []
        for line in input_file.readlines():
            if 'State' in line:
                list_of_states.append({})
            if 'cur_x' in line:
                list_of_states[-1]['drone_x'] = int(line.split(':')[1].strip())
            if 'cur_y' in line:
                list_of_states[-1]['drone_y'] = int(line.split(':')[1].strip())
            if 'tree_x' in line:
                list_of_states[-1]['tree_x'] = [
                    int(tree_x.strip())
                    for tree_x in line.split(':')[1].strip().replace('[', '').replace(']', '').split(',')
                ]
            if 'tree_y' in line:
                list_of_states[-1]['tree_y'] = [
                    int(tree_x.strip())
                    for tree_x in line.split(':')[1].strip().replace('[', '').replace(']', '').split(',')
                ]
            if 'tar_x' in line:
                list_of_states[-1]['target_x'] = int(line.split(':')[1].strip())
            if 'tar_y' in line:
                list_of_states[-1]['target_y'] = int(line.split(':')[1].strip())
        draw_grid_line(list_of_states, output_name, x_size, y_size)
        index = 0
        for (index, states) in enumerate(list_of_states):
            draw_grid(create_grid_from_states(states, x_size, y_size), index, output_name, x_size, y_size)
        create_gif(index, output_name)
    return

def create_grid_from_states(states, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    for tree_count in range(min(len(states['tree_x']), len(states['tree_y']))):
        grid[states['tree_x'][tree_count]][states['tree_y'][tree_count]] = 'O'
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
    target_line = [(list_of_states[0]['target_x'] * tile_side + int(tile_side/2), list_of_states[0]['target_y'] * tile_side + int(tile_side/2))]
    for index in range(1, len(list_of_states)):
        current_states = list_of_states[index]
        if current_states['drone_x'] != drone_line[-1][0] or current_states['drone_y'] != drone_line[-1][1]:
            drone_line.append((current_states['drone_x'] * tile_side + int(tile_side/2), current_states['drone_y'] * tile_side + int(tile_side/2)))
        if current_states['target_x'] != target_line[-1][0] or current_states['target_y'] != target_line[-1][1]:
            target_line.append((current_states['target_x'] * tile_side + int(tile_side/2), current_states['target_y'] * tile_side + int(tile_side/2)))
    draw.line(drone_line, fill = COLORS['D'], width = line_size)
    draw.line(target_line, fill = COLORS['T'], width = line_size)
    image.save(output_name + '_line.png')

def draw_grid(grid, index, output_name, x_size, y_size):
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
    for x in range(x_size):
        draw.line([(tile_side * x, 0), (tile_side * x, size[1])], fill = 'black', width = int(tile_side/10) + 1)
    for y in range(y_size):
        draw.line([(0, tile_side * y), (size[0], tile_side * y)], fill = 'black', width = int(tile_side/10) + 1)
    image.save(output_name + '_' + str(index) + '.png')

def create_gif(index, output_name):
    if index < 1:
        return
    frames = [Image.open(output_name + '_' + str(image) + '.png') for image in range(index)]
    frame_one = frames[0]
    frame_one.save(output_name + '_drone.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)

handle_file(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
#create_gif(122, './processed_data/pictures/counterexample_for_5/11x11')
