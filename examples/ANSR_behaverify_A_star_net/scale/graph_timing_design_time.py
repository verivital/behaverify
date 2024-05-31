# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
import sys
# import os
FILE_1 = sys.argv[1]
FILE_2 = sys.argv[2]
OUTPUT = sys.argv[3]

data_1 = {}
data_2 = {}
for (cur_file, cur_data) in ((FILE_1, data_1), (FILE_2, data_2)):
    with open(cur_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if line == '':
                continue
            (grid_size, file_size) = line.split('::>', 1)
            grid_size = grid_size.strip()
            file_size = file_size.strip()
            cur_data[int(grid_size) + 1] = float(file_size)
for (cur_data, cur_encoding) in ((data_1, ('black', '*')), (data_2, ('green', 'v'))):
    x_range = []
    y_range = []
    for x in sorted(cur_data.keys()):
        x_range.append(x)
        y_range.append(cur_data[x])
    plt.plot(x_range, y_range, color = cur_encoding[0], marker = cur_encoding[1])
plt.ylabel('Time in Seconds')
plt.xlabel('Grid size (n by n)')
plt.legend(['dense fixed', 'sparse random'])
plt.tight_layout()
plt.savefig(OUTPUT + '.png', bbox_inches = 'tight')

plt.clf()
