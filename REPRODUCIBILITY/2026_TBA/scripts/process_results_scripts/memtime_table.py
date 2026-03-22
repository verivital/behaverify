#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

minimal = False
if len(sys.argv) >= 3:
    if sys.argv[2] == 'True':
        minimal = True

if sys.argv[1] == "blueROV":

    group_name = "blueROV"

    folders = ["leaf_v1", "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["Leaf_v1", "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = ["full", "small", "warnings_only"]
    filesShort = ["full", "small", "warnings_only"]

elif sys.argv[1] == "checklist":

    group_name = "checklist"

    folders = ["BTCompiler", "leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["BTC", "Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = []
    filesShort = []
    for sel in range(1, 51):
            files.append(str(sel))
            filesShort.append(str(sel))
elif sys.argv[1] == "parallel-checklist":

    group_name = "parallel-checklist"

    folders = ["BTCompiler", "leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["BTC", "Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = []
    filesShort = []
    for sel in range(1, 51):
            files.append(str(sel))
            filesShort.append(str(sel))
else:
    sys.exit("unknown arg")

if minimal:
    folders[:] = [x for x in folders if not 'v1' in x]
    foldersShort[:] = [x for x in foldersShort if not 'v1' in x]
    print(folders)

#folders = ["BTCompiler"]
#foldersShort = ["BTC"]

    


elapsed_time_ltl = []

elapsed=re.compile("system, -?(?P<val1>[\.\d]+) elapsed")

for i in range(len(files)):
    file_name = files[i]
    elapsed_time_ltl.append([])
    for j in range(len(folders)):
        folder = folders[j]
        found_ltl_silent = False
        try:
            with open('./results/' + group_name + '/' + folder + '-' + file_name + '.txt', 'r') as cur_file:
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        elapsed_time_ltl[i].append(match.group('val1'))
                        found_ltl_silent = True
        except FileNotFoundError as e:
            pass
        try:
            with open('./results/' + group_name + '/models_' + folder + '-STATES_SILENT_' + file_name + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_states[i].append(match.group('val1'))
                            found_states_silent = True
        except FileNotFoundError as e:
            pass
        if not found_ltl_silent:
            elapsed_time_ltl[i].append('-')





df = pd.DataFrame(elapsed_time_ltl, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_build.tex', caption=group_name + ', Time in Seconds to Create .smv', label=group_name + '_build')


if 'checklist' in group_name:
    
    x_range = list(range(1, 51))
            
    for i in range(len(foldersShort)):
        y_range = []
        for x in range(50):
            val = elapsed_time_ltl[x][i]
            if val == '-':
                #y_range.append(350)
                y_range.append(500)
            else:
                y_range.append(float(val))
        if foldersShort[i] == 'BTC':
            plt.plot(x_range, y_range, color = 'red', marker = 'o')
        elif foldersShort[i] == 'Leaf_v1':
            plt.plot(x_range, y_range, color = 'blue', marker = 'v')
        elif foldersShort[i] == 'Leaf_v2':
            plt.plot(x_range, y_range, color = 'green', marker = '^')
        elif foldersShort[i] == 'Total_v1':
            plt.plot(x_range, y_range, color = 'yellow', marker = '*')
        elif foldersShort[i] == 'Total_v2':
            plt.plot(x_range, y_range, color = 'magenta', marker = 'x')
        elif foldersShort[i] == 'Total_v3':
            plt.plot(x_range, y_range, color = 'black', marker = '.')
    plt.ylabel('Time in Seconds')
    plt.xlabel('Number of Checks in ' + group_name)
    plt.title('Time in Seconds to Create .smv in ' + group_name)
    plt.legend(foldersShort)
    plt.tight_layout()
    plt.savefig('./processed_data/' + group_name + '/elapsed_build.png')

