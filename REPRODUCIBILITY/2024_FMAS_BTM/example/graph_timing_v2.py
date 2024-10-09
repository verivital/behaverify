# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
import sys
# import os
FILE_1 = sys.argv[1]
FILE_2 = sys.argv[2]
FILE_3 = sys.argv[3]
BASELINE = sys.argv[4]
OUTPUT = sys.argv[5]

data_1 = {}
data_2 = {}
data_3 = {}
data_baseline = {}
for (cur_file, cur_data) in ((FILE_1, data_1), (FILE_2, data_2), (FILE_3, data_3), (BASELINE, data_baseline)):
    # print(cur_file)
    with open(cur_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if line == '':
                continue
            (grid_size, file_size) = line.split('::>', 1)
            grid_size = grid_size.strip()
            file_size = file_size.strip()
            cur_data[int(grid_size) + 1] = float(file_size)
            # print(file_size)
for (cur_data, cur_encoding) in ((data_1, ('black', '*')), (data_2, ('green', 'v')), (data_3, ('blue', '.'))):
    x_range = []
    y_range = []
    for x in sorted(cur_data.keys()):
        x_range.append(x)
        y_range.append(cur_data[x] - data_baseline[x])
    print(x_range)
    print(y_range)
    plt.plot(x_range, y_range, color = cur_encoding[0], marker = cur_encoding[1])
plt.ylabel('Time in Seconds')
plt.xlabel('Grid size (n by n)')
plt.legend(['BehaVerify', 'Copilot', 'NuRV'])
plt.tight_layout()
plt.savefig(OUTPUT + '.png', bbox_inches = 'tight')

plt.clf()
