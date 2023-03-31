# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys


encodings = ['aut', 'aut_s', 'func', 'norm']
encoding_name_to_result_name = {
    'aut' : 'aut_',
    'aut_s' : 'aut_s_',
    'func' : 'func_',
    'norm' : ''
}

encoding_mark = {
    'aut' : ('red', 'o'),
    'func' : ('blue', 'v'),
    'norm' : ('green', '^'),
    'tbd' : ('yellow', '*'),
    'tbd1' : ('magenta', 'x'),
    'aut_s' : ('black', '.'),
    'tbd3' : ('black', '.')
}

diameters = []
reachable_states = []
total_v1_states = []
elapsed_time_ltl = []
elapsed_time_ctl = []
elapsed_time_states = []
elapsed_time_model = []
maximum_resident_ltl = []

reach = re.compile('reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)')
elapsed = re.compile('elapse: -?(?P<val1>[\.\d]+) seconds,')
resident = re.compile('Maximum resident size\s*= (?P<val1>[\.\d]+)K')

group_name = sys.argv[1]
experiments = list(map(str, range(2, 21)))

for encoding_name in encodings:
    encoding_result_name = encoding_name_to_result_name[encoding_name]

    diameters.append([])
    total_v1_states.append([])
    reachable_states.append([])
    elapsed_time_ltl.append([])
    elapsed_time_ctl.append([])
    elapsed_time_states.append([])
    elapsed_time_model.append([])
    maximum_resident_ltl.append([])
    for experiment in experiments:
        found_diamater = False
        found_states = False
        found_states_silent = False
        found_ctl_silent = False
        found_ltl_silent = False
        found_model = False
        found_resident = False
        try:
            with open('../examples/' + group_name + '/results/STATES_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                for line in cur_file:
                    if 'system diameter:' in line:
                        val = line.split(':')[1]
                        val = val.strip()
                        diameters[-1].append(val)
                        found_diamater = True
                    match = reach.search(line)
                    if match:
                        reachable_states[-1].append(match.group('val1'))
                        total_v1_states[-1].append(match.group('val3'))
                        found_states = True
        except FileNotFoundError:
            pass
        try:
            with open('../examples/' + group_name + '/results/SILENT_STATES_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match = elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_states[-1].append(match.group('val1'))
                            found_states_silent = True
        except FileNotFoundError:
            pass
        try:
            with open('../examples/' + group_name + '/results/SILENT_CTL_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match = elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_ctl[-1].append(match.group('val1'))
                            found_ctl_silent = True
        except FileNotFoundError:
            pass
        try:
            with open('../examples/' + group_name + '/results/SILENT_LTL_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match = elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_ltl[-1].append(match.group('val1'))
                            found_ltl_silent = True
            with open('../examples/' + group_name + '/results/SILENT_LTL_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                # decoy = True
                for line in cur_file:
                    # print(line)
                    match = resident.search(line)
                    if match:
                        # if decoy:
                        #     decoy = False
                        # else:
                        maximum_resident_ltl[-1].append(match.group('val1'))
                        found_resident = True
        except FileNotFoundError:
            pass
        try:
            with open('../examples/' + group_name + '/results/MODEL_' + encoding_result_name + group_name + '_' + experiment + '.txt', 'r') as cur_file:
                decoy = True
                for line in cur_file:
                    match = elapsed.search(line)
                    if match:
                        if decoy:
                            decoy = False
                        else:
                            elapsed_time_model[-1].append(match.group('val1'))
                            found_model = True
        except FileNotFoundError:
            pass
        if not found_diamater:
            diameters[-1].append('-')
        if not found_states:
            reachable_states[-1].append('-')
            total_v1_states[-1].append('-')
        if not found_states_silent:
            elapsed_time_states[-1].append('-')
        if not found_ctl_silent:
            elapsed_time_ctl[-1].append('-')
        if not found_ltl_silent:
            elapsed_time_ltl[-1].append('-')
        if not found_model:
            elapsed_time_model[-1].append('-')
        if not found_resident:
            maximum_resident_ltl[-1].append('-')

print(diameters)

df = pd.DataFrame(diameters, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/diameters.tex', caption=group_name + ', System Diameter', label=group_name + '_diam')

df = pd.DataFrame(reachable_states, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/reachable_states.tex', caption=group_name + ', Reachable States', label=group_name + '_reach')

df = pd.DataFrame(total_v1_states, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/total_states.tex', caption=group_name + ', Total States', label=group_name + '_total')

df = pd.DataFrame(elapsed_time_states, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/elapsed_states.tex', caption=group_name + ', Time in Seconds to Compute Reachability', label=group_name + '_states_time')

df = pd.DataFrame(elapsed_time_ctl, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/elapsed_ctl.tex', caption=group_name + ', Time in Seconds to Compute CTL', label=group_name + '_CTL_time')

df = pd.DataFrame(elapsed_time_ltl, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/elapsed_ltl.tex', caption=group_name + ', Time in Seconds to Compute LTL', label=group_name + '_LTL_time')

df = pd.DataFrame(elapsed_time_model, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/elapsed_model.tex', caption=group_name + ', Time in Seconds to Build Model', label=group_name + '_model_time')

df = pd.DataFrame(maximum_resident_ltl, columns=experiments, index=encodings)
df.to_latex('../examples/' + group_name + '/processed_data/maximum_resident_ltl.tex', caption=group_name + ', Maximum Resident Size in K to Compute LTL', label=group_name + '_LTL_size')

print(len(elapsed_time_ltl))

for i in range(len(encodings)):
    y_range = []
    for x in range(len(experiments)):
        val = elapsed_time_ltl[i][x]
        if val == '-':
            # y_range.append(350)
            y_range.append(-1000)
        else:
            y_range.append(float(val))
    plt.plot(experiments, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1])
plt.ylabel('Time in Seconds')
plt.xlabel('Number of Checks in ' + group_name)
plt.title('Time in Seconds to verify LTL Specs in ' + group_name)
plt.legend(encodings)
plt.tight_layout()
plt.savefig('../examples/' + group_name + '/processed_data/elapsed_ltl.png')

plt.clf()

for i in range(len(encodings)):
    y_range = []
    for x in range(len(experiments)):
        val = maximum_resident_ltl[i][x]
        if val == '-':
            # y_range.append(350)
            y_range.append(-1000)
        else:
            y_range.append(float(val))
    plt.plot(experiments, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1])

plt.ylabel('Maximum Resident Size in K')
plt.xlabel('Number of Checks in ' + group_name)
plt.title('Max Resident Size in K for LTL Specs in ' + group_name)
plt.legend(encodings)
plt.tight_layout()
plt.savefig('../examples/' + group_name + '/processed_data/memory_ltl.png')
