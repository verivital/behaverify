import sys
from generate_data import generate_table
from misc_util import extract_info, handle_path

obstacle_path = sys.argv[1]
(min_val, max_val, fly_at, number_of_obstacles, max_size) = extract_info(obstacle_path)
generate_table(min_val, max_val, obstacle_path, obstacle_path.replace('obstacles', 'table'))

with open(obstacle_path.replace('obstacles', 'ANSRt').replace('.txt', '.tree'), 'w', encoding = 'utf-8') as output_file:
    constants = ', '.join(
        [
            'min_val := ' + str(min_val),
            'max_val := ' + str(max_val),
            'number_of_obstacles := ' + str(number_of_obstacles),
            'max_obstacle_size := ' + str(max_size)
        ]
    )
    with open(obstacle_path.replace('obstacles', 'table'), 'r', encoding = 'utf-8') as input_file:
        fake_network = input_file.read()
    with open(obstacle_path, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        (obstacles, obstacle_sizes) = data.split('#', 1)
        obstacles = obstacles.replace('#', '')
        obstacle_sizes = obstacle_sizes.replace('#', '')
    with open((handle_path('template_monitor.tree') if len(sys.argv) == 2 else sys.argv[2]), 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    template = template.replace('REPLACE_CONSTANTS', constants)
    template = template.replace('REPLACE_OBSTACLE_SIZES', obstacle_sizes)
    template = template.replace('REPLACE_OBSTACLES', obstacles)
    template = template.replace('REPLACE_FAKE_NETWORK', fake_network)
    output_file.write(template)
