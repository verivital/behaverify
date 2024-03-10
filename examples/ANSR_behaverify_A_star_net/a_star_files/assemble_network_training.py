import sys
from generate_obstacles import generate_obstacles
from generate_data import generate_sets

number_of_obstacles = int(sys.argv[1])
min_val = int(sys.argv[2])
max_val = int(sys.argv[3])
max_size = int(sys.argv[4])
epochs = int(sys.argv[5])
generate_obstacles(number_of_obstacles, min_val, max_val, max_size)
(left, right, up, down, no_action) = generate_sets(min_val, max_val, 'ignore/obstacles_' + str(number_of_obstacles) + '_' + str(min_val) + '_' + str(max_val) + '_' + str(max_size) + '.txt')

with open('ignore/train_' + str(number_of_obstacles) + '_' + str(min_val) + '_' + str(max_val) + '_' + str(max_size) + '.py', 'w', encoding = 'utf-8') as output_file:
    with open('template.py', 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    template = template.replace('REPLACE_EPOCHS', str(epochs))
    # inputs_string = 'torch.tensor(['
    # targets_string = 'torch.tensor(['
    inputs_string = []
    targets_string = []
    for (cur_set, cur_target) in ((left, '[1.0, 0.0, 0.0, 0.0, 0.0]'),
                                  (right, '[0.0, 1.0, 0.0, 0.0, 0.0]'),
                                  (up, '[0.0, 0.0, 1.0, 0.0, 0.0]'),
                                  (down, '[0.0, 0.0, 0.0, 1.0, 0.0]'),
                                  (no_action, '[0.0, 0.0, 0.0, 0.0, 1.0]')):
        for ((s_x, s_y), (e_x, e_y)) in cur_set:
            # inputs_string += (str([s_x, s_y, e_x, e_y]) + ', ')
            # targets_string += (cur_target + ', ')
            inputs_string.append('\t[' + str(s_x) + '.0, ' +  str(s_y) + '.0, ' + str(e_x) + '.0, ' + str(e_y) + '.0],\n')
            targets_string.append('\t' + cur_target + ',\n')
    # inputs_string += '])'
    # targets_string += '])'
    # template = template.replace('REPLACE_TARGETS', targets_string)
    # template = template.replace('REPLACE_INPUTS', inputs_string)
    print(len(left) + len(right) + len(up) + len(down) + len(no_action))
    print(len(targets_string))
    print(len(inputs_string))
    template = template.replace('REPLACE_TARGETS', 'torch.tensor([\n' + ''.join(targets_string) + '])')
    template = template.replace('REPLACE_INPUTS', 'torch.tensor([\n' + ''.join(inputs_string) + '])')
    output_file.write(template)
