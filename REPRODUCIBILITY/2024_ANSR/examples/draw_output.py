from PIL import Image, ImageDraw

COLORS = {'D': 'blue', 'T': 'green', 'O': 'black', '-': 'white', 'L' : 'purple'}

def create_grid_from_states(states, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    for index in range(len(states['obstacles']) // 2):
        obstacle_size = states['obstacle_sizes'][index] + 1
        x_loc = states['obstacles'][2 * index]
        y_loc = states['obstacles'][(2 * index) + 1]
        for sub_index_x in range(obstacle_size):
            for sub_index_y in range(obstacle_size):
                grid[max(0, x_loc - sub_index_x)][max(0, y_loc - sub_index_y)] = 'O'
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
            if cell_value == 'T':
                cell_value = '-'
            draw.rectangle([(x * tile_side, y * tile_side), ((x + 1) * tile_side, (y + 1) * tile_side)], fill=COLORS[cell_value])
    for x in range(x_size + 1):
        draw.line([(tile_side * x, 0), (tile_side * x, size[1])], fill = 'black', width = line_size)
        draw.line([(tile_side * x + line_size, 0), (tile_side * x + line_size, size[1])], fill = 'black', width = line_size)
    for y in range(y_size + 1):
        draw.line([(0, tile_side * y), (size[0], tile_side * y)], fill = 'black', width = line_size)
        draw.line([(0, tile_side * y + line_size), (size[0], tile_side * y + line_size)], fill = 'black', width = line_size)
    drone_line = [(list_of_states[0]['drone_x'] * tile_side + int(tile_side/2), list_of_states[0]['drone_y'] * tile_side + int(tile_side/2))]
    target_count = 0
    target = (-1, -1)
    for index in range(1, len(list_of_states)):
        current_states = list_of_states[index]
        if 'drone_x' in current_states or 'drone_y' in current_states:
            drone_line.append(
                ((current_states['drone_x'] * tile_side + int(tile_side/2)) if 'drone_x' in current_states else drone_line[-1][0],
                 (current_states['drone_y'] * tile_side + int(tile_side/2)) if 'drone_y' in current_states else drone_line[-1][1])
            )
        if current_states['target_x'] != target[0] or current_states['target_y'] != target[1]:
            target_count = target_count + 1
            target = (current_states['target_x'], current_states['target_y'])
            draw.text((target[0] * tile_side + int(tile_side/2), target[1] * tile_side), str(target_count), fill = COLORS['T'], font_size = 18)
    draw.line(drone_line, fill = COLORS['D'], width = line_size)
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
    image.save(output_name + '_' + (f"{index:0>3}") + '.png')

def create_gif(index, output_name):
    if index < 1:
        return
    frames = [Image.open(output_name + '_' + (f"{image:0>3}") + '.png') for image in range(index)]
    frame_one = frames[0]
    frame_one.save(output_name + '_animate.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)
