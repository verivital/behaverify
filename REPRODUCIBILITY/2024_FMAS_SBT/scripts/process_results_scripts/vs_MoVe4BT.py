# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
# import os

PATH_DIRECTION = '../../examples/'

TOOLNAME = 'BehaVerify on Original Tree'
TOOLNAME_changed = 'BehaVerify on MoVe4BT Tree'
COMP1 = 'MoVe4BT'
encoding_combo = {
    'vs' : [TOOLNAME, COMP1],
    'vs_robot' : [TOOLNAME, TOOLNAME_changed, COMP1],
    'vs_bigger_fish' : [TOOLNAME, TOOLNAME_changed, COMP1]
}
encoding_name_to_result_name = {
    'aut' : 'aut_',
    'aut_s' : 'aut_s_',
    'depth' : 'depth_',
    'func' : 'func_',
    'norm' : 'norm_',
    'no_internal' : 'no_internal_',
    's_var' : 's_var_',
    'no_opt' : 'no_opt_',
    'last_opt' : 'last_opt_',
    'first_opt' : 'first_opt_',
    'full_opt' : 'full_opt_',
    TOOLNAME : 'full_opt_',
    TOOLNAME_changed : 'full_opt_CHANGED_',
    COMP1 : 'MoVe4BT_'
}

encoding_mark = {
    'aut' : ('red', 'o'),
    'func' : ('blue', 'v'),
    'norm' : ('green', '^'),
    'no_internal' : ('yellow', '*'),
    'depth' : ('magenta', 'x'),
    'aut_s' : ('black', '.'),
    's_var' : ('tan', '.'),
    # the below and above will never run at the same time. no conflict
    'no_opt' : ('red', 'o'),
    'last_opt' : ('blue', 'v'),
    'first_opt' : ('green', '^'),
    'full_opt' : ('black', '*'),
    TOOLNAME : ('black', '*', '-'),
    TOOLNAME_changed : ('blue', '^', ':'),
    COMP1 : ('green', 'v'),
}

#reach = re.compile('reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)')
reach = re.compile('reachable states: (?P<val1>((\d+)|(\d+(\.\d+)?e\+\d+))) \(2\^((\d+)|(\d+\.\d+))\) out of (?P<val3>((\d+)|(\d+(\.\d+)?e\+\d+))) \(2\^((\d+)|(\d+\.\d+))\)')
elapsed = re.compile('elapse: -?(?P<val1>[\.\d]+) seconds,')
resident = re.compile('Maximum resident size\s*= (?P<val1>[\.\d]+)K')

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--folder_name', nargs = '+')
arg_parser.add_argument('--file_name', nargs = '+')
arg_parser.add_argument('--minV', nargs = '+', type = int)
arg_parser.add_argument('--maxV', nargs = '+', type = int)
arg_parser.add_argument('--step', nargs = '+', type = int)
arg_parser.add_argument('--xLabel', nargs = '+')
arg_parser.add_argument('--encodings', nargs = '+')

args = arg_parser.parse_args()

folder_names = args.folder_name
file_names = args.file_name
mins = args.minV
maxs = args.maxV
steps = args.step
encoding_codes = args.encodings

for encoding_code in encoding_codes:
    encodings = encoding_combo[encoding_code]
    for i in range(max(len(folder_names), len(file_names), len(mins), len(maxs), len(steps), len(encoding_codes))):
        group_name = folder_names[i if i < len(folder_names) else -1]
        file_name = file_names[i if i < len(file_names) else -1]
        experiments = list(map(str, range(mins[i if i < len(mins) else -1], maxs[i if i < len(maxs) else -1] + 1, steps[i if i < len(steps) else -1])))
        xLabel = args.xLabel[i if i < len(args.xLabel) else -1]

        elapsed_time_ltl = []
        skip_ltl_silent = True

        for encoding_name in encodings:
            encoding_result_name = encoding_name_to_result_name[encoding_name]
            elapsed_time_ltl.append([])
            for experiment in experiments:
                found_ltl_silent = False
                try:
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_LTL_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        decoy = True
                        for line in cur_file:
                            match = elapsed.search(line)
                            if match:
                                if decoy:
                                    decoy = False
                                else:
                                    elapsed_time_ltl[-1].append(match.group('val1'))
                                    found_ltl_silent = True
                            if 'Time Used' in line:
                                elapsed_time_ltl[-1].append(line.split(':', 1)[1].split('s', 1)[0].strip())
                                found_ltl_silent = True
                except FileNotFoundError:
                    pass
                if not found_ltl_silent:
                    elapsed_time_ltl[-1].append('-')
                else:
                    skip_ltl_silent = False

        for (thing, skip) in [('ltl', skip_ltl_silent),]:
            if skip:
                continue
            elif thing == 'ltl':
                data = elapsed_time_ltl
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to verify LTL for ' + file_name
                file_end = 'ltl'
                y_default_val = -1000
            for i in range(len(encodings)):
                x_range = []
                y_range = []
                for x in range(len(experiments)):
                    val = data[i][x]
                    if val == '-':
                        pass
                    else:
                        x_range.append(experiments[x])
                        y_range.append(float(val))
                plt.plot(x_range, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1], linestyle = ('solid' if len(encoding_mark[encodings[i]]) < 3 else encoding_mark[encodings[i]][2]))
            plt.ylabel(y_label)
            plt.xlabel(x_label)
            #plt.title(title)
            plt.legend(encodings)
            plt.tight_layout()
            plt.savefig(PATH_DIRECTION + group_name + '/processed_data/pictures/' + file_name + '_' + file_end + '.png', bbox_inches = 'tight')
            print(PATH_DIRECTION + group_name + '/processed_data/pictures/' + file_name + '_' + file_end + '.png')
            plt.clf()
