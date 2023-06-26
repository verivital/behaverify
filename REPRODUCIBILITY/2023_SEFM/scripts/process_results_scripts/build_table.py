# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import argparse
# import os

def write_table(_data, _experiments, _encodings, _encoding_code, _file_name, _caption, _group_name, _label):
    if mins == maxs:
        # print(_data)
        flattened = [d[0] for d in _data]
        # print(flattened)
        #df = pd.DataFrame([flattened], columns=_encodings, index=None)
        df = pd.DataFrame([flattened], columns=_encodings, index=None)
        #df = pd.DataFrame(_data, columns=_encodings, index=['no'])
        df.to_latex(PATH_DIRECTION + _group_name + '/processed_data/tables/' + _encoding_code + '/' + _file_name, caption=_caption, label=_label, index=False)
    else:
        df = pd.DataFrame(_data, columns=_experiments, index=_encodings)
        df.to_latex(PATH_DIRECTION + _group_name + '/processed_data/tables/' + _encoding_code + '/' + _file_name, caption=_caption, label=_label)

PATH_DIRECTION = '../../examples/'

encoding_combo = {
    'all' : ['aut', 'aut_s', 'depth', 'func', 'norm', 'no_internal', 's_var'],
    'internal' : ['norm', 'no_internal', 's_var'],
    'core' : ['aut', 'aut_s', 'norm'],
    'aut' : ['aut', 'aut_s'],
    'func' : ['func', 'norm', 'no_internal', 's_var'],
    'invar' : ['aut', 'func', 'norm', 'no_internal', 's_var'],
    'opt' : ['no_opt', 'last_opt', 'first_opt', 'full_opt']
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
    'full_opt' : 'full_opt_'
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
    'full_opt' : ('yellow', '*'),
}

