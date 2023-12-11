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
    with open(location + '/' + 'simplified_robot_' + str(i) + '.tree', 'w') as f:
        preamble = (
            'constants {' + os.linesep
            + '\tx_max = ' + str(i - 1) + os.linesep
            + '\ty_max = ' + str(i - 1) + os.linesep
            + '} end_constants' + os.linesep
        )
        f.write(preamble + template)
