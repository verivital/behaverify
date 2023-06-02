import os

with open('template.tree', 'r') as f:
    template = f.read()

for i in range(2, 20 + 1):
    with open('simple_robot_' + str(i) + '.tree', 'w') as f:
        preamble = (
            'constants {' + os.linesep
            + '\tx_max = ' + str(i) + os.linesep
            + '\ty_max = ' + str(i) + os.linesep
            + '} end_constants' + os.linesep
        )
        f.write(preamble + template)
