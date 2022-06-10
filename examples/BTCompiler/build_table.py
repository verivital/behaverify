#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import re

#folders = ["./models_selector_mixed", "./models_selector_parallel", "./models_selector_non_parallel", "./models_sequence",  "./models_path", "./models_path"]
#folders2 = ["selector_mixed", "selector_parallel", "selector_non_parallel",  "sequence", "path", "double_path", "double_path_clean", "double_path_cleaner", "double_path_ivar", "total"]
folders2 = ["BTCompiler", "double_path", "double_path_clean", "double_path_cleaner", "double_path_ivar", "total"]
files = ["serene_uc1"]

#foldersShort = ["SelMixed", "SelParallel", "SelNonParallel", "Sequence", "Path", "Double Path", "D P Clean", "D P Cleaner", "D P IVAR", "Total"]
foldersShort = ["BTCompiler", "Double Path", "D P Clean", "D P Cleaner", "D P IVAR", "Total"]
filesShort = ["uc1"]

#diameters = {}
#reachable_states = {}
#total_states = {}
diameters = []
reachable_states = []
total_states = []
reach=re.compile("reachable states: (?P<val1>\d+(\.\d+e\+\d+|)) \(2\^(?P<val2>\d+(\.\d+|))\) out of (?P<val3>\d+(\.\d+e\+\d+|)) \(2\^(?P<val4>\d+(\.\d+|))\)")

#for file_name in files:
for i in range(len(files)):
    file_name = files[i]
    diameters.append([])
    total_states.append([])
    reachable_states.append([])
    # diameters[file_name]={}
    # reachable_states[file_name]={}
    # total_states[file_name]={}
    # for folder in folders2:
    for j in range(len(folders2)):
        folder = folders2[j]
        with open('./models_' + folder + '/results/' + file_name + '.smv_states.txt', 'r') as cur_file:
            for line in cur_file:
                if "system diameter:" in line:
                    val=line.split(':')[1]
                    val=int(val.strip())
                    diameters[i].append(val)
                    #diameters[file_name][folder] = val
                match=reach.search(line)
                if match:
                    #reachable_states[file_name][folder]=int(match.group('val1'))
                    #total_states[file_name][folder]=int(match.group('val3'))
                    
                    #reachable_states[i].append(int(match.group('val1')))
                    #total_states[i].append(int(match.group('val3')))
                    reachable_states[i].append(match.group('val1'))
                    total_states[i].append(match.group('val3'))

                    
                    #vals_reachable_pow.append(float(match.group('val2')))
                    #vals_total_pow.append(float(match.group('val4')))


df = pd.DataFrame(diameters, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/diameters.tex', caption='Basic Examples, System Diameter', label='b_e_diam')

df = pd.DataFrame(reachable_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/reachable_states.tex', caption='Basic Examples, Reachable States', label='b_e_reach')


df = pd.DataFrame(total_states, columns=foldersShort, index=filesShort)
df.to_latex('./processed_data/total_states.tex', caption='Basic Examples, Total States', label='b_e_total')
