import os
import sys
def indent(n):
    return ' ' * (4 * n)
MAX_VAL = int(sys.argv[1])
NUMBER_OF_OBSTACLES = int(sys.argv[2])
OBSTACLE_FILE = sys.argv[3]
OUTPUT_LOCATION = sys.argv[4]
def create_obstacle_definition():
    obstacles = {}
    obstacle_sizes = {}
    with open(OBSTACLE_FILE, 'r', encoding = 'utf-8') as input_file:
        data = input_file.read()
        data = data.replace('condition {(eq, index_var,', '')
        data = data.replace(')} assign{result{', ', ')
        data = data.replace('}}', ';')
        (locations, sizes) = data.split('#', 1)
        locations = locations.replace('#', '')
        sizes = sizes.replace('#', '')
        for index_val in locations.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacles[index] = val
        for index_val in sizes.split(';'):
            if index_val.strip() == '':
                continue
            (index, val) = index_val.split(',')
            index = int(index.strip())
            val = int(val.strip())
            obstacle_sizes[index] = val
    return ''.join(
        [
            (indent(2) + 'obstacles_index_' + str(index) + ' := ' + str(value) + ';' + os.linesep)
            for (index, value) in obstacles.items()
        ]
        +
        [
            (indent(2) + 'obstacle_sizes_index_' + str(index) + ' := ' + str(value) + ';' + os.linesep)
            for (index, value) in obstacle_sizes.items()
        ]
    )
OBSTACLE_DEFINITION = create_obstacle_definition()
PREAMBLE = (
    'MODULE main' + os.linesep
    + indent(1) + 'VAR' + os.linesep
    + indent(2) + 'system : system_module;' + os.linesep
    + os.linesep
)
SAFETY_POSTAMBLE = (
    'MODULE system_module' + os.linesep
    + indent(1) + 'DEFINE' + os.linesep
    + OBSTACLE_DEFINITION
    + indent(1) + 'VAR' + os.linesep
    + indent(2) + 'drone_x : 0..' + str(MAX_VAL) + ';' + os.linesep
    + indent(2) + 'drone_y : 0..' + str(MAX_VAL) + ';' + os.linesep
    + indent(2) + 'drone_speed : 1..2;' + os.linesep
    + indent(2) + 'delta_x : -1..1;' + os.linesep
    + indent(2) + 'delta_y : -1..1;' + os.linesep
    + indent(1) + 'ASSIGN' + os.linesep
    + indent(2) + 'init(drone_x) := {' + ', '.join([str(val) for val in range(MAX_VAL + 1)]) + '};' + os.linesep
    + indent(2) + 'init(drone_y) := {' + ', '.join([str(val) for val in range(MAX_VAL + 1)]) + '};' + os.linesep
    + indent(2) + 'init(delta_x) := {-1, 0, 1};' + os.linesep
    + indent(2) + 'init(delta_y) := {-1, 0, 1};' + os.linesep
    + indent(2) + 'next(delta_x) := {-1, 0, 1};' + os.linesep
    + indent(2) + 'next(delta_y) := {-1, 0, 1};' + os.linesep
    + indent(2) + 'next(drone_x) := min(' + str(MAX_VAL) + ', max(0, drone_x + (drone_speed * delta_x)));' + os.linesep
    + indent(2) + 'next(drone_y) := min(' + str(MAX_VAL) + ', max(0, drone_y + (drone_speed * delta_y)));' + os.linesep
)
LIVENESS_POSTAMBLE = (
    'MODULE system_module' + os.linesep
    + indent(1) + 'VAR' + os.linesep
    + indent(2) + 'current_action : {0, 1, 2, 3, 4};' + os.linesep
)
SAFETY_SPEC = (
    'LTLSPEC G(!('
    + ' | '.join(
        [
            (
                '('
                + '(system.drone_x <= system.obstacles_index_' + str(2 * index) + ')'
                + '& (system.drone_x >= (system.obstacles_index_' + str(2 * index) + ' - system.obstacle_sizes_index_' + str(index) + '))'
                + '& (system.drone_y <= system.obstacles_index_' + str((2 * index) + 1) + ')'
                + '& (system.drone_y >= (system.obstacles_index_' + str((2 * index) + 1) + ' - system.obstacle_sizes_index_' + str(index) + '))'
                + ')'
            )
            for index in range(NUMBER_OF_OBSTACLES)
        ]
    )
    + '));' + os.linesep
    + os.linesep
)
LIVENESS_SPEC = (
    'LTLSPEC G('
    + '((system.current_action = 0) -> (X(system.current_action != 1)))'
    + ' & ((system.current_action = 1) -> (X(system.current_action != 0)))'
    + ' & ((system.current_action = 2) -> (X(system.current_action != 3)))'
    + ' & ((system.current_action = 3) -> (X(system.current_action != 2)))'
    + ');' + os.linesep
    + os.linesep
)
with open(OUTPUT_LOCATION + 'nurv_collision.smv', 'w', encoding = 'utf-8') as output_file:
    output_file.write(PREAMBLE + SAFETY_SPEC + SAFETY_POSTAMBLE)
with open(OUTPUT_LOCATION + 'nurv_loop.smv', 'w', encoding = 'utf-8') as output_file:
    output_file.write(PREAMBLE + LIVENESS_SPEC + LIVENESS_POSTAMBLE)
