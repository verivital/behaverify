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
MAX_UPDATES = 5
MAX_CONDITIONS = 3
MAX_INDEX_DEPTH = 0
MAX_TIMES_INDEXED = 1
CUR_TIMES_INDEXED = 0
ALLOW_INTERESTING_INDEX = False

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
CONSTANTS_INT = list(map(str, range(MIN_VAL, MAX_VAL + 1))) + list(map(str, range(MAX_VAL * -1, (MIN_VAL * -1) + 1)))
CONSTANTS_ENUM = ['\'yes\'', '\'no\'', '\'both\'']
CONSTANTS_BOOL = ['True', 'False']
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


def domain_compare(cur_var, domain):
    if domain == 'int':
        return cur_var['domain'] in {'int_pos', 'int_neg'}
    elif domain == 'bool':
        return cur_var['domain'] == 'bool'
    elif domain == 'enum':
        return cur_var['domain'] == 'enum'
    else:
        return True


def get_var(bl, local, env, var_only, domain):
    '''
    bl -> bool indicating if blackboard variables allowed
    local -> list of local variables allowed
    env -> bool indicating if environment variables allowed
    '''
    cumulative = (
        (
            (list(filter(lambda x: domain_compare(x, domain), vars_bl)) if bl else [])
            + list(filter(lambda x: domain_compare(x, domain) and x in vars_local, local))
            + (list(filter(lambda x: domain_compare(x, domain), vars_env)) if env else [])
        )
        if var_only
        else
        (
            (list(filter(lambda x: domain_compare(x, domain), vars_bl + f_vars_bl + d_vars_bl)) if bl else [])
            + list(filter(lambda x: domain_compare(x, domain), local))
            + (list(filter(lambda x: domain_compare(x, domain), vars_env + f_vars_env + d_vars_env)) if env else [])
        )
    )
    if len(cumulative) == 0:
        return None
    return random.choice(cumulative)


def create_int_value(depth_left, bl, local, env):
    if depth_left < 0:
        depth_left = random.randint(0, STATEMENT_DEPTH)
    if depth_left == 0:
        if random.choice([True, False]):
            return random.choice(CONSTANTS_INT)
        ret_var = get_var(bl, local, env, False, 'int')
        if ret_var is None:
            return random.choice(CONSTANTS_INT)
        if ret_var['array'] is None:
            return ret_var['name']
        if ALLOW_INTERESTING_INDEX:
            global CUR_TIMES_INDEXED
            if CUR_TIMES_INDEXED >= MAX_TIMES_INDEXED:
                return random.choice(CONSTANTS_INT)
            CUR_TIMES_INDEXED = CUR_TIMES_INDEXED + 1
            return '(index, ' + ret_var['name'] + ', (max, 0, (min, ' + str(ret_var['array'] - 1) + ', ' + create_int_value(random.randint(0, MAX_INDEX_DEPTH), bl, local, env) + ')))'
        return '(index, ' + ret_var['name'] + ', ' + str(random.randint(0, ret_var['array'] - 1)) + ')'
    (func, min_arg, max_arg) = random.choice(FUNCTIONS)
    if func == 'count':
        return '(count, ' + ', '.join([create_bool_value(depth_left, bl, local, env) for _ in range(random.randint(min_arg, max_arg))]) + ')'
    if func == 'division':
        return (
            '(division, ' + create_int_value(random.randint(0, depth_left - 1), bl, local, env)
            + ', ('
            + (
                ('max, 1, ' + create_int_value(random.randint(0, depth_left - 1), bl, local, env))
                if random.choice((True, False))
                else
                ('min, -1, ' + create_int_value(random.randint(0, depth_left - 1), bl, local, env))
            )
            + '))'
        )
    return '(' + func + ', ' + ', '.join([create_int_value(random.randint(0, depth_left - 1), bl, local, env) for _ in range(random.randint(min_arg, max_arg))]) + ')'


