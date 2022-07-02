#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

minimal = False
if len(sys.argv) >= 3:
    if sys.argv[2] == 'True':
        minimal = True

if sys.argv[1] == "gcd":

    group_name = "gcd"

    folders = ["leaf_v1", "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = ["gcd_example"]
    filesShort = ["gcd"]
    
elif sys.argv[1] == "basic":

    group_name = "basic"
    
    folders = ["BTCompiler", "leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["BTC", "Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = ["example0", "example1", "example2", "example3", "example4", "example5", "example6", "example7", "example8"]
    filesShort = ["Ex0", "Ex1", "Ex2", "Ex3", "Ex4", "Ex5", "Ex6", "Ex7", "Ex8"]
elif sys.argv[1] == "blueROV":

    group_name = "blueROV"

    folders = ["leaf_v1", "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["Leaf_v1", "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = []
    filesShort = []
    base1 = ['blueROV_warnings_only', 'blueROV_small', 'blueROV_full']
    base2 = ['battery', 'emergency', 'home_reached', 'obstacle', 'sensor']
    for b1 in base1:
        for b2 in base2:
            files.append(b1 + "_" + b2)
            filesShort.append(b1[8] + " " + b2[0:4])
elif sys.argv[1] == "auto_example":

    group_name = "auto_example"

    folders = ["BTCompiler", "leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["BTC", "Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = []
    filesShort = []
    for sel in [0, 5, 10, 15, 20]:
        for seq in range(0, 21):
            files.append("sel" + str(sel) + "-" + "seq" + str(seq))
            filesShort.append(str(sel) + ", " + str(seq))
    for seq in [0, 5, 10, 15, 20]:
        for sel in range(0, 21):
            if sel in [0, 5, 10, 15, 20]:
                continue
            files.append("sel" + str(sel) + "-" + "seq" + str(seq))
            filesShort.append(str(sel) + ", " + str(seq))

elif sys.argv[1] == "checklist":

    group_name = "checklist"

    folders = ["BTCompiler", "leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["BTC", "Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
    files = []
    filesShort = []
    for sel in range(1, 51):
            files.append(str(sel))
            filesShort.append(str(sel))
elif sys.argv[1] == "checklist-v2":            
    group_name = "checklist-v2"

    folders = ["leaf_v1",  "leaf_v2", "total_v1", "total_v2", "total_v3"]
    foldersShort = ["Leaf_v1",  "Leaf_v2", "Total_v1", "Total_v2", "Total_v3"]
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

folders = ["BTCompiler"]
foldersShort = ["BTC"]

    

    
diameters = []
reachable_states = []
total_v1_states = []
elapsed_time_ltl = []
elapsed_time_ctl = []
elapsed_time_states = []
elapsed_time_model = []
maximum_resident_ltl = []

reach=re.compile("reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)")
elapsed=re.compile("elapse: -?(?P<val1>[\.\d]+) seconds,")
resident=re.compile("Maximum resident size\s*= (?P<val1>[\.\d]+)K")

for i in range(len(files)):
    file_name = files[i]
    diameters.append([])
    total_v1_states.append([])
    reachable_states.append([])
    elapsed_time_ltl.append([])
    elapsed_time_ctl.append([])
    elapsed_time_states.append([])
    elapsed_time_model.append([])
    maximum_resident_ltl.append([])
    for j in range(len(folders)):
        folder = folders[j]
        found_states = False
        found_states_silent = False
        found_ctl_silent = False
        found_ltl_silent = False
        found_model = False
        found_resident = False
        try:
            with open('./results/' + group_name + '/models_' + folder + '-STATES_' + file_name + '.txt', 'r') as cur_file:
                for line in cur_file:
                    if "system diameter:" in line:
                        val=line.split(':')[1]
                        val=val.strip()
                        diameters[i].append(val)
                    match=reach.search(line)
                    if match:
                        reachable_states[i].append(match.group('val1'))
                        total_v1_states[i].append(match.group('val3'))
                        found_states = True
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
        # try:
        #     with open('./results/' + group_name + '/models_' + folder + '-CTL_SILENT_' + file_name + '.txt', 'r') as cur_file:
        #         decoy = True
        #         for line in cur_file:
        #             match=elapsed.search(line)
        #             if match:
        #                 if decoy:
        #                     decoy = False
        #                 else:
        #                     elapsed_time_ctl[i].append(match.group('val1'))
        #                     found_ctl_silent = True
        # except FileNotFoundError as e:
        #     pass
        try:
            with open('./results/' + group_name + '/models_' + folder + '-LTL_SILENT_' + file_name + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_ltl[i].append(match.group('val1'))
                            found_ltl_silent = True
            with open('./results/' + group_name + '/models_' + folder + '-LTL_SILENT_' + file_name + '.txt', 'r') as cur_file:
                #decoy = True
                for line in cur_file:
                    #print(line)
                    match=resident.search(line)
                    if match:
                        #if decoy:
                            #decoy = False
                        #else:
                        maximum_resident_ltl[i].append(match.group('val1'))
                        found_resident = True
        except FileNotFoundError as e:
            pass
        try:
            with open('./results/' + group_name + '/models_' + folder + '-MODEL_' + file_name + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_model[i].append(match.group('val1'))
                            found_model = True
        except FileNotFoundError as e:
            pass
        if not found_states:
            diameters[i].append('-')
            reachable_states[i].append('-')
            total_v1_states[i].append('-')
        if not found_states_silent:
            elapsed_time_states[i].append('-')
        #if not found_ctl_silent:
            #elapsed_time_ctl[i].append('-')
        if not found_ltl_silent:
            elapsed_time_ltl[i].append('-')
        if not found_model:
            elapsed_time_model[i].append('-')
        if not found_resident:
            maximum_resident_ltl[i].append('-')



df = pd.DataFrame(diameters, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/diameters.tex', caption=group_name + ', System Diameter', label=group_name + '_diam')

df = pd.DataFrame(reachable_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/reachable_states.tex', caption=group_name + ', Reachable States', label=group_name + '_reach')


df = pd.DataFrame(total_v1_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/total_states.tex', caption=group_name + ', Total States', label=group_name + '_total')

df = pd.DataFrame(elapsed_time_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_states.tex', caption=group_name + ', Time in Seconds to Compute Reachability', label=group_name + '_states_time')


#df = pd.DataFrame(elapsed_time_ctl, columns=foldersShort, index=filesShort)
#df.to_latex('./processed_data/' + group_name + '/elapsed_ctl.tex', caption=group_name + ', Time in Seconds to Compute CTL', label=group_name + '_CTL_time')


df = pd.DataFrame(elapsed_time_ltl, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_ltl.tex', caption=group_name + ', Time in Seconds to Compute LTL', label=group_name + '_LTL_time')


df = pd.DataFrame(elapsed_time_model, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_model.tex', caption=group_name + ', Time in Seconds to Build Model', label=group_name + '_model_time')

df = pd.DataFrame(maximum_resident_ltl, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/maximum_resident_ltl.tex', caption=group_name + ', Maximum Resident Size in K to Compute LTL', label=group_name + '_LTL_size')


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
    plt.title('Time in Seconds to verify LTL Specs in ' + group_name)
    plt.legend(foldersShort)
    plt.tight_layout()
    plt.savefig('./processed_data/' + group_name + '/elapsed_ltl.png')

    plt.clf()
    for i in range(len(foldersShort)):
        y_range = []
        for x in range(50):
            val = maximum_resident_ltl[x][i]
            if val == '-':
                y_range.append(-1000)
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
    plt.ylabel('Maximum Resident Size in K')
    plt.xlabel('Number of Checks in ' + group_name)
    plt.title('Max Resident Size in K for LTL Specs in ' + group_name)
    plt.legend(foldersShort)
    plt.tight_layout()
    plt.savefig('./processed_data/' + group_name + '/memory_ltl.png')
            
