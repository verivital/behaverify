import sys
import os
import random

LOCATION = sys.argv[1]
TO_GEN = int(sys.argv[2])
MIN_VAL = int(sys.argv[3])
MAX_VAL = int(sys.argv[4])

MIN_VAL = max(MIN_VAL, 2)
MAX_VAL = max(MAX_VAL, MIN_VAL)

STATEMENT_DEPTH = 4
MAX_UPDATES = 6
MAX_CONDITIONS = 3

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
# FUNCTIONS = [('abs', 1, 1), ('max', 2, 2), ('min', 2, 2), ('negative', 1, 1), ('addition', 2, 5), ('subtraction', 2, 2), ('multiplication', 2, 5), ('division', 2, 2), ('mod', 2, 2), ('count', 2, 5)]
FUNCTIONS = [('abs', 1, 1), ('max', 2, 2), ('min', 2, 2), ('negative', 1, 1), ('addition', 2, 4), ('subtraction', 2, 2), ('multiplication', 2, 4), ('division', 2, 2), ('count', 2, 4)]
COMPARISONS = ['equal', 'not_equal', 'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal', 'and', 'or', 'xor', 'xnor', 'implies', 'equivalent']
STATUSES = ['success', 'failure', 'running']

# int_values = {}
# bool_values = {}
# check_nodes = {}
# action_nodes = {}


def get_status():
    return random.choice(STATUSES)


def get_var(bl, local, env):
    '''
    bl -> bool indicating if blackboard variables allowed
    local -> list of local variables allowed
    env -> bool indicating if environment variables allowed
    '''
    cumulative = (VARS_BL if bl else []) + local + (VARS_ENV if env else [])
    return random.choice(cumulative)


def create_int_value(depth_left, bl, local, env):
    if depth_left < 0:
        depth_left = random.randint(0, STATEMENT_DEPTH)
    if depth_left == 0:
        if random.choice([True, False]):
            return random.choice(CONSTANTS)
        return get_var(bl, local, env)
    (func, min_arg, max_arg) = random.choice(FUNCTIONS)
    if func == 'count':
        return '(count, ' + ', '.join([create_condition(depth_left, bl, local, env) for _ in range(random.randint(min_arg, max_arg))]) + ')'
    return '(' + func + ', ' + ', '.join([('(min, ' + "'MAX_VAL'" + ', (max, ' + "'MIN_VAL'" + ', ' +create_int_value(random.randint(0, depth_left - 1), bl, local, env) + '))') for _ in range(random.randint(min_arg, max_arg))]) + ')'


def create_condition(depth_left, bl, local, env):
    if depth_left < 0:
        depth_left = random.randint(0, STATEMENT_DEPTH)
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
        return '(' + comp + ', ' + create_int_value(left_depth, bl, local, env) + ', ' + create_int_value(right_depth, bl, local, env) + ')'
    return '(' + comp + ', ' + create_condition(left_depth, bl, local, env) + ', ' + create_condition(right_depth, bl, local, env) + ')'
    

def create_check_node(name):
    return (indent(1) + 'check {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'read_variables ' + VAR_BL_STRING + os.linesep
            + indent(2) + 'condition{' + create_condition(-1, True, [], False) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )

def create_check_env_node(name):
    return (indent(1) + 'check_environment {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'read_variables ' + VAR_BL_STRING + os.linesep
            + indent(2) + 'condition{' + create_condition(-1, True, [], True) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )


def write_variable_statement(var, instant, condition_count, indent_level, bl, local, env):
    return (
        indent(indent_level) + 'variable_statement{ ' + ('instant ' if instant else '') + var + ' assign {' + os.linesep
        + ''.join(
            [
                (indent(indent_level + 1) + 'case {' + create_condition(-1, bl, local, env) + '} result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + create_int_value(-1, bl, local, env) + '))}' + os.linesep)
                for _ in range(condition_count)
            ]
        )
        + (indent(indent_level + 1) + 'result { (min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + create_int_value(-1, bl, local, env) + '))}' + os.linesep)
        + indent(indent_level) + '}}' + os.linesep
    )