def create_bool_value(depth_left, bl, local, env):
    if depth_left < 0:
        depth_left = random.randint(0, STATEMENT_DEPTH)
    if depth_left == 0:
        if random.choice([True, False]):
            return random.choice(['True', 'False'])
        ret_var = get_var(bl, local, env, False, 'bool')
        if ret_var is None:
            return random.choice(('True', 'False'))
        if ret_var['array'] is None:
            return ret_var['name']
        if ALLOW_INTERESTING_INDEX:
            global CUR_TIMES_INDEXED
            if CUR_TIMES_INDEXED >= MAX_TIMES_INDEXED:
                return random.choice(('True', 'False'))
            CUR_TIMES_INDEXED = CUR_TIMES_INDEXED + 1
            return '(index, ' + ret_var['name'] + ', (max, 0, (min, ' + str(ret_var['array'] - 1) + ', ' + create_int_value(random.randint(0, MAX_INDEX_DEPTH), bl, local, env) + ')))'
        return '(index, ' + ret_var['name'] + ', ' + str(random.randint(0, ret_var['array'] - 1)) + ')'
    left_depth = random.randint(0, depth_left - 1)
    right_depth = random.randint(0, depth_left - 1)
    comp = random.choice(COMPARISONS)
    if comp in {'equal', 'not_equal'}:
        mode = (random.choice(['int', 'bool', 'enum']) if can_use_enums else random.choice(['int', 'bool']))
    elif comp in {'less_than', 'greater_than', 'less_than_or_equal', 'greater_than_or_equal'}:
        mode = 'int'
    else:
        mode = 'bool'
    if mode == 'int':
        return '(' + comp + ', ' + create_int_value(left_depth, bl, local, env) + ', ' + create_int_value(right_depth, bl, local, env) + ')'
    elif mode == 'enum':
        return '(' + comp + ', ' + create_enum_value(left_depth, bl, local, env) + ', ' + create_enum_value(right_depth, bl, local, env) + ')'
    return '(' + comp + ', ' + create_bool_value(left_depth, bl, local, env) + ', ' + create_bool_value(right_depth, bl, local, env) + ')'


def create_enum_value(_, bl, local, env):
    if random.choice([True, False]):
        return random.choice(CONSTANTS_ENUM)
    ret_var = get_var(bl, local, env, False, 'enum')
    if ret_var is None:
        return random.choice(CONSTANTS_ENUM)
    if ret_var['array'] is None:
        return ret_var['name']
    if ALLOW_INTERESTING_INDEX:
        global CUR_TIMES_INDEXED
        if CUR_TIMES_INDEXED >= MAX_TIMES_INDEXED:
            return random.choice(CONSTANTS_ENUM)
        CUR_TIMES_INDEXED = CUR_TIMES_INDEXED + 1
        return '(index, ' + ret_var['name'] + ', (max, 0, (min, ' + str(ret_var['array'] - 1) + ', ' + create_int_value(random.randint(0, MAX_INDEX_DEPTH), bl, local, env) + ')))'
    return '(index, ' + ret_var['name'] + ', ' + str(random.randint(0, ret_var['array'] - 1)) + ')'


def create_check_node(name):
    global CUR_TIMES_INDEXED
    CUR_TIMES_INDEXED = 0
    return (indent(1) + 'check {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'read_variables ' + VAR_BL_STRING + os.linesep
            + indent(2) + 'condition{' + create_bool_value(-1, True, [], False) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )

def create_check_env_node(name):
    global CUR_TIMES_INDEXED
    CUR_TIMES_INDEXED = 0
    return (indent(1) + 'check_environment {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'read_variables ' + VAR_BL_STRING + os.linesep
            + indent(2) + 'condition{' + create_bool_value(-1, True, [], True) + '}' + os.linesep
            + indent(1) + '}' + os.linesep
            )


