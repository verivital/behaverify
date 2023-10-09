import random
import os
import sys

def create_flat_fake_net(hidden_size):
    return (
        ''.join(
            [
                'variable {bl fake_net_1_' + str(index) + ' DEFINE INT assign {result{(max, 0, (add, (mult, prev_dest_x, ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '), ' + str(random.randint(0, 5) * random.choice([-1, 1])) + ', (mult, prev_dest_y, ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '), ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '))}}}' + os.linesep
                for index in range(hidden_size)
            ]
        )
        + 'variable {bl fake_net_output DEFINE INT assign {result{(max, 0, (add, '
        + ', '.join(
            [
                '(mult, fake_net_1_' + str(index) + ', ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '), ' + str(random.randint(0, 5) * random.choice([-1, 1]))
                for index in range(hidden_size)
            ]
        )
        + '))}}}' + os.linesep
        + 'variable {bl fake_net_result VAR {0, 1} assign {case{(gt, fake_net_output, 0)}result{1}result{0}}}' + os.linesep
    )

def create_square_fake_net(hidden_size):
    return (
        ''.join(
            [
                'variable {bl fake_net_0_' + str(index) + ' DEFINE INT assign {result{' + ('prev_dest_x' if index % 2 == 0 else 'prev_dest_y') + '}}}' + os.linesep
                for index in range(hidden_size)
            ]
            +
            [
                'variable {bl fake_net_' + str(layer) + '_' + str(index) + ' DEFINE INT assign {result{(max, 0, (add, '
                + ', '.join(
                    [
                        '(mult, fake_net_' + str(layer - 1) + '_' + str(prev_index) + ', ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '), ' + str(random.randint(0, 5) * random.choice([-1, 1]))
                        for prev_index in range(hidden_size)
                    ]
                )
                + '))}}}' + os.linesep
                for layer in range(1, hidden_size)
                for index in range(hidden_size)
            ]
        )
        + 'variable {bl fake_net_output DEFINE INT assign {result{(max, 0, (add, '
        + ', '.join(
            [
                '(mult, fake_net_' + str(hidden_size - 1) + '_' + str(index) + ', ' + str(random.randint(0, 5) * random.choice([-1, 1])) + '), ' + str(random.randint(0, 5) * random.choice([-1, 1]))
                for index in range(hidden_size)
            ]
        )
        + '))}}}' + os.linesep
        + 'variable {bl fake_net_result VAR {0, 1} assign {case{(gt, fake_net_output, 0)}result{1}result{0}}}' + os.linesep
    )

def insert_net(net):
    return_string = ''
    with open(TEMPLATE_FILE, 'r', encoding = 'utf-8') as template:
        return_string = template.read()
    return_string = return_string.replace('} end_variables', net + os.linesep + '} end_variables')
    return_string = return_string.replace('} end_specifications', 'INVARSPEC { (eq, 0, fake_net_result)}' + os.linesep + '} end_specifications')
    return return_string

def write_flat_file(hidden_size):
    with open(WRITE_LOCATION + '/ANSR_scaling_with_state_flat_' + str(hidden_size) + '.tree', 'w', encoding = 'utf-8') as output:
        output.write(insert_net(create_flat_fake_net(hidden_size * hidden_size)))
    return

def write_square_file(hidden_size):
    with open(WRITE_LOCATION + '/ANSR_scaling_with_state_square_' + str(hidden_size) + '.tree', 'w', encoding = 'utf-8') as output:
        output.write(insert_net(create_square_fake_net(hidden_size)))
    return

TEMPLATE_FILE = sys.argv[1]
WRITE_LOCATION = sys.argv[2]
MIN_VAL = int(sys.argv[3])
MAX_VAL = int(sys.argv[4]) + 1
STEP_SIZE =int( sys.argv[5])

for count in range(MIN_VAL, MAX_VAL, STEP_SIZE):
    print(count)
    write_flat_file(count)
    write_square_file(count)
