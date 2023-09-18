import re
import sys
import os
from PIL import Image, ImageDraw



def convert_line_to_grid(line, x_size, y_size):
    grid = [['-' for _ in range(y_size)] for _ in range(x_size)]
    # Extract relevant values from the line using regular expressions
    boardCurX = int(re.search(r'boardCurX: (\d+)', line).group(1))
    boardCurY = int(re.search(r'boardCurY: (\d+)', line).group(1))
    envTarX = int(re.search(r'envTarX: (\d+)', line).group(1))
    envTarY = int(re.search(r'envTarY: (\d+)', line).group(1))
    # envTreeX = [int(re.search(r'envTreeX: \[(\d+),', line).group(1)), int(re.search(r', (\d+)\], envTreeY', line).group(1))]
    # envTreeY = [int(re.search(r'envTreeY: \[(\d+),', line).group(1)), int(re.search(r', (\d+)\], envTarX', line).group(1))]
    envTreeX = [int(re.search(r'envTreeX: \[(\d+), (\d+)\]', line).group(1)), int(re.search(r'envTreeX: \[(\d+), (\d+)\]', line).group(2))]
    envTreeY = [int(re.search(r'envTreeY: \[(\d+), (\d+)\]', line).group(1)), int(re.search(r'envTreeY: \[(\d+), (\d+)\]', line).group(2))]

    # Update the grid with 'R', 'F', and 'T' as needed
    grid[envTreeY[0]][envTreeX[0]] = 'T'
    grid[envTreeY[1]][envTreeX[1]] = 'T'
    grid[envTarY][envTarX] = 'F'
    grid[boardCurY][boardCurX] = 'R'
    return grid


COLORS = {'R': 'blue', 'F': 'yellow', 'T': 'green', '-': 'white'}

def draw_grid(grid, count, x_size, y_size):
    x_dim = -1
    y_dim = -1
    for size in range(280,400):
        x_dim = (x_dim if x_dim != -1 else (size // x_size if size % x_size == 0 else -1))
        y_dim = (y_dim if y_dim != -1 else (size // y_size if size % y_size == 0 else -1))
        if x_dim != -1 and y_dim != -1:
            break
    image = Image.new('RGB', (x_size * x_dim, y_size * y_dim), 'black')
    draw = ImageDraw.Draw(image)
    for y in range(y_size):
        for x in range(x_size):
            cell_value = grid[y][x]
            draw.rectangle([(x * x_dim, y * y_dim), ((x + 1) * x_dim, (y + 1) * y_dim)], fill=COLORS[cell_value])
    image.save('./' + str(x_size) + 'x' + str(y_size) + '_images' + ('_trained' if TRAINED else '') + '/' + str(count) + '.png')

def handle_file(x_size, y_size):
    with open('./haskell' + ('_trained' if TRAINED else '') + '/output.txt', 'r') as file:
        count = 0
        if not os.path.exists('./' + str(x_size) + 'x' + str(y_size) + '_images' + ('_trained' if TRAINED else '')):
            os.makedirs('./' + str(x_size) + 'x' + str(y_size) + '_images' + ('_trained' if TRAINED else ''))
        for line in file:
            grid = convert_line_to_grid(line, x_size, y_size)
            # # Print the grid
            # print('------------------------------------')
            # for row in grid:
            #     print(' '.join(row))
            draw_grid(grid, count, x_size, y_size)
            count = count + 1
        return count

def create_gif(count, x_size, y_size):
    frames = [Image.open('./' + str(x_size) + 'x' + str(y_size) + '_images' + ('_trained' if TRAINED else '') + '/' + str(image) + '.png') for image in range(count)]
    frame_one = frames[0]
    frame_one.save('./drone.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)
TRAINED = bool(sys.argv[1])
create_gif(handle_file(int(sys.argv[2]), int(sys.argv[3])), int(sys.argv[2]), int(sys.argv[3]))
