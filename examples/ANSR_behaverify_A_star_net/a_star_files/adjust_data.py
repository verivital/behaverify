import sys
import os
import importlib.util
import torch
import torch.nn as nn
import torch.optim as optim
import random

input_path = sys.argv[1]
target_path = sys.argv[2]



print('loading inputs')
inputs = []
index = 0
with open(input_path, 'r', encoding = 'utf-8') as input_file:
    for line in input_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        inputs.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 1000 == 0:
            print('reading input: ' + str(index))
        index = index + 1

print('loading targets')
targets = []
index = 0
with open(target_path, 'r', encoding = 'utf-8') as target_file:
    for line in target_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        targets.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 1000 == 0:
            print('reading target: ' + str(index))
        index = index + 1

for index in range(len(inputs)):
    if targets[index][-1] == 1.0:
        continue
    
