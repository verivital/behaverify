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
    # envTreeX = [int(re.search(r'envTreeX: \((\d+),(\d+)\)', line).group(1)), int(re.search(r'envTreeX: \((\d+),(\d+)\)', line).group(2))]
    # envTreeY = [int(re.search(r'envTreeY: \((\d+),(\d+)\)', line).group(1)), int(re.search(r'envTreeY: \((\d+),(\d+)\)', line).group(2))]
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
    image.save(OUTPUT_FOLDER + str(count) + '.png')

def handle_file(x_size, y_size):
    with open(INPUT_FOLDER + 'output.txt', 'r', encoding = 'utf-8') as input_file:
        count = 0
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        for line in input_file:
            grid = convert_line_to_grid(line, x_size, y_size)
            draw_grid(grid, count, x_size, y_size)
            count = count + 1
        return count

def create_gif(count):
    frames = [Image.open(OUTPUT_FOLDER + str(image) + '.png') for image in range(count)]
    frame_one = frames[0]
    frame_one.save(OUTPUT_FOLDER + 'drone.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)

INPUT_FOLDER = sys.argv[1]
if INPUT_FOLDER[-1] != '/':
    INPUT_FOLDER += '/'
OUTPUT_FOLDER = sys.argv[2]
if OUTPUT_FOLDER[-1] != '/':
    OUTPUT_FOLDER += '/'
X_MAX_VAL = int(sys.argv[3])
Y_MAX_VAL = int(sys.argv[4])
create_gif(handle_file(X_MAX_VAL, Y_MAX_VAL))
