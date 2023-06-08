import sys
import os

LOCATION = sys.argv[1]
MIN_VAL = int(sys.argv[2])
MAX_VAL = int(sys.argv[3])
if MIN_VAL == 0:
    MIN_VAL = 1
if MAX_VAL < MIN_VAL:
    MAX_VAL = MIN_VAL

# ROOT = [('selector', 'sel'), ('sequence', 'seq'), ('parallel policy success_on_all', 'p_all'), ('parallel policy success_on_one', 'p_one')]
ROOT = [('selector', 'sel'), ('sequence', 'seq')]
CONSTANTS = list(map(str, range(MIN_VAL, MAX_VAL + 1)))
VARIABLES = ['x', 'y']
FUNCTIONS = ['addition', 'mod']
COMPARISONS = ['greater_than', 'equal']


int_values = {}
bool_values = {}
check_nodes = {}
action_nodes = {}


def create_int_values(depth_left):
    if depth_left < 0:
        return []
    if depth_left in int_values:
        return int_values[depth_left]
    values = ['2'] + VARIABLES
    if depth_left > 0:
        poss_vals_left = create_int_values(depth_left - 1)
        poss_vals_right = ['2'] + VARIABLES
        for func in FUNCTIONS:
            for left_val in poss_vals_left:
                for right_val in poss_vals_right:
                    values.append('(' + func + ', ' + left_val + ', ' + right_val + ')')
    int_values[depth_left] = values
    return values


def create_condition(depth_left):
    if depth_left < 1:
        return []
    if depth_left in bool_values:
        return bool_values[depth_left]
    values = []
    poss_vals_left = create_int_values(depth_left - 1)
    poss_vals_right = ['2'] + VARIABLES
    for comparison in COMPARISONS:
        for left_val in poss_vals_left:
            for right_val in poss_vals_right:
                values.append('(' + comparison + ', ' + left_val + ', ' + right_val + ')')
    bool_values[depth_left] = values
    return values


def create_check_nodes(depth_left):
    def create_write_node(cur_condition):
        def write_node(name):
            return (indent(1) + 'check {' + os.linesep
                    + indent(2) + name + os.linesep
                    + indent(2) + 'read_variables { x y}' + os.linesep
                    + indent(2) + 'condition{' + cur_condition + '}' + os.linesep
                    + indent(1) + '}' + os.linesep
                    )
        return write_node
    if depth_left in check_nodes:
        return check_nodes[depth_left]
    values = []
    for condition in create_condition(depth_left):
        values.append(create_write_node(condition))
    check_nodes[depth_left] = values
    return values


def create_action_nodes(depth_left):
    def create_write_node(var1, var2, val1, val2):
        def write_node(name):
            return (indent(1) + 'action {' + os.linesep
                    + indent(2) + name + os.linesep
                    + indent(2) + 'local_variables {}' + os.linesep
                    + indent(2) + 'read_variables { }' + os.linesep
                    + indent(2) + 'write_variables { x y}' + os.linesep
                    + indent(2) + 'initial_values {}' + os.linesep
                    + indent(2) + 'update {' + os.linesep
                    + indent(3) + 'variable_statement{' + var1 + ' assign { result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + val1 + '))}}}' + os.linesep
                    + indent(3) + 'return_statement{ result{success}}' + os.linesep
                    + indent(3) + 'variable_statement{' + var2 + ' assign { result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + val2 + '))}}}' + os.linesep
                    + indent(1) + '}' + os.linesep
                    )
        return write_node
    if depth_left in action_nodes:
        return action_nodes[depth_left]
    values = []
    poss_vals_one = create_int_values(depth_left)
    poss_vals_two = create_int_values(depth_left-1)
    if len(poss_vals_one) == 0:
        poss_vals_one = ['2'] + VARIABLES
    if len(poss_vals_two) == 0:
        poss_vals_one = ['2'] + VARIABLES
    for var1 in VARIABLES:
        for var2 in VARIABLES:
            for val1 in poss_vals_one:
                for val2 in poss_vals_two:
                    values.append(create_write_node(var1, var2, val1, val2))
    action_nodes[depth_left] = values
    return values

def indent(n):
    return '\t'*n

count = 0
print('hello?')
r =len(ROOT)
c2 = len(create_check_nodes(2))
a2 = len(create_action_nodes(2))
c1 = len(create_check_nodes(1))
a1 = len(create_action_nodes(1))
print(a2)
print(a1)
print(r*r*c2*a2*c1*a1*a1)
print(r*r*c2*a2)
raise Exception
for (root_type, root_name) in ROOT:
    print('hello1?')
    for (left_type, left_name) in ROOT:
        print('hello2?')
        for left_check in create_check_nodes(2):
            print('hello3?')
            for action1 in create_action_nodes(2):
                print('hello4?')
                for right_check in create_check_nodes(1):
                    print('hello5?')
                    for action2 in create_action_nodes(1):
                        print('hello6?')
                        for action3 in create_action_nodes(1):
                            print('writing to: ' + LOCATION + str(count) + '.tree')
                            with open(LOCATION + 'tree_files/' + str(count) + '.tree', 'w') as f:
                                f.write('constants {}' + os.linesep
                                        + 'variables { variable { bl x VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(MIN_VAL) + '}}} variable { bl y VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(MIN_VAL) + '}}}}' + os.linesep
                                        + 'environment_update {}' + os.linesep
                                        + 'checks{' + os.linesep
                                        + left_check('l_check') + os.linesep
                                        + right_check('r_check') + os.linesep
                                        + '}' + os.linesep
                                        + 'environment_checks {}' + os.linesep
                                        + 'actions{' + os.linesep
                                        + action1('action1')
                                        + action2('action2')
                                        + action3('action3')
                                        + '}' + os.linesep
                                        + 'subtrees{}' + os.linesep
                                        + 'tree {' + os.linesep
	                                + indent(1) + 'composite {' + root_name + ' ' + root_type + ' children {' + os.linesep
                                        + indent(2) + 'composite {left_' + left_name + ' ' + left_type + ' children {l_check action1}}' + os.linesep
                                        + indent(2) + 'r_check' + os.linesep
                                        + indent(2) + 'action2' + os.linesep
                                        + indent(2) + 'action3' + os.linesep
                                        + indent(1) + '}' + os.linesep
                                        + '}' + os.linesep
                                        + 'specifications { #comment# INVAR, LTL, and CTL specs go here #end_comment# } end_specifications'
                                        )
                            count = count + 1
