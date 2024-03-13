import sys
from create_grid import create_grid
from basic_a_star import a_star

min_val = int(sys.argv[1])
max_val = int(sys.argv[2])
start_x = int(sys.argv[3])
start_y = int(sys.argv[4])
end_x = int(sys.argv[5])
end_y = int(sys.argv[6])
grid = create_grid('ignore/obstacles.txt', min_val, max_val)
print(grid[3][3])
print(a_star(grid, min_val, max_val, (start_x, start_y), (end_x, end_y)))
