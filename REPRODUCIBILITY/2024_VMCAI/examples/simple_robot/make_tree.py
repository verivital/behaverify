import os
import sys

template_location = sys.argv[1]
location = sys.argv[2]
min_val = int(sys.argv[3])
max_val = int(sys.argv[4])
step_size = int(sys.argv[5])

with open(template_location + '/' + 'template.tree', 'r') as f:
    template = f.read()


for i in range(min_val, max_val + 1, step_size):
    with open(location + '/' + 'simple_robot_' + str(i) + '.tree', 'w') as f:
        preamble = (
            'configuration{}' + os.linesep
            + 'enumerations{}' + os.linesep
            + 'constants {\'x_max\' := ' + str(i - 1) + ', \'y_max\' := ' + str(i - 1) + '} end_constants' + os.linesep
        )
        f.write(preamble + template)
