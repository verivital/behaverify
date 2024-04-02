import sys
import os
import random

input_path = sys.argv[1]
target_path = sys.argv[2]
min_x = int(sys.argv[3])
max_x = int(sys.argv[4])
min_y = int(sys.argv[5])
max_y = int(sys.argv[6])
trials = int(sys.argv[7])


print('loading inputs')
inputs = []
index = 0
with open(input_path, 'r', encoding = 'utf-8') as input_file:
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
with open(target_path, 'r', encoding = 'utf-8') as target_file:
    for line in target_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        targets.append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 10000 == 0:
            print('reading target: ' + str(index))
        index = index + 1

a_star_dict = {tuple(map(int, inputs[index])) : tuple(map(int, targets[index])) for index in range(len(inputs))}
dir_to_delta = {
    (1, 0, 0, 0, 0) : (-1, 0),
    (0, 1, 0, 0, 0) : (1, 0),
    (0, 0, 1, 0, 0) : (0, 1),
    (0, 0, 0, 1, 0) : (0, -1),
    (0, 0, 0, 0, 1) : (0, 0)
}
for index in range(trials):
    start_x = random.randint(min_x, max_x)
    start_y = random.randint(min_y, max_y)
    end_x = random.randint(min_x, max_x)
    end_y = random.randint(min_y, max_y)
    print('-------------------------------')
    print((start_x, start_y, end_x, end_y))
    while start_x != end_x or start_y != end_y:
        (d_x, d_y) = dir_to_delta[a_star_dict[(start_x, start_y, end_x, end_y)]]
        start_x += d_x
        start_y += d_y
        print((start_x, start_y, end_x, end_y))
        if d_x == 0 and d_y == 0:
            print('NO ACTION LOOP')
            break
