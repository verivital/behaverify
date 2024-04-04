import sys
from generate_data import generate_table
from misc_util import extract_info

obstacle_path = sys.argv[1]
(min_val, max_val, fly_at, number_of_obstacles, max_size) = extract_info(obstacle_path)

with open(obstacle_path.replace('obstacles', 'ANSRn').replace('.txt', '.tree'), 'w', encoding = 'utf-8') as output_file:
    constants = ', '.join(
        [
            'min_val := ' + str(min_val),
            'max_val := ' + str(max_val),
            'number_of_obstacles := ' + str(number_of_obstacles),
            'max_obstacle_size := ' + str(max_size)
        ]
    )
    with open(obstacle_path, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        (obstacles, obstacle_sizes) = data.split('#', 1)
        obstacles = obstacles.replace('#', '')
        obstacle_sizes = obstacle_sizes.replace('#', '')
    with open('template_network.tree', 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    template = template.replace('REPLACE_CONSTANTS', constants)
    template = template.replace('REPLACE_OBSTACLE_SIZES', obstacle_sizes)
    template = template.replace('REPLACE_OBSTACLES', obstacles)
    output_file.write(template)