def write_assign_statement(cur_var, condition_count, indent_level, bl, local, env):
    global CUR_TIMES_INDEXED
    CUR_TIMES_INDEXED = 0
    return (
        indent(indent_level) + 'assign {' + os.linesep
        + ''.join(
            [
                (
                    indent(indent_level + 1) + 'case {' + create_bool_value(-1, bl, local, env) + '} result { '
                    + (
                        ('(min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + create_int_value(-1, bl, local, env) + '))')
                        if cur_var['domain'] == 'int_pos'
                        else
                        (
                            ('(min, ' + str(MIN_VAL * -1) + ', (max, ' + str(MAX_VAL * -1) + ', ' + create_int_value(-1, bl, local, env) + '))')
                            if cur_var['domain'] == 'int_neg'
                            else
                            (
                                create_bool_value(-1, bl, local, env)
                                if cur_var['domain'] == 'bool'
                                else
                                create_enum_value(-1, bl, local, env)
                            )
                        )
                    )
                    + '}' + os.linesep
                )
                for _ in range(condition_count)
            ]
        )
        + indent(indent_level + 1) + 'result {'
        + (
            ('(min, ' + str(MAX_VAL) + ', (max, ' + str(MIN_VAL) + ', ' + create_int_value(-1, bl, local, env) + '))')
            if cur_var['domain'] == 'int_pos'
            else
            (
                ('(min, ' + str(MIN_VAL * -1) + ', (max, ' + str(MAX_VAL * -1) + ', ' + create_int_value(-1, bl, local, env) + '))')
                if cur_var['domain'] == 'int_neg'
                else
                (
                    create_bool_value(-1, bl, local, env)
                                if cur_var['domain'] == 'bool'
                    else
                    create_enum_value(-1, bl, local, env)
                )
            )
        )
        + '}' + os.linesep
        + indent(indent_level) + '}' + os.linesep
    )


def write_variable_statement(cur_var, instant, condition_count, indent_level, bl, local, env):
    global CUR_TIMES_INDEXED
    CUR_TIMES_INDEXED = 0
    return (
        indent(indent_level) + 'variable_statement{ ' + ('instant ' if instant else '') + cur_var['name'] + os.linesep
        + (
            write_assign_statement(cur_var, condition_count, indent_level, bl, local, env)
            if cur_var['array'] is None
            else
            (
                ''.join(
                    (
                        [
                            (
                                indent(indent_level + 1) + 'index_of { (min, ' + str(cur_var['array'] - 1) + ', (max, 0, ' + create_int_value(-1, bl, local, env) + '))}' + os.linesep
                                + write_assign_statement(cur_var, condition_count, indent_level + 1, bl, local, env)
                            )
                            for _ in range(random.randint(1, cur_var['array']))
                        ]
                    )
                )
            )
        )
        + indent(indent_level) + '}' + os.linesep
    )

