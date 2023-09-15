import re
from PIL import Image, ImageDraw



def convert_line_to_grid(line):
    grid = [['-' for _ in range(7)] for _ in range(7)]
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

def draw_grid(grid, count):
    image = Image.new('RGB', (7*40, 7*40), 'black')
    draw = ImageDraw.Draw(image)
    for y in range(7):
        for x in range(7):
            cell_value = grid[y][x]
            draw.rectangle([(x * 40, y * 40), ((x + 1) * 40, (y + 1) * 40)], fill=COLORS[cell_value])
    image.save('./images/' + str(count) + '.png')

def handle_file():
    with open('./haskell/output.txt', 'r') as file:
        count = 0
        for line in file:
            grid = convert_line_to_grid(line)
            # # Print the grid
            # print('------------------------------------')
            # for row in grid:
            #     print(' '.join(row))
            draw_grid(grid, count)
            count = count + 1
        return count

def create_gif(count):
    frames = [Image.open('./images/' + str(image) + '.png') for image in range(count)]
    frame_one = frames[0]
    frame_one.save('./drone.gif', format = 'GIF', append_images = frames, save_all = True, duration = 300, loop = 0)
create_gif(handle_file())
