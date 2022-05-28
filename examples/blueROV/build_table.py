#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import re

folders = ["./models_selector_mixed", "./models_selector_parallel", "./models_selector_non_parallel", "./models_sequence",  "./models_path", "./models_double_path"]
#folders2 = ["selector_mixed", "selector_parallel", "selector_non_parallel",  "sequence", "path"]
folders2 = ["selector_parallel", "selector_non_parallel",  "sequence", "path", "double_path"]
files = ["blueROV_full", "blueROV_full_small", "blueROV_warnings_only"]
filesShort = ["blueROV1", "blueROV2", "blueROV3"]

foldersShort = ["SelParallel", "SelNonParallel", "Sequence", "Path", "DoublePath"]

#diameters = {}
#reachable_states = {}
#total_states = {}
diameters = []
reachable_states = []
total_states = []
elapsed_time = []

reach=re.compile("reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)")
elapsed=re.compile("system, (?P<val1>[\.\d]+) elapsed")

#for file_name in files:
for i in range(len(files)):
    file_name = files[i]
    diameters.append([])
    total_states.append([])
    reachable_states.append([])
    elapsed_time.append([])
    # diameters[file_name]={}
    # reachable_states[file_name]={}
    # total_states[file_name]={}
    # for folder in folders2:
    for j in range(len(folders2)):
        folder = folders2[j]
        try:
            with open('./models_' + folder + '/results/STATES_' + file_name + '_ltl_full.txt', 'r') as cur_file:
                for line in cur_file:
                    if "system diameter:" in line:
                        val=line.split(':')[1]
                        val=val.strip()
                        diameters[i].append(val)
                        #diameters[file_name][folder] = val
                    match=reach.search(line)
                    if match:
                        #reachable_states[file_name][folder]=int(match.group('val1'))
                        #total_states[file_name][folder]=int(match.group('val3'))
                        reachable_states[i].append(match.group('val1'))
                        total_states[i].append(match.group('val3'))


                        #vals_reachable_pow.append(float(match.group('val2')))
                        #vals_total_pow.append(float(match.group('val4')))
                    match=elapsed.search(line)
                    if match:
                        elapsed_time[i].append(match.group('val1'))
        except FileNotFoundError as e:
            diameters[i].append('-')
            reachable_states[i].append('-')
            total_states[i].append('-')
            elapsed_time[i].append('-')


print(elapsed_time)

df = pd.DataFrame(diameters, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/diameters.tex', caption='BlueROV, System Diameter', label='ROV_diam')

df = pd.DataFrame(reachable_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/reachable_states.tex', caption='BlueROV, Reachable States', label='ROV_reach')


df = pd.DataFrame(total_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/total_states.tex', caption='BlueROV, Total States', label='ROV_total')

df = pd.DataFrame(elapsed_time, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/elapsed_states.tex', caption='BlueROV, Time in Seconds to Compute Reachability', label='ROV_states_time')


elapsed_time = []


for i in range(len(files)):
    file_name = files[i]
    elapsed_time.append([])
    for j in range(len(folders2)):
        folder = folders2[j]
        try:
            with open('./models_' + folder + '/results/' + file_name + '_ltl_full.txt', 'r') as cur_file:
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        elapsed_time[i].append(match.group('val1'))
        except FileNotFoundError as e:
            elapsed_time[i].append('-')


df = pd.DataFrame(elapsed_time, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/elapsed_full.tex', caption='BlueROV, Time in Seconds for all LTL Specs', label='ROV_LTL_full_time')


elapsed_time = []


for i in range(len(files)):
    file_name = files[i]
    elapsed_time.append([])
    for j in range(len(folders2)):
        folder = folders2[j]
        try:
            with open('./models_' + folder + '/results/' + file_name + '_ltl_battery_only.txt', 'r') as cur_file:
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        elapsed_time[i].append(match.group('val1'))
        except FileNotFoundError as e:
            elapsed_time[i].append('-')

print(elapsed_time)
df = pd.DataFrame(elapsed_time, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/elapsed_battery.tex', caption='BlueROV, Time in Seconds to for Battery LTL', label='ROV_LTL_battery_time')




#-----------------------------------------------------------------------------------------------------------------------------------------

elapsed=re.compile("elapse: (?P<val1>[\.\d]+) seconds,")

elapsed_time = []


for i in range(len(files)):
    file_name = files[i]
    elapsed_time.append([])
    for j in range(len(folders2)):
        folder = folders2[j]

        first = True
        try:
            with open('./models_' + folder + '/results/SILENT_' + file_name + '_ltl_full.txt', 'r') as cur_file:
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        if first:
                            first = False
                        else:
                            elapsed_time[i].append(match.group('val1'))
        except FileNotFoundError as e:
            elapsed_time[i].append('-')

df = pd.DataFrame(elapsed_time, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/silent/elapsed_full.tex', caption='BlueROV, Time in Seconds for all LTL Specs', label='ROV_LTL_full_time')


elapsed_time = []


for i in range(len(files)):
    file_name = files[i]
    elapsed_time.append([])
    for j in range(len(folders2)):
        folder = folders2[j]

        first = True
        try:
            with open('./models_' + folder + '/results/SILENT_' + file_name + '_ltl_battery_only.txt', 'r') as cur_file:
                for line in cur_file:
                    match=elapsed.search(line)
                    if match:
                        if first:
                            first = False
                        else:
                            elapsed_time[i].append(match.group('val1'))
        except FileNotFoundError as e:
            elapsed_time[i].append('-')


df = pd.DataFrame(elapsed_time, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/silent/elapsed_battery.tex', caption='BlueROV, Time in Seconds to for Battery LTL', label='ROV_LTL_battery_time')