def create_action_node(name):
    my_local_vars = []
    local_init = ''
    for local in VARS_LOCAL:
        if random.randint(0, 1) == 1:
            my_local_vars.append(local)
            if random.randint(0, 1) == 1:
                condition_count = random.randint(0, 2)
                local_init += write_variable_statement(local, False, condition_count, 3, True, [], False)
    total_updates = random.randint(0, MAX_UPDATES)
    num_before = random.randint(0, total_updates)
    num_after = total_updates - num_before
    before_string = ''
    after_string = ''
    before_mode = num_before > 0
    num_left = num_before if before_mode else num_after
    while num_left > 0:
        statement_type = random.randint(0, 2)
        if NUM_ENV == 0:
            statement_type = min(statement_type, 1)
            # prevents us from trying to create write_environment without evironement variables
        if statement_type == 0:  # variable_statement
            num_left = num_left - 1
            condition_count = random.randint(0, MAX_CONDITIONS)
            update_string = write_variable_statement(get_var(True, my_local_vars, False), False, condition_count, 3, True, my_local_vars, False)
        elif statement_type == 1:  # read_environment
            read_updates = random.randint(1, num_left)
            num_left = num_left - read_updates
            update_string = (
                indent(3) + 'read_environment {' + os.linesep
                + indent(4) + name + '_read_' + ('before_' if before_mode else 'after_') + str(num_left) + os.linesep
                + indent(4) + 'condition {' + create_condition(-1, True, my_local_vars, True) + '}' + os.linesep
                + ''.join(
                    [
                        write_variable_statement(get_var(True, my_local_vars, False), False, random.randint(0, MAX_CONDITIONS), 4, True, my_local_vars, True)
                        for _ in range(read_updates)
                    ]
                )
                + indent(3) + '}' + os.linesep
            )
        else:  # write_environment
            write_updates = random.randint(1, num_left)
            num_left = num_left - write_updates
            update_string = (
                indent(3) + 'write_environment {' + os.linesep
                + indent(4) + name + '_write_' + ('before_' if before_mode else 'after_') + str(num_left) + os.linesep
                + ''.join(
                    [
                        write_variable_statement(get_var(False, [], True), random.choice([True, False]), random.randint(0, MAX_CONDITIONS), 4, True, my_local_vars, True)
                        for _ in range(write_updates)
                    ]
                )
                + indent(3) + '}' + os.linesep
            )
        if before_mode:
            before_string += update_string
            if num_left < 1:
                before_mode = False
                num_left = num_after
        else:
            after_string += update_string

    condition_count = random.randint(0, 3)
    update_string = (
        before_string
        + indent(3) + 'return_statement {' + os.linesep
        + ''.join(
            [
                (indent(4) + 'case { ' + create_condition(-1, True, my_local_vars, False) + '} result { ' + get_status() + '}' + os.linesep)
                for _ in range(condition_count)
            ]
        )
        + (indent(4) + 'result {' + get_status() + '}' + os.linesep)
        + indent(3) + '}' + os.linesep
        + after_string
    )
    return (indent(1) + 'action {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'local_variables {' + ' '.join(my_local_vars) + '}' + os.linesep
            + indent(2) + 'read_variables { }' + os.linesep
            + indent(2) + 'write_variables ' + VAR_BL_STRING + os.linesep
            + indent(2) + 'initial_values {' + os.linesep
            + local_init + os.linesep
            + indent(2) + '}' + os.linesep
            + indent(2) + 'update {' + os.linesep
            + update_string
            + indent(2) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )


def indent(n):
    return '\t'*n


node_count = 0
def create_structure(depth_left):
    if depth_left == -1:
        depth_left = random.randint(0, 4)
    if depth_left == 0:
        return {'leaf': True, 'dec': False, 'name' : random.choice(['c1', 'c2', 'a1', 'a2', 'a3', 'a4'])}
    global node_count
    if random.randint(0, 4) == 0:
        (node_type, node_name) = random.choice(DECORATOR)
        node_name = node_name + str(node_count)
        node_count = node_count + 1
        return {'leaf': False, 'dec': True, 'name' : node_name, 'type' : node_type, 'child' : create_structure(random.randint(0, depth_left - 1))}
    num_child = random.randint(2, 4)
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

    NUM_VARS = random.randint(2, 8)
    NUM_BL = random.randint(1, NUM_VARS)
    NUM_LOCAL = random.randint(0, min(NUM_VARS - NUM_BL, 2))  # cap out at 2 local variables
    NUM_ENV = random.randint(0, (NUM_VARS - NUM_BL) - NUM_LOCAL)
    VARS_BL = list(map(lambda x : 'bl' + str(x + 1), range(NUM_BL)))
    VARS_LOCAL = list(map(lambda x : 'local' + str(x + 1), range(NUM_LOCAL)))
    VARS_ENV = list(map(lambda x : 'env' + str(x + 1), range(NUM_ENV)))
    VAR_BL_STRING = '{' + ' '.join(VARS_BL) + '}'
    VAR_LOCAL_STRING = '{' + ' '.join(VARS_LOCAL) + '}'

    node_count = 0
    ENV_UPD = random.randint(0, 5) if NUM_ENV > 0 else 0
    with open(LOCATION + 't' + str(count) + '.tree', 'w') as f:
        f.write('constants {' + os.linesep
                + indent(1) + 'MIN_VAL = ' + str(MIN_VAL) + os.linesep
                + indent(1) + 'MAX_VAL = ' + str(MAX_VAL) + os.linesep
                + '}' + os.linesep
                + 'variables { ' + os.linesep
                + ''.join([(indent(1) + 'variable { bl ' + var + ' VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(random.randint(MIN_VAL, MAX_VAL)) + '}}}' + os.linesep) for var in VARS_BL])
                + ''.join([(indent(1) + 'variable { local ' + var + ' VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(random.randint(MIN_VAL, MAX_VAL)) + '}}}' + os.linesep) for var in VARS_LOCAL])
                + ''.join([(indent(1) + 'variable { env ' + var + ' VAR [' + str(MIN_VAL) + ', ' + str(MAX_VAL) + '] assign { result {' + str(random.randint(MIN_VAL, MAX_VAL)) + '}}}' + os.linesep) for var in VARS_ENV])
                + '}' + os.linesep
                + 'environment_update {' + os.linesep
                + ''.join(
                    [
                        # write_variable_statement(get_var(False, [], True), random.choice([True, False]), random.randint(0, 2), 1, True, [], True)
                        write_variable_statement(get_var(False, [], True), False, random.randint(0, 2), 1, True, [], True)
                        for _ in range(ENV_UPD)
                    ]
                )
                + '}' + os.linesep
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
