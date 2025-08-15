import sys
from PIL import Image, ImageDraw
from behaverify.grid_world_draw.create_grid import create_grid
from behaverify.grid_world_draw.misc_util import extract_info


COLORS = {1: 'black', 0: 'white'}


def draw_grid(file_name, x_size, y_size):
    grid = create_grid(file_name, 0, x_size - 1)
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
    image.save(file_name.replace('.txt', '.png').replace('obstacles', 'map'))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_val = extract_info(sys.argv[1])[1]
        draw_grid(sys.argv[1], max_val + 1, max_val + 1)
    else:
        #file_name, x_size, y_size
        draw_grid(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
