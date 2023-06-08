import sys

experiment_name = sys.argv[1]
python_file = sys.argv[2]
smv_file = sys.argv[3]

python_run = []
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
        elif ':' in line:
            var_name = line.split(':')[0]
            var_name = var_name.strip()
            var_val = line.split(':')[1]
            var_val = var_val.strip()
            python_run[-1][var_name] = var_val

nuxmv_run = []
with open(smv_file, 'r', encoding = 'utf-8') as f:
    ignore = True
    for line in f:
        line.strip()
        if 'State: ' in line:
            nuxmv_run.append({})
            max_stage = {}
            ignore = False
        if not ignore:
            if '.status' in line:
                node_name = line.split('.status')[0].strip()
                # print(line)
                # print(node_name)
                status = line.split('=')[-1].strip()
                nuxmv_run[-1][node_name] = status
            elif '_stage_' in line:
                var_name_stage = line.split('=')[0]
                var_name_stage = var_name_stage.strip()
                var_name = var_name_stage.split('_stage_')[0]
                var_name = var_name.strip()
                var_stage = var_name_stage.split('_stage_')[1]
                var_stage = var_stage.strip()
                var_stage = int(var_stage)
                var_val = line.split('=')[1]
                var_val = var_val.strip()
                if var_name in max_stage:
                    if var_stage > max_stage[var_name]:
                        max_stage[var_name] = var_stage
                        nuxmv_run[-1][var_name] = var_val
                    else:
                        pass
                else:
                    max_stage[var_name] = var_stage
                    nuxmv_run[-1][var_name] = var_val


print('-----------------------------' + experiment_name + '-----------------------------')

for tick in range(len(python_run)):
    python_tick = python_run[tick]
    nuxmv_tick = nuxmv_run[tick]
    for item in python_tick:
        if item not in nuxmv_tick:
            print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + python_tick[item] + ' was in python_tick but not in nuxmv_tick')
            print(nuxmv_tick)
            print(python_tick)
            sys.exit()
        elif python_tick[item] != nuxmv_tick[item]:
            print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + python_tick[item] + ' in python_tick but ' + nuxmv_tick[item] + ' in nuxmv_tick')
            sys.exit()
    for item in nuxmv_tick:
        if item not in python_tick:
            print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' with value ' + nuxmv_tick[item] + ' was in nuxmv_tick but not in python_tick')
            sys.exit()
        elif python_tick[item] != nuxmv_tick[item]:
            print('Comparison failure! After tick ' + str(tick + 1) + ', ' + item + ' was ' + python_tick[item] + ' in python_tick but ' + nuxmv_tick[item] + ' in nuxmv_tick')
            sys.exit()
