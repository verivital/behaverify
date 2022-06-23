#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import re
import sys

if sys.argv[1] == "gcd":

    group_name = "gcd"

    folders = ["leaf", "leaf_no_IVAR", "total", "total_no_IVAR_errorless_unique_child"]
    foldersShort = ["Leaf",  "L_no", "Total", "T_unique"]
    files = ["gcd_example"]
    filesShort = ["gcd"]
    
elif sys.argv[1] == "basic":

    group_name = "basic"
    
    folders = ["BTCompiler", "leaf",  "leaf_no_IVAR", "total", "total_no_IVAR_errorless_unique_child"]
    foldersShort = ["BTC", "Leaf",  "L_no", "Total", "T_unique"]
    files = ["example0", "example1", "example2", "example3", "example4", "example5", "example6", "example7", "example8"]
    filesShort = ["Ex0", "Ex1", "Ex2", "Ex3", "Ex4", "Ex5", "Ex6", "Ex7", "Ex8"]
elif sys.argv[1] == "blueROV":

    group_name = "blueROV"

    folders = ["leaf", "leaf_no_IVAR", "total", "total_no_IVAR_errorless_unique_child"]
    foldersShort = ["Leaf", "L_no", "Total", "T_unique"]
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

    folders = ["BTCompiler", "leaf",  "leaf_no_IVAR", "total", "total_no_IVAR_errorless_unique_child"]
    foldersShort = ["BTC", "Leaf",  "L_no", "Total", "T_unique"]
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

elif sys.argv[1] == "robot":

    group_name = "robot"

    folders = ["BTCompiler", "leaf",  "leaf_no_IVAR", "total", "total_no_IVAR_errorless_unique_child"]
    foldersShort = ["BTC", "Leaf",  "L_no", "Total", "T_unique"]
    files = []
    filesShort = []
    for sel in range(1, 51):
            files.append(str(sel))
            filesShort.append(str(sel))
else:
    sys.exit("unknown arg")

    

    
diameters = []
reachable_states = []
total_states = []
elapsed_time_ltl = []
elapsed_time_ctl = []
elapsed_time_states = []
elapsed_time_model = []

reach=re.compile("reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)")
elapsed=re.compile("elapse: -?(?P<val1>[\.\d]+) seconds,")

for i in range(len(files)):
    file_name = files[i]
    diameters.append([])
    total_states.append([])
    reachable_states.append([])
    elapsed_time_ltl.append([])
    elapsed_time_ctl.append([])
    elapsed_time_states.append([])
    elapsed_time_model.append([])
    for j in range(len(folders)):
        folder = folders[j]
        found_states = False
        found_states_silent = False
        found_ctl_silent = False
        found_ltl_silent = False
        found_model = False
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
                        total_states[i].append(match.group('val3'))
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
            total_states[i].append('-')
        if not found_states_silent:
            elapsed_time_states[i].append('-')
        #if not found_ctl_silent:
            #elapsed_time_ctl[i].append('-')
        if not found_ltl_silent:
            elapsed_time_ltl[i].append('-')
        if not found_model:
            elapsed_time_model[i].append('-')



df = pd.DataFrame(diameters, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/diameters.tex', caption=group_name + ', System Diameter', label=group_name + '_diam')

df = pd.DataFrame(reachable_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/reachable_states.tex', caption=group_name + ', Reachable States', label=group_name + '_reach')


df = pd.DataFrame(total_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/total_states.tex', caption=group_name + ', Total States', label=group_name + '_total')

df = pd.DataFrame(elapsed_time_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_states.tex', caption=group_name + ', Time in Seconds to Compute Reachability', label=group_name + '_states_time')


#df = pd.DataFrame(elapsed_time_ctl, columns=foldersShort, index=filesShort)
#df.to_latex('./processed_data/' + group_name + '/elapsed_ctl.tex', caption=group_name + ', Time in Seconds to Compute CTL', label=group_name + '_CTL_time')


df = pd.DataFrame(elapsed_time_ltl, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_ltl.tex', caption=group_name + ', Time in Seconds to Compute LTL', label=group_name + '_LTL_time')


df = pd.DataFrame(elapsed_time_model, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/' + group_name + '/elapsed_model.tex', caption=group_name + ', Time in Seconds to Build Model', label=group_name + '_model_time')