def create_action_node(name):
    global CUR_TIMES_INDEXED
    CUR_TIMES_INDEXED = 0
    my_local_vars = []
    local_init = ''
    local_count = 0
    for local in vars_local:
        if random.randint(0, 1) == 1:
            my_local_vars.append(local)
            if random.randint(0, 1) == 1:
                condition_count = random.randint(0, 2)
                local_init += write_variable_statement(local, False, condition_count, 3, True, [], False)
            local_count = local_count + 1
            break
    for local in f_vars_local + d_vars_local:
        if random.randint(0, 1) == 1:
            my_local_vars.append(local)
            if random.randint(0, 1) == 1:
                condition_count = random.randint(0, 2)
                local_init += write_variable_statement(local, False, condition_count, 3, True, [], False)
            local_count = local_count + 1
            if local_count >= 3:
                break

    total_updates = random.randint(0, MAX_UPDATES)
    num_before = random.randint(0, total_updates)
    num_after = total_updates - num_before
    before_string = ''
    after_string = ''
    before_mode = num_before > 0
    num_left = num_before if before_mode else num_after
    while num_left > 0:
        statement_type = random.randint(0, 2)
        if statement_type == 0:  # variable_statement
            num_left = num_left - 1
            condition_count = random.randint(0, MAX_CONDITIONS)
            update_string = write_variable_statement(get_var(True, my_local_vars, False, True, 'any'), False, condition_count, 3, True, my_local_vars, False)
        elif statement_type == 1:  # read_environment
            read_updates = random.randint(1, num_left)
            num_left = num_left - read_updates
            update_string = (
                indent(3) + 'read_environment {' + os.linesep
                + indent(4) + name + '_read_' + ('before_' if before_mode else 'after_') + str(num_left) + os.linesep
                + indent(4) + 'condition {' + create_bool_value(-1, True, my_local_vars, True) + '}' + os.linesep
                + ''.join(
                    [
                        write_variable_statement(get_var(True, my_local_vars, False, True, 'any'), False, random.randint(0, MAX_CONDITIONS), 4, True, my_local_vars, True)
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
                        write_variable_statement(get_var(False, [], True, True, 'any'), random.choice([True, False]), random.randint(0, MAX_CONDITIONS), 4, True, my_local_vars, True)
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
                (indent(4) + 'case { ' + create_bool_value(-1, True, my_local_vars, False) + '} result { ' + get_status() + '}' + os.linesep)
                for _ in range(condition_count)
            ]
        )
        + (indent(4) + 'result {' + get_status() + '}' + os.linesep)
        + indent(3) + '}' + os.linesep
        + after_string
    )
    return (indent(1) + 'action {' + os.linesep
            + indent(2) + name + os.linesep
            + indent(2) + 'local_variables {' + ' '.join(map(lambda x: x['name'], my_local_vars)) + '}' + os.linesep
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


def create_var(num, can_array, mode, force_type = None):
    my_domain = random.choice(('int_pos', 'int_neg', 'bool', 'enum'))
    if my_domain == 'enum':
        global can_use_enums
        if mode == 'DEFINE' and not can_use_enums:
            my_domain = random.choice(('int_pos', 'int_neg', 'bool'))
        else:
            can_use_enums = True
    if force_type is None:
        my_type = random.choice(('bl', 'local', 'env'))
    else:
        my_type = force_type
    if my_type == 'local' or not can_array or random.choice((True, False)):
        my_array = None
    else:
        my_array = random.randint(2, 3)
    cur_var = {
        'name' : my_type + mode + str(num),
        'type' : my_type,
        'domain' : my_domain,
        'array' : my_array,
    }
    cur_var['declaration'] = create_variable_declaration(cur_var, mode)
    return cur_var


def create_variable_declaration(cur_var, mode):
    cur_domain = ''
    if mode == 'DEFINE':
        cur_domain = (
            'INT'
            if cur_var['domain'] in {'int_pos', 'int_neg'}
            else
            (
                'BOOLEAN'
                if cur_var['domain'] == 'bool'
                else
                'ENUM'
            )
        )
    else:
        cur_domain = (
            ('[' + str(MIN_VAL) + ', ' + str(MAX_VAL) + ']')
            if cur_var['domain'] == 'int_pos'
            else
            (
                ('[' + str(-1 * MAX_VAL) + ', ' + str(-1 * MIN_VAL) + ']')
                if cur_var['domain'] == 'int_neg'
                else
                (
                    'BOOLEAN'
                    if cur_var['domain'] == 'bool'
                    else
                    ('{' + ', '.join(CONSTANTS_ENUM) + '}')
                )
            )
        )
    return (
        indent(1) + 'variable { ' + cur_var['type'] + ' ' + cur_var['name']
        + ('' if cur_var['array'] is None else (' array ' + str(cur_var['array'])))
        + ' ' + mode + ' '
        + cur_domain + os.linesep
        + (
            write_assign_statement(cur_var, random.randint(0, MAX_CONDITIONS), 2, True, [], cur_var['type'] == 'env')
            if cur_var['array'] is None
            else
            (
                (
                    indent(2) + 'range' + os.linesep
                    + write_assign_statement(cur_var, random.randint(0, MAX_CONDITIONS), 2, True, [], cur_var['type'] == 'env')
                )
                if random.choice((True, False))
                else
                ''.join(
                    [
                        write_assign_statement(cur_var, random.randint(0, MAX_CONDITIONS), 2, True, [], cur_var['type'] == 'env')
                        for _ in range(cur_var['array'])
                    ]
                )
            )
        )
        + indent(1) + '}' + os.linesep
    )

for count in range(TO_GEN):
    can_use_enums = False

    vars_bl = []
    vars_local = []
    vars_env = []
    f_vars_bl = []
    f_vars_local = []
    f_vars_env = []
    d_vars_bl = []
    d_vars_local = []
    d_vars_env = []

    create_order = []

    vars_bl = [create_var(0, False, 'VAR', force_type = 'bl')]
    create_order.append(vars_bl[0])
    vars_local = []
    vars_env = [create_var(1, False, 'VAR', force_type = 'env')]
    create_order.append(vars_env[0])
    num_array = 0
    total_vars = 2
    for _ in range(0, random.randint(1, 3)):
        new_var = create_var(total_vars, False, 'VAR')
        if new_var['array'] is not None:
            num_array = num_array + 1
        if new_var['type'] == 'bl':
            vars_bl.append(new_var)
        elif new_var['type'] == 'local':
            vars_local.append(new_var)
        else:
            vars_env.append(new_var)
        total_vars = total_vars + 1
        create_order.append(new_var)

    VAR_NAMES_BL = list(map(lambda x : x['name'], vars_bl))
    VAR_NAMES_LOCAL = list(map(lambda x : x['name'], vars_local))
    VAR_NAMES_ENV = list(map(lambda x : x['name'], vars_env))
    ENV_UPD = random.randint(0, 5)

    f_vars_bl = []
    f_vars_local = []
    f_vars_env = []
    num_array = 0
    for _ in range(0, random.randint(0, 2)):
        new_var = create_var(total_vars, False, 'FROZENVAR')
        if new_var['array'] is not None:
            num_array = num_array + 1
        if new_var['type'] == 'bl':
            f_vars_bl.append(new_var)
        elif new_var['type'] == 'local':
            f_vars_local.append(new_var)
        else:
            f_vars_env.append(new_var)
        total_vars = total_vars + 1
        create_order.append(new_var)

    F_VAR_NAMES_BL = list(map(lambda x : x['name'], f_vars_bl))
    F_VAR_NAMES_LOCAL = list(map(lambda x : x['name'], f_vars_local))
    F_VAR_NAMES_ENV = list(map(lambda x : x['name'], f_vars_env))

    d_vars_bl = []
    d_vars_local = []
    d_vars_env = []
    num_array = 0
    for _ in range(0, random.randint(2, 4)):
        new_var = create_var(total_vars, False, 'DEFINE')
        if new_var['array'] is not None:
            num_array = num_array + 1
        if new_var['type'] == 'bl':
            d_vars_bl.append(new_var)
        elif new_var['type'] == 'local':
            d_vars_local.append(new_var)
        else:
            d_vars_env.append(new_var)
        total_vars = total_vars + 1
        create_order.append(new_var)

    D_VAR_NAMES_BL = list(map(lambda x : x['name'], d_vars_bl))
    D_VAR_NAMES_LOCAL = list(map(lambda x : x['name'], d_vars_local))
    D_VAR_NAMES_ENV = list(map(lambda x : x['name'], d_vars_env))

    VAR_BL_STRING = '{' + ' '.join(VAR_NAMES_BL + F_VAR_NAMES_BL + D_VAR_NAMES_BL) + '}'
    VAR_LOCAL_STRING = '{' + ' '.join(VAR_NAMES_LOCAL + F_VAR_NAMES_LOCAL + D_VAR_NAMES_LOCAL) + '}'


    node_count = 0
    with open(LOCATION + '/' + 't' + str(count) + '.tree', 'w') as f:
        f.write('constants {' + os.linesep
                + indent(1) + 'MIN_VAL = ' + str(MIN_VAL) + os.linesep
                + indent(1) + 'MAX_VAL = ' + str(MAX_VAL) + os.linesep
                + '}' + os.linesep
                + 'variables { ' + os.linesep
                + ''.join(map(lambda x: x['declaration'], create_order))
                + '}' + os.linesep
                + 'environment_update {' + os.linesep
                + ''.join(
                    [
                        # write_variable_statement(get_var(False, [], True), random.choice([True, False]), random.randint(0, 2), 1, True, [], True)
                        write_variable_statement(get_var(False, [], True, True, 'any'), False, random.randint(0, 2), 1, True, [], True)
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
