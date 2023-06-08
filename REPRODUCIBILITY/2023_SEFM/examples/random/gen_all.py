import sys
import os
import random

LOCATION = sys.argv[1]
TO_GEN = int(sys.argv[2])
MIN_VAL = int(sys.argv[3])
MAX_VAL = int(sys.argv[4])

MIN_VAL = max(MIN_VAL, 2)
MAX_VAL = max(MAX_VAL, MIN_VAL)

ROOT = [('selector', 'sel'), ('sequence', 'seq'), ('parallel policy success_on_all', 'p_all'), ('parallel policy success_on_one', 'p_one')]
DECORATOR = [
    ('X_is_Y X success Y failure', 'dec_sf'),
    ('X_is_Y X success Y running', 'dec_sr'),
    ('X_is_Y X failure Y success', 'dec_fs'),
    ('X_is_Y X failure Y running', 'dec_fr'),
    ('X_is_Y X running Y success', 'dec_rs'),
    ('X_is_Y X running Y failure', 'dec_rf'),
    ('inverter', 'dec_inv')]
MEMORY = ['with_partial_memory', '']
# ROOT = [('selector', 'sel'), ('sequence', 'seq')]
CONSTANTS = list(map(str, range(MIN_VAL, MAX_VAL + 1)))
VARIABLES = list(map(lambda x : 'var' + str(x + 1), range(random.randint(2, 8))))
VAR_STRING = '{' + ' '.join(VARIABLES) + '}'
# FUNCTIONS = [('abs', 1, 1), ('max', 2, 2), ('min', 2, 2), ('negative', 1, 1), ('addition', 2, 5), ('subtraction', 2, 2), ('multiplication', 2, 5), ('division', 2, 2), ('mod', 2, 2), ('count', 2, 5)]
FUNCTIONS = [('abs', 1, 1), ('max', 2, 2), ('min', 2, 2), ('negative', 1, 1), ('addition', 2, 4), ('subtraction', 2, 2), ('multiplication', 2, 4), ('division', 2, 2), ('count', 2, 4)]
COMPARISONS = ['equal', 'not_equal', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'and', 'or', 'xor', 'xnor', 'implies', 'equivalent']
STATUSES = ['success', 'failure', 'running']

int_values = {}
bool_values = {}
check_nodes = {}
action_nodes = {}


def get_status():
    return random.choice(STATUSES)


def get_var():
    return random.choice(VARIABLES)


def create_int_value(depth_left):
    if depth_left < 0:
        depth_left = random.randint(0, 5)
    if depth_left == 0:
        if random.choice([True, False]):
            return random.choice(CONSTANTS)
        return get_var()
    (func, min_arg, max_arg) = random.choice(FUNCTIONS)
    if func == 'count':
        return '(count, ' + ', '.join([create_condition(depth_left) for _ in range(random.randint(min_arg, max_arg))]) + ')'
    return '(' + func + ', ' + ', '.join([('(min, ' + "'MAX_VAL'" + ', (max, ' + "'MIN_VAL'" + ', ' +create_int_value(random.randint(0, depth_left - 1)) + '))') for _ in range(random.randint(min_arg, max_arg))]) + ')'


def create_condition(depth_left):
    if depth_left < 0:
        depth_left = random.randint(0, 5)
    if depth_left == 0:
        return random.choice(['True', 'False'])
    left_depth = random.randint(0, depth_left - 1)
    right_depth = random.randint(0, depth_left - 1)
    comp = random.choice(COMPARISONS)
    if comp in {'equal', 'not_equal'}:
        int_mode = random.choice([True, False])
    elif comp in {'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal'}:
        int_mode = True
    else:
        int_mode = False
    if int_mode:
        return '(' + comp + ', ' + create_int_value(left_depth) + ', ' + create_int_value(right_depth) + ')'
    return '(' + comp + ', ' + create_condition(left_depth) + ', ' + create_condition(right_depth) + ')'
    

def create_check_node(name):
    return (indent(1) + 'check {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'read_variables ' + VAR_STRING + os.linesep
            + indent(2) + 'condition{' + create_condition(-1) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )


def create_action_node(name):
    num_before = random.randint(0, 4)
    num_after = random.randint(0, 4)
    update_before = []
    update_after = []
    for _ in range(num_before):
        condition_count = random.randint(0, 3)
        assign_pair = []
        for _ in range(condition_count):
            assign_pair.append((create_condition(-1), create_int_value(-1)))
        default = create_int_value(-1)
        update_before.append((get_var(), assign_pair, default))
    for _ in range(num_after):
        condition_count = random.randint(0, 3)
        assign_pair = []
        for _ in range(condition_count):
            assign_pair.append((create_condition(-1), create_int_value(-1)))
        default = create_int_value(-1)
        update_after.append((get_var(), assign_pair, default))
    condition_count = random.randint(0, 3)
    status_pair = []
    for _ in range(condition_count):
        status_pair.append((create_condition(-1), get_status()))
    default_status = get_status()
    return (indent(1) + 'action {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'local_variables {}' + os.linesep
            + indent(2) + 'read_variables { }' + os.linesep
            + indent(2) + 'write_variables ' + VAR_STRING + os.linesep
            + indent(2) + 'initial_values {}' + os.linesep
            + indent(2) + 'update {' + os.linesep
            + ''.join(
                [
                    (
                        indent(3) + 'variable_statement{' + var + ' assign { ' + os.linesep
                        + ''.join(
                            [
                                (indent(4) + 'case {' + condition + '} result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + result + '))}' + os.linesep)
                                for (condition, result) in assign_pair
                            ]
                        )
                        + (indent(4) + 'result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + default + '))}' + os.linesep)
                        + indent(3) + '}}' + os.linesep
                    )
                    for (var, assign_pair, default) in update_before
                ]
            )
            + indent(3) + 'return_statement{' + os.linesep
            + ''.join(
                [
                    (indent(4) + 'case { ' + condition + '} result { ' + status + '}' + os.linesep)
                    for (condition, status) in status_pair
                ]
            )
            + (indent(4) + 'result {' + default_status + '}' + os.linesep)
            + indent(3) + '}' + os.linesep
            + ''.join(
                [
                    (
                        indent(3) + 'variable_statement{' + var + ' assign { ' + os.linesep
                        + ''.join(
                            [
                                (indent(4) + 'case {' + condition + '} result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + result + '))}' + os.linesep)
                                for (condition, result) in assign_pair
                            ]
                        )
                        + (indent(4) + 'result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + default + '))}' + os.linesep)
                        + indent(3) + '}}' + os.linesep
                    )
                    for (var, assign_pair, default) in update_after
                ]
            )
            + indent(2) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )

def indent(n):
    return '\t'*n

node_count = 0
def create_structure(depth_left):
    if depth_left == -1:
        depth_left = random.randint(0, 5)
    if depth_left == 0:
        return {'leaf': True, 'dec': False, 'name' : random.choice(['c1', 'c2', 'a1', 'a2', 'a3', 'a4'])}
    global node_count
    if random.randint(0, 4) == 0:
        (node_type, node_name) = random.choice(DECORATOR)
        node_name = node_name + str(node_count)
        node_count = node_count + 1
        return {'leaf': False, 'dec': True, 'name' : node_name, 'type' : node_type, 'child' : create_structure(random.randint(0, depth_left - 1))}
    num_child = random.randint(2, 5)
    (node_type, node_name) = random.choice(ROOT)
    node_name = node_name + str(node_count)
    node_count = node_count + 1
    if 'success_on_one' in node_type:
        mem = ''
    else:
        mem = random.choice(MEMORY)
    return {'leaf': False, 'dec': False, 'name' : node_name, 'type' : node_type, 'mem' : mem, 'children' : [create_structure(random.randint(0, depth_left - 1)) for _ in range(num_child)]}


def write_tree(structure, indent_level):
    if structure['leaf']:
        return indent(indent_level) + structure['name'] + os.linesep
    if structure['dec']:
        return (
            indent(indent_level) + 'decorator {' + os.linesep
            + indent(indent_level + 1) + structure['name'] + os.linesep
            + indent(indent_level + 1) + structure['type'] + os.linesep
            + indent(indent_level + 1) + 'child {' + os.linesep
            + write_tree(structure['child'], indent_level + 2)
            + indent(indent_level + 1) + '}' + os.linesep
            + indent(indent_level) + '}' + os.linesep
        )
    return (
        indent(indent_level) + 'composite {' + os.linesep
        + indent(indent_level + 1) + structure['name'] + os.linesep
        + indent(indent_level + 1) + structure['type'] + os.linesep
        + indent(indent_level + 1) + structure['mem'] + os.linesep
        + indent(indent_level + 1) + 'children {' + os.linesep
        + ''.join(map(lambda child: write_tree(child, indent_level + 2), structure['children']))
        + indent(indent_level + 1) + '}' + os.linesep
        + indent(indent_level) + '}' + os.linesep
    )

for count in range(TO_GEN):
    node_count = 0
    with open(LOCATION + 't' + str(count) + '.tree', 'w') as f:
        f.write('constants {' + os.linesep
                + indent(1) + 'MIN_VAL = ' + str(MIN_VAL) + os.linesep
                + indent(1) + 'MAX_VAL = ' + str(MAX_VAL) + os.linesep
                + '}' + os.linesep
                + 'variables { ' + os.linesep
                + ''.join([(indent(1) + 'variable { bl ' + var + ' VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(random.randint(MIN_VAL, MAX_VAL)) + '}}}' + os.linesep) for var in VARIABLES])
                + '}' + os.linesep
                + 'environment_update {}' + os.linesep
                + 'checks{' + os.linesep
                + create_check_node('c1')
                + create_check_node('c2')
                + '}' + os.linesep
                + 'environment_checks {}' + os.linesep
                + 'actions{' + os.linesep
                + create_action_node('a1')
                + create_action_node('a2')
                + create_action_node('a3')
                + create_action_node('a4')
                + '}' + os.linesep
                + 'sub_trees{}' + os.linesep
                + 'tree {' + os.linesep
                + write_tree(create_structure(-1), 1)
                + '}' + os.linesep
                + 'specifications { #comment# INVAR, LTL, and CTL specs go here #end_comment# } end_specifications'
                )