reach = re.compile('reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)')
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
    #print(encoding_code)
    encodings = encoding_combo[encoding_code]
    for i in range(max(len(folder_names), len(file_names), len(mins), len(maxs), len(steps), len(encoding_codes))):
        group_name = folder_names[i if i < len(folder_names) else -1]
        file_name = file_names[i if i < len(file_names) else -1]
        experiments = list(map(str, range(mins[i if i < len(mins) else -1], maxs[i if i < len(maxs) else -1] + 1, steps[i if i < len(steps) else -1])))
        xLabel = args.xLabel[i if i < len(args.xLabel) else -1]

        diameters = []
        reachable_states = []
        total_v1_states = []
        elapsed_time_ltl = []
        elapsed_time_ctl = []
        elapsed_time_invar = []
        elapsed_time_compute_reachable = []
        elapsed_time_print_states = []
        elapsed_time_model = []
        maximum_resident_ltl = []
        maximum_resident_ctl = []
        maximum_resident_invar = []
        skip_diamater = True
        skip_print_states = True
        skip_time_states = True
        skip_compute_reachable = True
        skip_ctl_silent = True
        skip_ltl_silent = True
        skip_invar_silent = True
        skip_model = True
        skip_ltl_resident = True
        skip_ctl_resident = True
        skip_invar_resident = True

        for encoding_name in encodings:
            encoding_result_name = encoding_name_to_result_name[encoding_name]

            diameters.append([])
            total_v1_states.append([])
            reachable_states.append([])
            elapsed_time_ltl.append([])
            elapsed_time_ctl.append([])
            elapsed_time_invar.append([])
            elapsed_time_compute_reachable.append([])
            elapsed_time_print_states.append([])
            elapsed_time_model.append([])
            maximum_resident_ltl.append([])
            maximum_resident_ctl.append([])
            maximum_resident_invar.append([])
            for experiment in experiments:
                found_diamater = False
                found_print_states = False
                found_time_states = False
                found_compute_reachable = False
                found_ctl_silent = False
                found_ltl_silent = False
                found_invar_silent = False
                found_model = False
                found_ltl_resident = False
                found_ctl_resident = False
                found_invar_resident = False
                try:
                    with open(PATH_DIRECTION + group_name + '/results/STATES_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        decoy = True
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
                                found_print_states = True
                            match = elapsed.search(line)
                            if match:
                                if decoy:
                                    decoy = False
                                else:
                                    elapsed_time_print_states[-1].append(match.group('val1'))
                                    found_time_states = True
                except FileNotFoundError:
                    pass
                try:
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_STATES_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        decoy = True
                        for line in cur_file:
                            match = elapsed.search(line)
                            if match:
                                if decoy:
                                    decoy = False
                                else:
                                    elapsed_time_compute_reachable[-1].append(match.group('val1'))
                                    found_compute_reachable = True
                except FileNotFoundError:
                    pass
                try:
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_CTL_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        decoy = True
                        for line in cur_file:
                            match = elapsed.search(line)
                            if match:
                                if decoy:
                                    decoy = False
                                else:
                                    elapsed_time_ctl[-1].append(match.group('val1'))
                                    found_ctl_silent = True
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_CTL_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        # decoy = True
                        for line in cur_file:
                            # print(line)
                            match = resident.search(line)
                            if match:
                                # if decoy:
                                #     decoy = False
                                # else:
                                maximum_resident_ctl[-1].append(match.group('val1'))
                                found_ctl_resident = True
                except FileNotFoundError:
                    pass
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
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_LTL_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        # decoy = True
                        for line in cur_file:
                            # print(line)
                            match = resident.search(line)
                            if match:
                                # if decoy:
                                #     decoy = False
                                # else:
                                maximum_resident_ltl[-1].append(match.group('val1'))
                                found_ltl_resident = True
                except FileNotFoundError:
                    pass
                try:
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_INVAR_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        decoy = True
                        for line in cur_file:
                            match = elapsed.search(line)
                            if match:
                                if decoy:
                                    decoy = False
                                else:
                                    elapsed_time_invar[-1].append(match.group('val1'))
                                    found_invar_silent = True
                    with open(PATH_DIRECTION + group_name + '/results/SILENT_INVAR_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
                        # decoy = True
                        for line in cur_file:
                            # print(line)
                            match = resident.search(line)
                            if match:
                                # if decoy:
                                #     decoy = False
                                # else:
                                maximum_resident_invar[-1].append(match.group('val1'))
                                found_invar_resident = True
                except FileNotFoundError:
                    pass
                try:
                    with open(PATH_DIRECTION + group_name + '/results/MODEL_' + encoding_result_name + file_name + '_' + experiment + '.txt', 'r') as cur_file:
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
                else:
                    skip_diamater = False
                if not found_print_states:
                    reachable_states[-1].append('-')
                    total_v1_states[-1].append('-')
                else:
                    skip_print_states = False
                if not found_time_states:
                    elapsed_time_print_states[-1].append('-')
                else:
                    skip_time_states = False
                if not found_compute_reachable:
                    elapsed_time_compute_reachable[-1].append('-')
                else:
                    skip_compute_reachable = False
                if not found_ctl_silent:
                    elapsed_time_ctl[-1].append('-')
                else:
                    skip_ctl_silent = False
                if not found_ltl_silent:
                    elapsed_time_ltl[-1].append('-')
                else:
                    skip_ltl_silent = False
                if not found_invar_silent:
                    elapsed_time_invar[-1].append('-')
                else:
                    skip_invar_silent = False
                if not found_model:
                    elapsed_time_model[-1].append('-')
                else:
                    skip_model = False
                if not found_ltl_resident:
                    maximum_resident_ltl[-1].append('-')
                else:
                    skip_ltl_resident = False
                if not found_ctl_resident:
                    maximum_resident_ctl[-1].append('-')
                else:
                    skip_ctl_resident = False
                if not found_invar_resident:
                    maximum_resident_invar[-1].append('-')
                else:
                    skip_invar_resident = False

        # print(diameters)

        escaped_encodings = list(map(lambda x: x.replace('_', '\_'), encodings))
        escaped_file_name = file_name.replace('_', '\_')

        if not skip_diamater:
            df = pd.DataFrame(diameters, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_diameters.tex', caption=escaped_file_name + ', System Diameter', label=file_name + '_diam')

        if not skip_print_states:
            write_table(reachable_states, experiments, escaped_encodings, encoding_code, file_name + '_reachable_states.tex', escaped_file_name + ', Reachable States', group_name, file_name + '_reach')
            # df = pd.DataFrame(reachable_states, columns=experiments, index=escaped_encodings)
            # df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_reachable_states.tex', caption=escaped_file_name + ', Reachable States', label=file_name + '_reach')

            df = pd.DataFrame(total_v1_states, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_total_states.tex', caption=escaped_file_name + ', Total States', label=file_name + '_total')
        if not skip_time_states:
            df = pd.DataFrame(elapsed_time_print_states, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_print_states.tex', caption=escaped_file_name + ', Time in Seconds to Print Reachability', label=file_name + '_states_time')

        if not skip_compute_reachable:
            df = pd.DataFrame(elapsed_time_compute_reachable, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_reachable.tex', caption=escaped_file_name + ', Time in Seconds to Compute Reachability', label=file_name + '_states_time')

        if not skip_ctl_silent:
            df = pd.DataFrame(elapsed_time_ctl, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_ctl.tex', caption=escaped_file_name + ', Time in Seconds to Compute CTL', label=file_name + '_CTL_time')

        if not skip_ltl_silent:
            df = pd.DataFrame(elapsed_time_ltl, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_ltl.tex', caption=escaped_file_name + ', Time in Seconds to Compute LTL', label=file_name + '_LTL_time')

        if not skip_invar_silent:
            write_table(elapsed_time_invar, experiments, escaped_encodings, encoding_code, file_name + '_elapsed_invar.tex', escaped_file_name + ', Time in Seconds to Compute INVAR', group_name, file_name + '_INVAR_time')
            # df = pd.DataFrame(elapsed_time_invar, columns=experiments, index=escaped_encodings)
            # df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_invar.tex', caption=escaped_file_name + ', Time in Seconds to Compute INVAR', label=file_name + '_INVAR_time')

        if not skip_model:
            df = pd.DataFrame(elapsed_time_model, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_elapsed_model.tex', caption=escaped_file_name + ', Time in Seconds to Build Model', label=file_name + '_model_time')

        if not skip_ltl_resident:
            df = pd.DataFrame(maximum_resident_ltl, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_maximum_resident_ltl.tex', caption=escaped_file_name + ', Maximum Resident Size in K to Compute LTL', label=file_name + '_LTL_size')

        if not skip_ctl_resident:
            df = pd.DataFrame(maximum_resident_ctl, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_maximum_resident_ctl.tex', caption=escaped_file_name + ', Maximum Resident Size in K to Compute CTL', label=file_name + '_CTL_size')

        if not skip_invar_resident:
            df = pd.DataFrame(maximum_resident_invar, columns=experiments, index=escaped_encodings)
            df.to_latex(PATH_DIRECTION + group_name + '/processed_data/tables/' + encoding_code + '/' + file_name + '_maximum_resident_invar.tex', caption=escaped_file_name + ', Maximum Resident Size in K to Compute INVAR', label=file_name + '_INVAR_size')

        # print(len(elapsed_time_ltl))

        for (thing, skip) in [
                ('diameters', skip_diamater),
                ('reachable', skip_compute_reachable),
                ('total', skip_compute_reachable),
                ('print', skip_print_states),
                ('compute', skip_compute_reachable),
                ('ctl', skip_ctl_silent),
                ('ltl', skip_ltl_silent),
                ('invar', skip_invar_silent),
                ('model', skip_model),
                ('ctl_r', skip_invar_resident),
                ('ltl_r', skip_ltl_resident),
                ('invar_r', skip_invar_resident)]:
            if skip:
                continue
            if thing == 'diameters':
                data = diameters
                x_label = xLabel
                y_label = 'Diameter of FSM'
                title = 'Diameter of FSM for ' + file_name
                file_end = 'diameter'
                y_default_val = -1000
            elif thing == 'reachable':
                data = reachable_states
                x_label = xLabel
                y_label = 'Reachable States'
                title = 'Reachable States of FSM for ' + file_name
                file_end = 'reachable'
                y_default_val = -1000
            elif thing == 'total':
                data = total_v1_states
                x_label = xLabel
                y_label = 'Total States'
                title = 'Total States of FSM for ' + file_name
                file_end = 'total'
            elif thing == 'print':
                data = elapsed_time_print_states
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to Print States of FSM for ' + file_name
                file_end = 'print'
                y_default_val = -1000
            elif thing == 'compute':
                data = elapsed_time_compute_reachable
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to Compute States of FSM for ' + file_name
                file_end = 'compute'
                y_default_val = -1000
            elif thing == 'ctl':
                data = elapsed_time_ctl
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to verify CTL of FSM for ' + file_name
                file_end = 'ctl'
                y_default_val = -1000
            elif thing == 'ltl':
                data = elapsed_time_ltl
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to verify LTL of FSM for ' + file_name
                file_end = 'ltl'
                y_default_val = -1000
            elif thing == 'invar':
                data = elapsed_time_invar
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to verify INVAR of FSM for ' + file_name
                file_end = 'invar'
                y_default_val = -1000
            elif thing == 'model':
                data = elapsed_time_model
                x_label = xLabel
                y_label = 'Time in Seconds'
                title = 'Time in Seconds to Build Model of FSM for ' + file_name
                file_end = 'model'
                y_default_val = -1000
            elif thing == 'ctl_r':
                data = maximum_resident_ctl
                x_label = xLabel
                y_label = 'Maximum Resident Size in K'
                title = 'Max Resident Size in K for CTL Specs in ' + file_name
                file_end = 'ctl_r'
                y_default_val = -1000
            elif thing == 'ltl_r':
                data = maximum_resident_ltl
                x_label = xLabel
                y_label = 'Maximum Resident Size in K'
                title = 'Max Resident Size in K for LTL Specs in ' + file_name
                file_end = 'ltl_r'
                y_default_val = -1000
            elif thing == 'invar_r':
                data = maximum_resident_invar
                x_label = xLabel
                y_label = 'Maximum Resident Size in K'
                title = 'Max Resident Size in K for INVAR Specs in ' + file_name
                file_end = 'invar_r'
                y_default_val = -1000
            for i in range(len(encodings)):
                x_range = []
                y_range = []
                for x in range(len(experiments)):
                    val = data[i][x]
                    if val == '-':
                        # y_range.append(350)
                        # y_range.append(y_default_val)
                        pass
                    else:
                        x_range.append(experiments[x])
                        y_range.append(float(val))
                # plt.plot(experiments, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1])
                #print(x_range)
                plt.plot(x_range, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1])
            plt.ylabel(y_label)
            plt.xlabel(x_label)
            plt.title(title)
            plt.legend(encodings)
            plt.tight_layout()
            plt.savefig(PATH_DIRECTION + group_name + '/processed_data/pictures/' + encoding_code + '/' + file_name + '_' + file_end + '.png')

            plt.clf()

        # for i in range(len(encodings)):
        #     y_range = []
        #     for x in range(len(experiments)):
        #         val = maximum_resident_ltl[i][x]
        #         if val == '-':
        #             # y_range.append(350)
        #             y_range.append(-1000)
        #         else:
        #             y_range.append(float(val))
        #     plt.plot(experiments, y_range, color = encoding_mark[encodings[i]][0], marker = encoding_mark[encodings[i]][1])

        # plt.ylabel('Maximum Resident Size in K')
        # plt.xlabel('Number of Checks in ' + file_name)
        # plt.title('Max Resident Size in K for LTL Specs in ' + file_name)
        # plt.legend(encodings)
        # plt.tight_layout()
        # plt.savefig(PATH_DIRECTION + group_name + '/processed_data/' + file_name + '_memory_ltl.png')

        # plt.clf()
