import sys
from create_grid import create_grid
from PIL import Image, ImageDraw
import onnxruntime


COLORS = {1: 'black', 0: 'white', 'g' : 'green', 'd' : 'blue'}

def argmax(vals):
    max_index = 0
    for index in range(len(vals)):
        max_index = index if vals[index] > vals[max_index] else max_index
    return max_index

CODES = {
    0 : 'left',
    1 : 'right',
    2 : 'up',
    3 : 'down',
    4 : 'no_action'
}


def draw_grid(file_name, network_file, end_x, end_y, x_size, y_size):
    grid = create_grid(file_name, 0, x_size - 1)
    circle_mode = (grid[end_x][end_y] == 1)
    grid[end_x][end_y] = 'g'
    tile_side = int(400 / max(x_size, y_size))
    line_size = int(tile_side/20) + 1
    size = (x_size * tile_side + 2*line_size, y_size * tile_side + 2*line_size)

    image = Image.new('RGB', size, 'black')
    draw = ImageDraw.Draw(image)

    for x in range(x_size):
        for y in range(y_size):
            if circle_mode and x == end_x and y == end_y:
                circle_value = COLORS['g']
                rectangle_value = COLORS[1]
                draw.rectangle([(x * tile_side, y * tile_side), ((x + 1) * tile_side, (y + 1) * tile_side)], fill = rectangle_value)
                draw.ellipse([(x * tile_side + 2 * line_size, y * tile_side + 2 * line_size), ((x + 1) * tile_side - 2 * line_size, (y + 1) * tile_side - 2 * line_size)], fill = circle_value)
                continue
            cell_value = grid[x][y]
            draw.rectangle([(x * tile_side, y * tile_side), ((x + 1) * tile_side, (y + 1) * tile_side)], fill=COLORS[cell_value])
    for x in range(x_size + 1):
        draw.line([(tile_side * x, 0), (tile_side * x, size[1])], fill = 'black', width = line_size)
        draw.line([(tile_side * x + line_size, 0), (tile_side * x + line_size, size[1])], fill = 'black', width = line_size)
    for y in range(y_size + 1):
        draw.line([(0, tile_side * y), (size[0], tile_side * y)], fill = 'black', width = line_size)
        draw.line([(0, tile_side * y + line_size), (size[0], tile_side * y + line_size)], fill = 'black', width = line_size)
    session = onnxruntime.InferenceSession(network_file)
    input_name = session.get_inputs()[0].name
    for start_x in range(x_size):
        for start_y in range(x_size):
            # print(session.run(None, {input_name : [[float(start_x), float(start_y), float(end_x), float(end_y)]]})[0][0])
            action = CODES[argmax(session.run(None, {input_name : [[float(start_x), float(start_y), float(end_x), float(end_y)]]})[0][0])]
            center_x = tile_side * start_x + (tile_side // 2)
            center_y = tile_side * start_y + (tile_side // 2)
            if action == 'no_action':
                draw.ellipse(
                    (
                        center_x - line_size,
                        center_y - line_size,
                        center_x + line_size,
                        center_y + line_size,
                    ), fill = COLORS['d'], outline = COLORS['d']
                )
                continue
            if action == 'left':
                dir_x = tile_side * start_x
                dir_y = center_y
                arrow_1_x = dir_x + (tile_side // 4)
                arrow_2_x = arrow_1_x
                arrow_1_y = dir_y - (tile_side // 4)
                arrow_2_y = dir_y + (tile_side // 4)
            elif action == 'right':
                dir_x = tile_side * (start_x + 1)
                dir_y = center_y
                arrow_1_x = dir_x - (tile_side // 4)
                arrow_2_x = arrow_1_x
                arrow_1_y = dir_y - (tile_side // 4)
                arrow_2_y = dir_y + (tile_side // 4)
            elif action == 'up':
                dir_x = center_x
                dir_y = tile_side * (start_y + 1)
                arrow_1_x = dir_x - (tile_side // 4)
                arrow_2_x = dir_x + (tile_side // 4)
                arrow_1_y = dir_y - (tile_side // 4)
                arrow_2_y = arrow_1_y
            elif action == 'down':
                dir_x = center_x
                dir_y = tile_side * start_y
                arrow_1_x = dir_x - (tile_side // 4)
                arrow_2_x = dir_x + (tile_side // 4)
                arrow_1_y = dir_y + (tile_side // 4)
                arrow_2_y = arrow_1_y
            else:
                raise RuntimeError("what")
            draw.line([(center_x, center_y), (dir_x, dir_y)], fill = COLORS['d'], width = line_size)
            draw.line([(arrow_1_x, arrow_1_y), (dir_x, dir_y), (arrow_2_x, arrow_2_y)], fill = COLORS['d'], width = line_size)
    image.save(file_name.replace('.txt', '.png').replace('obstacles', 'map_network'))

#file_name, network_file, end_x, end_y, x_size, y_size
draw_grid(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
