import os
import sys

location = sys.argv[1]

with open(location + 'template.tree', 'r') as f:
    template = f.read()

for i in range(2, 20 + 1):
    with open(location + 'simple_robot_' + str(i) + '.tree', 'w') as f:
        preamble = (
            'constants {' + os.linesep
            + '\tx_max = ' + str(i - 1) + os.linesep
            + '\ty_max = ' + str(i - 1) + os.linesep
            + '} end_constants' + os.linesep
        )
        f.write(preamble + template)
