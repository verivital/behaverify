import random
import os
import sys

def insert_max(size):
    return_string = ''
    with open(TEMPLATE_FILE, 'r', encoding = 'utf-8') as template:
        return_string = template.read()
    return_string = return_string.replace('x_max := 10', 'x_max := ' + str(size))
    return_string = return_string.replace('y_max := 10', 'y_max := ' + str(size))
    return return_string

def write_file(size):
    with open(WRITE_LOCATION + '/ANSR_scaling_grid_' + str(size) + '.tree', 'w', encoding = 'utf-8') as output:
        output.write(insert_max(size))
    return

TEMPLATE_FILE = sys.argv[1]
WRITE_LOCATION = sys.argv[2]
MIN_VAL = int(sys.argv[3])
MAX_VAL = int(sys.argv[4]) + 1
STEP_SIZE =int( sys.argv[5])

for count in range(MIN_VAL, MAX_VAL, STEP_SIZE):
    print(count)
    write_file(count)
