import sys


experiment_name = None
python_file = None
haskell_file = None
smv_file = None
opt_smv_file = None

if len(sys.argv) <= 3:
    print('only python file. exiting')
    sys.exit()
elif len(sys.argv) == 4:
    experiment_name = sys.argv[1]
    python_file = sys.argv[2]
    haskell_file = sys.argv[3]
    smv_file = None
    opt_smv_file = None
elif len(sys.argv) == 5:
    experiment_name = sys.argv[1]
    python_file = sys.argv[2]
    haskell_file = None
    smv_file = sys.argv[3]
    opt_smv_file = sys.argv[4]
elif len(sys.argv) >= 6:
    experiment_name = sys.argv[1]
    python_file = sys.argv[2]
    haskell_file = sys.argv[5]
    smv_file = sys.argv[3]
    opt_smv_file = sys.argv[4]
use_haskell = haskell_file is not None
use_nuxmv = smv_file is not None
use_python = python_file is not None

nodes = set()
variables = set()

def normalize_var_name(cur_var_name):
    # return cur_var_name.replace('_', '').upper().replace('BOARD', '').replace('ENV', '')
    cur_var_name = cur_var_name.replace('_', '').upper()
    scope = 'LOCAL' if 'LOCAL' in cur_var_name else ('BL' if 'BL' in cur_var_name else 'ENV')
    model = 'FROZENVAR' if 'FROZENVAR' in cur_var_name else ('VAR' if 'VAR' in cur_var_name else 'DEFINE')
    return scope + model + (cur_var_name.split(model)[1])

