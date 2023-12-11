import sys
from PIL import Image, ImageDraw


COLORS = {'D': 'blue', 'T': 'yellow', 'O': 'green', '-': 'white'}


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
        index = 0
        for (index, states) in enumerate(list_of_states):
            draw_grid(create_grid_from_states(states, x_size, y_size), index, output_name, x_size, y_size)
        create_gif(index, output_name)
    return

def create_grid_from_states(states, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    for tree_count in range(min(len(states['tree_x']), len(states['tree_y']))):
        grid[states['tree_y'][tree_count]][states['tree_x'][tree_count]] = 'O'
    grid[states['target_y']][states['target_x']] = 'T'
    grid[states['drone_y']][states['drone_x']] = 'D'
    return grid

def draw_grid(grid, index, output_name, x_size, y_size):
    tile_side = int(400 / max(x_size, y_size))
    line_size = int(tile_side/20) + 1
    size = (x_size * tile_side + 2*line_size, y_size * tile_side + 2*line_size)
    image = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(image)
    for y in range(y_size):
        for x in range(x_size):
            cell_value = grid[y][x]
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
