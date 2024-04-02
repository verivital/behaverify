import sys
import os
import random
import time

input_path_a = sys.argv[1]
target_path_a = sys.argv[2]
input_path_b = sys.argv[3]
target_path_b = sys.argv[4]
min_x = int(sys.argv[5])
max_x = int(sys.argv[6])
min_y = int(sys.argv[7])
max_y = int(sys.argv[8])


print('loading inputs')
inputs = []
index = 0
with open(input_path_a, 'r', encoding = 'utf-8') as input_file:
    for line in input_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        inputs.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 10000 == 0:
            print('reading input: ' + str(index))
        index = index + 1

print('loading targets')
targets = []
index = 0
with open(target_path_a, 'r', encoding = 'utf-8') as target_file:
    for line in target_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        targets.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 10000 == 0:
            print('reading target: ' + str(index))
        index = index + 1

a_star_dict_a = {tuple(map(int, inputs[index])) : tuple(map(int, targets[index])) for index in range(len(inputs))}
print('loading inputs')
inputs = []
index = 0
with open(input_path_b, 'r', encoding = 'utf-8') as input_file:
    for line in input_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        inputs.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 10000 == 0:
            print('reading input: ' + str(index))
        index = index + 1

print('loading targets')
targets = []
index = 0
with open(target_path_b, 'r', encoding = 'utf-8') as target_file:
    for line in target_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        targets.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 10000 == 0:
            print('reading target: ' + str(index))
        index = index + 1
a_star_dict_b = {tuple(map(int, inputs[index])) : tuple(map(int, targets[index])) for index in range(len(inputs))}
dir_to_delta = {
    (1, 0, 0, 0, 0) : (-1, 0),
    (0, 1, 0, 0, 0) : (1, 0),
    (0, 0, 1, 0, 0) : (0, 1),
    (0, 0, 0, 1, 0) : (0, -1),
    (0, 0, 0, 0, 1) : (0, 0)
}
def calculate_path_length(a_star_dict, cur_x, cur_y, dest_x, dest_y, test):
    cur_dir = dir_to_delta[a_star_dict[(cur_x, cur_y, dest_x, dest_y)]]
    # print(test + ': ' + str(cur_dir))
    if cur_x == dest_x and cur_y == dest_y:
        return 0
    if cur_dir[0] == 0 and cur_dir[1] == 0:
        return -1
    return (1 + calculate_path_length(a_star_dict, cur_x + cur_dir[0], cur_y + cur_dir[1], dest_x, dest_y, test))
for start_x in range(min_x, max_x + 1):
    for start_y in range(min_y, max_y + 1):
        for end_x in range(min_x, max_x + 1):
            for end_y in range(min_y, max_y + 1):
                dist_a = calculate_path_length(a_star_dict_a, start_x, start_y, end_x, end_y, 'a')
                dist_b = calculate_path_length(a_star_dict_b, start_x, start_y, end_x, end_y, 'b')
                if dist_a != dist_b:
                    print('----------------------------------')
                    print(((start_x, start_y), (end_x, end_y)))
                    print('dist a: ', dist_a)
                    print('dist b: ', dist_b)