python_run = []
if python_file is not None:
    with open(python_file, 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.strip()
            if 'State after tick:' in line:
                python_run.append({})
            elif '->' in line:
                status = line.split('->')[1]
                status = status.strip()
                status = status.lower()
                node_name = line.split('->')[0]
                node_name = node_name.strip()
                python_run[-1][node_name] = status
                nodes.add(node_name)
            elif ':' in line:
                var_name = line.split(':')[0]
                var_name = var_name.strip()
                var_name = normalize_var_name(var_name)
                var_val = line.split(':')[1]
                var_val = var_val.strip().upper().replace('\'', '').replace('"', '')
                python_run[-1][var_name] = var_val
                variables.add(var_name)

nuxmv_run = []
arrays_to_build = {}
if smv_file is not None:
    with open(smv_file, 'r', encoding = 'utf-8') as f:
        ignore = True
        max_stage = {}
        for line in f:
            line.strip()
            if 'State: ' in line:
                if len(nuxmv_run) > 0:
                    for array_name in arrays_to_build:
                        cur_array = []
                        for index in range(len(arrays_to_build[array_name])):
                            cur_array.append(arrays_to_build[array_name][index])
                        nuxmv_run[-1][array_name] = '[' + ', '.join(cur_array) + ']'
                nuxmv_run.append({})
                arrays_to_build = {}
                ignore = False
            elif not ignore:
                line = line.replace('system.', '')
                if '.status' in line:
                    node_name = line.split('.status')[0].strip()
                    # print(line)
                    # print(node_name)
                    status = line.split('=')[-1].strip()
                    nuxmv_run[-1][node_name] = status
                elif '_stage_' in line:
                    var_name_stage = line.split('=')[0]
                    var_name_stage = var_name_stage.strip()
                    index = -1
                    if '_index_' in line:
                        (var_name_stage, index) = var_name_stage.split('_index_')
                        index = int(index)
                    elif '[' in var_name_stage:
                        (var_name_stage, index) = var_name_stage.split('[')
                        index = index.replace(']', '')
                        index = int(index)
                    var_name = var_name_stage.split('_stage_')[0]
                    var_name = var_name.strip()
                    var_name = normalize_var_name(var_name)
                    var_stage = var_name_stage.split('_stage_')[1]
                    var_stage = var_stage.strip()
                    var_stage = int(var_stage)
                    var_val = line.split('=')[1]
                    var_val = var_val.strip().upper().replace('\'', '').replace('"', '')
                    if index >= 0:
                        if var_name in max_stage:
                            if var_stage >= max_stage[var_name]:
                                max_stage[var_name] = var_stage
                                if var_name in arrays_to_build:
                                    arrays_to_build[var_name][index] = var_val
                                else:
                                    arrays_to_build[var_name] = {index : var_val}
                            else:
                                pass
                        else:
                            max_stage[var_name] = var_stage
                            if var_name in arrays_to_build:
                                arrays_to_build[var_name][index] = var_val
                            else:
                                arrays_to_build[var_name] = {index : var_val}
                    else:
                        if var_name in max_stage:
                            if var_stage >= max_stage[var_name]:
                                max_stage[var_name] = var_stage
                                nuxmv_run[-1][var_name] = var_val
                            else:
                                pass
                        else:
                            max_stage[var_name] = var_stage
                            nuxmv_run[-1][var_name] = var_val
nuxmv_max_stage = 0 if smv_file is None else max_stage


opt_nuxmv_run = []
arrays_to_build = {}
if opt_smv_file is not None:
    with open(opt_smv_file, 'r', encoding = 'utf-8') as f:
        ignore = True
        max_stage = {}
        for line in f:
            line.strip()
            if 'State: ' in line:
                if len(opt_nuxmv_run) > 0:
                    for array_name in arrays_to_build:
                        cur_array = []
                        for index in range(len(arrays_to_build[array_name])):
                            cur_array.append(arrays_to_build[array_name][index])
                        opt_nuxmv_run[-1][array_name] = '[' + ', '.join(cur_array) + ']'
                opt_nuxmv_run.append({})
                arrays_to_build = {}
                ignore = False
            elif not ignore:
                line = line.replace('system.', '')
                if '.status' in line:
                    node_name = line.split('.status')[0].strip()
                    # print(line)
                    # print(node_name)
                    status = line.split('=')[-1].strip()
                    opt_nuxmv_run[-1][node_name] = status
                elif '_stage_' in line:
                    var_name_stage = line.split('=')[0]
                    var_name_stage = var_name_stage.strip()
                    index = -1
                    if '_index_' in line:
                        (var_name_stage, index) = var_name_stage.split('_index_')
                        index = int(index)
                    elif '[' in var_name_stage:
                        (var_name_stage, index) = var_name_stage.split('[')
                        index = index.replace(']', '')
                        index = int(index)
                    var_name = var_name_stage.split('_stage_')[0]
                    var_name = var_name.strip()
                    var_name = normalize_var_name(var_name)
                    var_stage = var_name_stage.split('_stage_')[1]
                    var_stage = var_stage.strip()
                    var_stage = int(var_stage)
                    var_val = line.split('=')[1]
                    var_val = var_val.strip().upper().replace('\'', '').replace('"', '')
                    if index >= 0:
                        if var_name in max_stage:
                            if var_stage >= max_stage[var_name]:
                                max_stage[var_name] = var_stage
                                if var_name in arrays_to_build:
                                    arrays_to_build[var_name][index] = var_val
                                else:
                                    arrays_to_build[var_name] = {index : var_val}
                            else:
                                pass
                        else:
                            max_stage[var_name] = var_stage
                            if var_name in arrays_to_build:
                                arrays_to_build[var_name][index] = var_val
                            else:
                                arrays_to_build[var_name] = {index : var_val}
                    else:
                        if var_name in max_stage:
                            if var_stage >= max_stage[var_name]:
                                max_stage[var_name] = var_stage
                                opt_nuxmv_run[-1][var_name] = var_val
                            else:
                                pass
                        else:
                            max_stage[var_name] = var_stage
                            opt_nuxmv_run[-1][var_name] = var_val
opt_nuxmv_max_stage = 0 if opt_smv_file is None else max_stage

haskell_run = []
arrays_to_build = {}
if haskell_file is not None:
    with open(haskell_file, 'r', encoding = 'utf-8') as f:
        ignore_initial_state = True
        for line in f:
            arrays_to_build = {}
            if ignore_initial_state:
                ignore_initial_state = False
                continue
            line.strip()
            haskell_run.append({})
            line = line.replace('(Board = {', '').replace('Env = {', ' ').replace('})', '').replace('}', '')
            for var_and_val in line.split(','):
                var_and_val.strip()
                if ':' not in var_and_val:
                    continue
                (var_name, var_val) = var_and_val.split(':')
                var_val = var_val.strip().upper().replace('\'', '').replace('"', '')
                var_name = var_name.strip()
                var_name = normalize_var_name(var_name)
                if 'INDEX' in var_name:
                    (var_name, index) = var_name.split('INDEX')
                    if var_name in arrays_to_build:
                        arrays_to_build[var_name][int(index)] = var_val
                    else:
                        arrays_to_build[var_name] = {int(index) : var_val}
                haskell_run[-1][var_name] = var_val
            for var_name in arrays_to_build:
                # new_array = list(map(lambda index: arrays_to_build[var_name][index], range(len(arrays_to_build[var_name]))))
                haskell_run[-1][var_name] = '[' + ', '.join(map(lambda index: arrays_to_build[var_name][index], range(len(arrays_to_build[var_name])))) + ']'

# print(opt_nuxmv_run)
# print(len(opt_nuxmv_run))
print('-----------------------------' + experiment_name + '-----------------------------')
if use_python and len(python_run) < 10:
    print('Comparison failure! Not enough python ticks')
    sys.exit()
if use_nuxmv and len(nuxmv_run) < 10:
    print('Comparison failure! Not enough nuXmv ticks')
    sys.exit()
if use_nuxmv and len(opt_nuxmv_run) < 10:
    print('Comparison failure! Not enough opt_nuxmv ticks')
    sys.exit()
if use_haskell and len(haskell_run) < 10:
    print('Comparison failure! Not enough haskell ticks')
    sys.exit()

# print(nuxmv_run[0])
# print(opt_nuxmv_run[0])
for tick in range(len(python_run)):
    try:
        python_tick = python_run[tick] if use_python else []
        nuxmv_tick = nuxmv_run[tick] if use_nuxmv else []
        opt_nuxmv_tick = opt_nuxmv_run[tick] if use_nuxmv else []
        haskell_tick = haskell_run[tick] if use_haskell else []
        for item in python_tick:
            # compare python tick to nuxmv tick
            if use_nuxmv:
                if item not in nuxmv_tick:
                    # if something is missing, that's bad
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(python_tick[item]) + ' was in python_tick but not in nuxmv_tick')
                        sys.exit()
                elif python_tick[item] != nuxmv_tick[item]:
                    # if something doesn't match, that's bad
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(python_tick[item]) + ' in python_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
            if use_haskell:
                if item in variables and item not in haskell_tick:
                    if 'LOCAL' in item or 'DEFINE' in item:
                        pass
                    else:
                        # if something is missing, that's bad
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(python_tick[item]) + ' was in python_tick but not in haskell_tick')
                        sys.exit()
                elif item in variables and haskell_tick[item] != python_tick[item]:
                    # if something doesn't match, that's bad
                    print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(python_tick[item]) + ' in python_tick but ' + str(haskell_tick[item]) + ' in haskell_tick')
                    sys.exit()
        for item in nuxmv_tick:
            # compare nuxmv tick to python tick, then nuxmv tick to nuxmv opt tick
            if use_python:
                if item not in python_tick:
                    # if something is missing, that's bad
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(nuxmv_tick[item]) + ' was in nuxmv_tick but not in python_tick')
                        sys.exit()
                elif python_tick[item] != nuxmv_tick[item]:
                    # if something doesn't match, that's bad
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(python_tick[item]) + ' in python_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
            if item not in opt_nuxmv_tick:
                # if something is missing, that MIGHT be bad.
                if item in variables:
                    if 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        # if it's a variable, that's bad. we shouldn't have fully eliminated any variables.
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(nuxmv_tick[item]) + ' was in nuxmv_tick but not in opt_nuxmv_tick')
                        sys.exit()
                elif nuxmv_tick[item] != 'invalid' and item[0] in {'c', 'a'}:
                    # if it's a node and not invalid, that's bad. (invalid nodes may have reasonably been pruned. no cause for alarm)
                    # jk, we can trim composite nodes that aren't invalid because they have only one child. verify that it is a leaf node that differs.
                    print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(nuxmv_tick[item]) + ' was in nuxmv_tick but not in opt_nuxmv_tick')
                    sys.exit()
            elif nuxmv_tick[item] != opt_nuxmv_tick[item]:
                # if something doesn't match, that MIGHT be bad
                if item in nodes:
                    # if a node doesn't match, that's bad for sure
                    print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                    sys.exit()
                elif not (item in nuxmv_max_stage and item in opt_nuxmv_max_stage):
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        # if a variable doesn't match and we don't have stage info on it, that's bad
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
                elif opt_nuxmv_max_stage[item] >= nuxmv_max_stage[item]:
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        # if a variable doesn't match and we DIDN'T prune the last stage, that's bad.
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
        for item in opt_nuxmv_tick:
            # now we compare opt_nuxmv to nuxmv
            if item not in nuxmv_tick:
                # if an item is in opt but not nuxmv, something has gone pretty seriously wrong
                print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(opt_nuxmv_tick[item]) + ' was in opt_nuxmv_tick but not in nuxmv_tick')
                sys.exit()
            elif opt_nuxmv_tick[item] != nuxmv_tick[item]:
                # if an item doesn't match, that might be fine. might just means pruning occured
                if item in nodes:
                    # if a node doesn't match, that's bad for sure
                    print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                    sys.exit()
                elif not (item in nuxmv_max_stage and item in opt_nuxmv_max_stage):
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        # if a variable doesn't match and we don't have stage info on it, that's bad
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
                elif opt_nuxmv_max_stage[item] >= nuxmv_max_stage[item]:
                    if item in variables and 'DEFINE' in item:
                        # nuxmv version might not have defined the macro
                        pass
                    else:
                        # if a variable doesn't match and we DIDN'T prune the last stage, that's bad.
                        print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(opt_nuxmv_tick[item]) + ' in opt_nuxmv_tick but ' + str(nuxmv_tick[item]) + ' in nuxmv_tick')
                        sys.exit()
        for item in haskell_tick:
            if item not in python_tick:
                if 'LOCAL' in item or 'DEFINE' in item:
                    pass
                else:
                    # if something is missing, that's bad
                    print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + str(haskell_tick[item]) + ' was in haskell_tick but not in python_tick')
                    sys.exit()
            elif haskell_tick[item] != python_tick[item]:
                # if something doesn't match, that's bad
                print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + str(python_tick[item]) + ' in python_tick but ' + str(haskell_tick[item]) + ' in haskell_tick')
                sys.exit()
        # we don't comapre opt_nuxmv to python, it's too complicated and requires too many strange things. besisdes, by transitivity, it should be fine.
    except Exception as e:
        print('Comparison failure! Reached unexpected error')
        print(str(e))
        sys.exit()
