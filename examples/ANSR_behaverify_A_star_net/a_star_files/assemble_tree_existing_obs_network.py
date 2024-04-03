import sys
from generate_obstacles import generate_obstacles
from generate_data import generate_table

max_val = int(sys.argv[1])
number_of_obstacles = int(sys.argv[2])
max_size = int(sys.argv[3])
min_val = 0
obstacles = sys.argv[4]

tail_end = '_' + str(max_val) + '_' + str(number_of_obstacles) + '_' + str(max_size)

with open('ignore/ANSR_behaverify_A_star_network' + tail_end + '.tree', 'w', encoding = 'utf-8') as output_file:
    constants = ', '.join(
        [
            'min_val := ' + str(min_val),
            'max_val := ' + str(max_val),
            'number_of_obstacles := ' + str(number_of_obstacles),
            'max_obstacle_size := ' + str(max_size)
        ]
    )
    with open(obstacles, 'r', encoding = 'utf-8') as input_file:
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
