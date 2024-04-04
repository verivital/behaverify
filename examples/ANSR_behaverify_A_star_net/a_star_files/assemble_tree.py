import sys
from generate_obstacles import generate_obstacles
from generate_data import generate_table
from misc_util import create_tail_end

max_val = int(sys.argv[1])
number_of_obstacles = int(sys.argv[2])
max_size = int(sys.argv[3])
min_val = 0
generate_obstacles(number_of_obstacles, min_val, max_val, max_size)
tail_end = create_tail_end(max_val, None, number_of_obstacles, max_size)
generate_table(min_val, max_val,
               'ignore/obstacles' + tail_end + '.txt',
               'ignore/table' + tail_end + '.txt')

with open('ignore/ANSRt' + tail_end + '.tree', 'w', encoding = 'utf-8') as output_file:
    constants = ', '.join(
        [
            'min_val := ' + str(min_val),
            'max_val := ' + str(max_val),
            'number_of_obstacles := ' + str(number_of_obstacles),
            'max_obstacle_size := ' + str(max_size)
        ]
    )
    with open('ignore/table' + tail_end + '.txt', 'r', encoding = 'utf-8') as input_file:
        fake_network = input_file.read()
    with open('ignore/obstacles' + tail_end + '.txt', 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        (obstacles, obstacle_sizes) = data.split('#', 1)
        obstacles = obstacles.replace('#', '')
        obstacle_sizes = obstacle_sizes.replace('#', '')
    with open('template.tree', 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    template = template.replace('REPLACE_CONSTANTS', constants)
    template = template.replace('REPLACE_OBSTACLE_SIZES', obstacle_sizes)
    template = template.replace('REPLACE_OBSTACLES', obstacles)
    template = template.replace('REPLACE_FAKE_NETWORK', fake_network)
    output_file.write(template)
