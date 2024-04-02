import sys
import os
import onnx
import onnxruntime

input_path = sys.argv[1]
target_path = sys.argv[2]
network_path = sys.argv[3]
min_x = int(sys.argv[4])
max_x = int(sys.argv[5])
min_y = int(sys.argv[6])
max_y = int(sys.argv[7])


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
def argmax(val):
    max_val = max(val)
    for index in range(len(val)):
        if val[index] == max_val:
            return index
    raise Exception
session = onnxruntime.InferenceSession(network_path)
input_name = session.get_inputs()[0].name
cur_count = 0
for start_x in range(min_x, max_x + 1):
    for start_y in range(min_y, max_y + 1):
        for end_x in range(min_x, max_x + 1):
            for end_y in range(min_y, max_y + 1):
                if cur_count % 1000 == 0:
                    print('still running: ', cur_count)
                cur_count += 1
                network_val = session.run(None, {input_name : [[start_x, start_y, end_x, end_y]]})[0][0]
                a_star_val = a_star_dict[(start_x, start_y, end_x, end_y)]
                if argmax(a_star_val) != argmax(network_val):
                    print('-------------------------------')
                    print((start_x, start_y, end_x, end_y))
                    print(a_star_val)
                    print(network_val)

print('---------------------------------------TESTING PATH')
start_x = 7
start_y = 7
end_x = 0
end_y = 2
print('-------------------------------')
print(session.run(None, {input_name : [[start_x, start_y, end_x, end_y]]})[0][0])
print(a_star_dict[(start_x, start_y, end_x, end_y)])
start_x = 7
start_y = 6
end_x = 0
end_y = 2
print('-------------------------------')
print(session.run(None, {input_name : [[start_x, start_y, end_x, end_y]]})[0][0])
print(a_star_dict[(start_x, start_y, end_x, end_y)])
start_x = 6
start_y = 6
end_x = 0
end_y = 2
print('-------------------------------')
print(session.run(None, {input_name : [[start_x, start_y, end_x, end_y]]})[0][0])
print(a_star_dict[(start_x, start_y, end_x, end_y)])
