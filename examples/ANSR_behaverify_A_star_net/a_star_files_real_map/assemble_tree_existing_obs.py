import sys
from generate_data import generate_table

obstacles = sys.argv[1]
template_loc = sys.argv[2]
(_, max_val, fly_at, number_of_obstacles, max_size) = obstacles.split('/')[-1].split('.')[0].split('_')
number_of_obstacles = int(number_of_obstacles)
min_val = 0
max_val = int(max_val)
max_size = int(max_size)

tail_end = str(max_val) + '_' + str(fly_at) + '_' + str(number_of_obstacles) + '_' + str(max_size)
start_end = ('.' if '/' not in obstacles else obstacles.rsplit('/', 1)[0]) + '/'
generate_table(min_val, max_val, obstacles, start_end + 'table_' + tail_end + '.txt')

with open(start_end + 'ANSR_behaverify_A_star_table_' + tail_end + '.tree', 'w', encoding = 'utf-8') as output_file:
    constants = ', '.join(
        [
            'min_val := ' + str(min_val),
            'max_val := ' + str(max_val),
            'number_of_obstacles := ' + str(number_of_obstacles),
            'max_obstacle_size := ' + str(max_size)
        ]
    )
    with open(start_end + 'table_' + tail_end + '.txt', 'r', encoding = 'utf-8') as input_file:
        fake_network = input_file.read()
    with open(obstacles, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        (obstacles, obstacle_sizes) = data.split('#', 1)
        obstacles = obstacles.replace('#', '')
        obstacle_sizes = obstacle_sizes.replace('#', '')
    with open(template_loc, 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    template = template.replace('REPLACE_CONSTANTS', constants)
    template = template.replace('REPLACE_OBSTACLE_SIZES', obstacle_sizes)
    template = template.replace('REPLACE_OBSTACLES', obstacles)
    template = template.replace('REPLACE_FAKE_NETWORK', fake_network)
    output_file.write(template)
