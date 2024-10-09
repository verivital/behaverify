import os
import argparse
import re
import sys
from check_grammar import validate_model
from serene_functions import build_meta_func
from behaverify_common import indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type, BTreeException, constant_type
from model_to_dsl import model_to_dsl

class Silly_Dictionary:
    def __init__(self, attributes):
        for attribute in attributes:
            setattr(self, attribute, None)

def create_blank_variable_obj():
    return Silly_Dictionary([ 'var_type', 'name', 'model_as', 'domain', 'static', 'array_size', 'default_value', 'constant_index', 'iterative_assign', 'index_var_name', 'assigns', 'assign'])
    # return Variable_Tuple()

def create_constant(name, value):
    con = Silly_Dictionary(['name', 'val'])
    con.name = name
    con.val = value
    return con

def create_result(condition, values):
    res = Silly_Dictionary(['condition', 'values'])
    res.condition = condition
    res.values = values
    return res

def create_assign_value(cond_vals_pairs):
    mapped = [create_result(cond, vals) for (cond, vals) in cond_vals_pairs]
    assign_value = Silly_Dictionary(['case_results', 'default_result'])
    assign_value.case_results = mapped[0:-1]
    assign_value.default_result = mapped[-1]
    return assign_value

def create_array_index(index, cond_vals_pairs):
    ind = Silly_Dictionary(['index_expr', 'assign'])
    ind.index_expr = [index]
    ind.assign = create_assign_value(cond_vals_pairs)
    return ind

def create_loop_array(index, cond_vals_pairs):
    ind = Silly_Dictionary(['loop_array_index', 'array_index'])
    ind.array_index = create_array_index(index, cond_vals_pairs)
    return ind

# # TODO FINISH THIS
# def create_loop_array_with_loop(index, cond_vals_pairs, monitor_name):
#     ind = namedtuple('looparray', ['loop_variable', 'reverse', 'loop_variable_domain', 'min_val', 'max_val', 'loop_condition', 'loop_array_index', 'array_index'])
#     ind.loop_variable = 'loop_var'
#     ind.min_val = '0'
#     ind.max_val = monitor_name + '_states_COUNT'
#     ind.loop_condition = 'True'
#     ind.loop_array_index = create_loop_array('loop_var', cond_vals_pairs)
#     return ind

def create_variable_obj_p(monitor_name, default_assign, assigns):
    var = create_blank_variable_obj()
    var.var_type = 'bl'
    var.name = monitor_name + '_p'
    var.model_as = 'DEFINE'
    var.domain = 'BOOLEAN'
    var.static = ''
    var.array_size = monitor_name + '_p_COUNT'
    var.default_value = default_assign
    var.constant_index = 'constant_index'
    var.assigns = assigns
    return var

def create_variable_obj_states(monitor_name, default_assign_states, assigns_states, default_assign_def, assigns_def):
    var_states = create_blank_variable_obj()
    var_states.var_type = 'bl'
    var_states.name = monitor_name + '_states'
    var_states.model_as = 'VAR'
    var_states.domain = 'BOOLEAN'
    var_states.static = ''
    var_states.array_size = monitor_name + '_states_COUNT'
    var_states.default_value = default_assign_states
    var_states.constant_index = 'constant_index'
    var_states.assigns = assigns_states
    var_states_def = create_blank_variable_obj()
    var_states_def.var_type = 'bl'
    var_states_def.name = monitor_name + '_states_def'
    var_states_def.model_as = 'DEFINE'
    var_states_def.domain = 'BOOLEAN'
    var_states_def.static = ''
    var_states_def.array_size = monitor_name + '_states_COUNT'
    var_states_def.default_value = default_assign_def
    var_states_def.constant_index = 'constant_index'
    var_states_def.assigns = assigns_def
    return (var_states, var_states_def)

def create_variable_statement(variable, assign):
    statement = Silly_Dictionary(['variable', 'constant_index', 'iterative_assign', 'assigns', 'assign', 'instant'])
    statement.variable = variable
    statement.constant_index = ''
    statement.assign = assign
    return statement

def create_iterative_assign(condition, assign):
    iter_assign = Silly_Dictionary(['condition', 'assign'])
    iter_assign.condition = condition
    iter_assign.assign = assign
    return iter_assign

def create_variable_statement_iterative(variable, iterative_assigns, assign):
    statement = Silly_Dictionary(['variable', 'constant_index', 'iterative_assign', 'index_var_name', 'iterative_assign_conditionals', 'assigns', 'assign', 'instant'])
    statement.variable = variable
    statement.iterative_assign = 'iterative_assign'
    statement.index_var_name = 'loop_var'
    statement.iterative_assign_conditionals = iterative_assigns
    statement.assign = assign
    return statement

def create_ltl2ba_command(metamodel_file, model_file, location, recursion_limit, no_checks):
    def execute_loop(function_call, to_call, packaged_args):
        return_vals = []
        all_domain_values = []
        if function_call.min_val is None:
            for domain_code in function_call.loop_variable_domain:
                for domain_value in execute_code(domain_code):
                    resolved = resolve_potential_reference_no_type(domain_value, declared_enumerations, {}, variables, constants, loop_references)
                    all_domain_values.append(resolved[1])
        else:
            (min_val, max_val) = get_min_max(function_call.min_val, function_call.max_val, declared_enumerations, {}, variables, constants, loop_references)
            all_domain_values = range(min_val, max_val + 1)
        if function_call.reverse:
            all_domain_values = reversed(all_domain_values)
        cond_func = build_meta_func(function_call.loop_condition)
        for domain_member in all_domain_values:
            loop_references[function_call.loop_variable] = domain_member
            if cond_func((constants, loop_references))[0]:
                return_vals.extend(to_call(packaged_args))
            loop_references.pop(function_call.loop_variable)
        return return_vals

    def execute_code(code):
        cur_func = build_meta_func(code)
        return cur_func((constants, loop_references))

    def format_function_if(_, function_call):
        return ['(' + format_code(function_call.values[1])[0] + ' if ' + format_code(function_call.values[0])[0] + ' else ' + format_code(function_call.values[2])[0] + ')']

    def format_function_loop(_, function_call):
        return execute_loop(function_call, format_code, function_call.values[0])

    def format_case_loop_recursive(function_call, cond_func, values, index):
        if len(values) == index:
            if function_call.loop_variable in loop_references:
                loop_references.pop(function_call.loop_variable)
            return format_code(function_call.default_value)
        loop_references[function_call.loop_variable] = values[index]
        if not cond_func((constants, loop_references))[0]:
            return format_case_loop_recursive(function_call, cond_func, values, index + 1)
        return ['(' + format_code(function_call.values[0])[0] + ' if ' + format_code(function_call.cond_value)[0] + ' else ' + format_case_loop_recursive(function_call, cond_func, values, index + 1)[0] + ')']

    def format_function_case_loop(_, function_call):
        all_domain_values = []
        if function_call.min_val is None:
            for domain_code in function_call.loop_variable_domain:
                for domain_value in execute_code(domain_code):
                    resolved = resolve_potential_reference_no_type(domain_value, declared_enumerations, {}, variables, constants, loop_references)
                    all_domain_values.append(resolved[1])
        else:
            (min_val, max_val) = get_min_max(function_call.min_val, function_call.max_val, declared_enumerations, {}, variables, constants, loop_references)
            all_domain_values = range(min_val, max_val + 1)
        if function_call.reverse:
            all_domain_values = list(reversed(all_domain_values))
        cond_func = build_meta_func(function_call.loop_condition)
        return format_case_loop_recursive(function_call, cond_func, all_domain_values, 0)

    def format_function_before(function_name, function_call):
        return [
            function_name + '('
            + ', '.join([', '.join(format_code(value)) for value in function_call.values])
            + ')'
        ]

    def format_function_between(function_name, function_call):
        return [
            '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value)) for value in function_call.values])
            + ')'
        ]

    def format_function_implies(_, function_call):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value))
        return ['(' + '(not ' + formatted_values[0] + ') or ' + formatted_values[1] + ')']

    def format_function_division(_, function_call):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value))
        return ['(int(' + formatted_values[0] + ' / ' + formatted_values[1] + '))']

    def format_function_xnor(_, function_call):
        return ['(not (' + function_format['xor'][1](function_format['xor'][0], function_call)[0] + '))']

    def format_function_count(_, function_call):
        return [
            '('
            + '[' + ', '.join([', '.join(format_code(value)) for value in function_call.values]) + '].count(True)'
            + ')'
        ]

    def format_function_index(_, function_call):
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        formatted_variable = format_variable_name_only(variable)
        formatted_index = ''
        if function_call.constant_index == 'constant_index':
            index_func = build_meta_func(function_call.values[0])
            index = resolve_potential_reference_no_type(index_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
            formatted_index = str(index)
        else:
            formatted_index = format_code(function_call.values[0])[0]
        return [
            (formatted_variable + '(' + formatted_index + ')')
            if variable.model_as in ('DEFINE', 'NEURAL') and variable.static != 'static' else
            (formatted_variable + '[' + formatted_index + ']')
        ]

    def format_function(code):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call)

    def format_variable_name_only(variable):
        return 'model_state[\'' + variable.name + '\']'

    def format_variable(variable):
        return format_variable_name_only(variable) + ('()' if variable.model_as in ('DEFINE', 'NEURAL') and variable.static != 'static' else '')

    def str_conversion(atom_type, atom):
        if atom_type in ('VARIABLE', 'NODE'):
            return str(atom)
        if atom_type == 'CONSTANT':
            atom_type = constant_type(atom, declared_enumerations)
        return (
            ('\'' + atom + '\'')
            if atom_type == 'ENUM' else
            (
                str(atom)
                if atom_type == 'BOOLEAN' else
                (
                    ('(' + str(atom) + ')')
                    if atom < 0 else
                    str(atom)
                )
            )
        )

    def handle_atom(code):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException as bt_e:  # this should be an argument.
            raise BTreeException([], 'Encountered unknown reference: ' + str(code.atom.reference)) from bt_e
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom)

    def format_code(code):
        return (
            [handle_atom(code)]
            if code.atom is not None else
            (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement)]
                if code.code_statement is not None else
                format_function(code)
            )
        )

    def has_ltl(code):
        return (
            False
            if code.atom is not None else
            (
                has_ltl(code.code_statement)
                if code.code_statement is not None else
                (
                    True
                    if code.function_call.function_name in ('next', 'globally', 'finally', 'until', 'release', 'previous', 'not_previous_not', 'historically', 'once', 'since', 'triggered') else
                    (
                        False
                        if code.function_call.function_name not in ('not', 'and', 'or', 'xor', 'xnor', 'implies', 'equivalent') else
                        any(has_ltl(value) for value in code.function_call.values)
                    )
                )
            )
        )

    def create_ltl2ba_command_internal(code, p_count):
        # what do I want this to return?
        # obviously I need it to return the command that we will feed to ltl2ba, but I also need more than that.
        # the other thing this needs to return is a dictionary from atoms (p1, p2, etc) to their definitions (e.g., p1 = x < 4).
        # then I just need to feed the ltl command to ltl2ba, and then parse that ouput using another method.
        if not has_ltl(code):
            # there is no ltl within this code. We can turn it into a single thing.
            return ([(str(p_count), code)], 'p' + str(p_count), p_count + 1)
        if code.code_statement is not None:
            return create_ltl2ba_command_internal(code.code_statement, p_count)
        if code.function_call.function_name not in function_format_ltl:
            raise NotImplementedError('The ltl function ' + str(code.function_call.function_name) + ' is not yet implemented for monitoring.')
        (symbol, mode) = function_format_ltl[code.function_call.function_name]
        if mode == 'before':
            (var_info, specification_string, p_count) = create_ltl2ba_command_internal(code.function_call.values[0], p_count)
            return (
                var_info,
                symbol + '(' + specification_string + ')',
                p_count
            )
        all_var_info = []
        command_strings = []
        for value in code.function_call.values:
            (var_info, command_string, p_count) = create_ltl2ba_command_internal(value, p_count)
            all_var_info.extend(var_info)
            command_strings.append('(' + command_string + ')')
        return (
            all_var_info,
            symbol.join(command_strings),
            p_count
        )
    function_format = {
        'if' : ('', format_function_if),
        'loop' : ('', format_function_loop),
        'case_loop' : ('', format_function_case_loop),
        'abs' : ('abs', format_function_before),
        'max' : ('max', format_function_before),
        'min' : ('min', format_function_before),
        'sin' : ('math.sin', format_function_before),
        'cos' : ('math.cos', format_function_before),
        'tan' : ('math.tan', format_function_before),
        'ln' : ('math.log', format_function_before),
        'not' : ('not ', format_function_before),  # space intentionally added here.
        'and' : ('and', format_function_between),
        'or' : ('or', format_function_between),
        'xor' : ('^', format_function_between),
        'xnor' : ('xnor', format_function_xnor),
        'implies' : ('->', format_function_implies),
        'equivalent' : ('==', format_function_between),
        'eq' : ('==', format_function_between),
        'neq' : ('!=', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('<=', format_function_between),
        'gte' : ('>=', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('*', format_function_between),
        # 'division' : ('//', format_function_between),  # this rounds to negative infinity, we want rounds to 0.
        'idiv' : ('division', format_function_division),
        'mod' : ('%', format_function_between),
        'rdiv' : ('/', format_function_between),
        'floor' : ('math.floor', format_function_before),
        'count' : ('count', format_function_count),
        'index' : ('index', format_function_index)
    }
    function_format_ltl = {
        'next' : ('X', 'before'),
        'globally' : ('[]', 'before'),
        'finally' : ('<>', 'before'),
        'until' : ('U', 'between'),
        'release' : ('V', 'between'),
        'not' : ('!', 'before'),
        'and' : ('&&', 'between'),
        'or' : ('||', 'between'),
        'implies' : ('->', 'between'),
        'equivalent' : ('<->', 'between')
    }
    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit, no_checks)
    loop_references = {}
    if location[-1] != '/':
        location = location + '/'
    for monitor in model.monitors:
        (all_var_info_, command_string_, p_count) = create_ltl2ba_command_internal(monitor.specification.code_statement, 0)
        with open (location + monitor.name + '.txt', 'w', encoding = 'utf-8') as output_file:
            output_file.write(command_string_)
        model.constants.append(create_constant(monitor.name + '_p_COUNT', p_count))
        model.constants.append(create_constant(monitor.name + '_states_COUNT', 3))
        model.constants.append(create_constant(monitor.name + '_ACCEPTING', monitor.safe_val))
        model.constants.append(create_constant(monitor.name + '_SAFE', monitor.safe_val))
        model.constants.append(create_constant(monitor.name + '_UNSAFE', monitor.unsafe_val))
        model.constants.append(create_constant(monitor.name + '_UNKNOWN', monitor.unknown_val))
        default_val = create_assign_value([(None, [False])])
        assigns = [None for _ in range(p_count)]
        for (index_, code_) in all_var_info_:
            assigns[int(index_)] = create_loop_array(index_, [(None, [code_])])
        model.variables.append(create_variable_obj_p(monitor.name, default_val, assigns))
        model.variables.extend(create_variable_obj_states(monitor.name, default_val, [create_loop_array(0, [(None, ['True'])])], default_val, assigns))
    for node in model.action_nodes:
        for statements in (node.pre_update_statements, node.post_update_statements):
            for index in reversed(range(len(statements))):
                statement = statements[index]
                if statement.monitor_statement is not None:
                    monitor_statement = statement.monitor_statement
                    mon_name = monitor_statement.monitor.name
                    var_name = monitor_statement.monitor_variable.name
                    if mon_name + '_states' not in node.write_variables:
                        node.write_variables.append(mon_name + '_states')
                    if mon_name + '_states_def' not in node.read_variables:
                        node.read_variables.append(mon_name + '_states_def')
                    if mon_name + '_p' not in node.read_variables:
                        node.read_variables.append(mon_name + '_p')
                    new_statement = Silly_Dictionary(['variable_statement', 'read_statement', 'write_statement', 'monitor_statement'])
                    if monitor_statement.monitor_reset == 'reset':
                        new_statement.variable_statement = create_variable_statement_iterative(
                            mon_name + '_states',
                            [create_iterative_assign('(eq, loop_var, 0)', create_assign_value([(None, ['True'])]))],
                            create_assign_value([(None, ['False'])])
                        )
                        statements.insert(index + 1, new_statement)
                    elif monitor_statement.monitor_mode == 'commit' and monitor_statement.monitor_reset == 'reset_on_failure':
                        new_statement.variable_statement = create_variable_statement_iterative(
                            mon_name + '_states',
                            [
                                create_iterative_assign(
                                    '(eq, loop_var, 0)',
                                    create_assign_value(
                                        [
                                            ('(eq, ' + var_name + ', ' + mon_name + '_UNSAFE)', ['True']),
                                            (None, ['(index, ' + mon_name + '_states_def, constant_index 0)'])
                                        ]
                                    )
                                )
                            ],
                            create_assign_value(
                                [
                                    ('(eq, ' + var_name + ', ' + mon_name + '_UNSAFE)', ['False']),
                                    (None, ['(index, ' + mon_name + '_states_def, constant_index loop_var)'])
                                ]
                            )
                        )
                        statements.insert(index + 1, new_statement)
                    # commit + reset is just reset.
                    # elif monitor_statement.monitor_mode == 'commit' and  monitor_statement.monitor_reset == 'reset':
                    #     pass
                    elif monitor_statement.monitor_mode == 'commit':
                        new_statement.variable_statement = create_variable_statement_iterative(
                            mon_name + '_states',
                            [],
                            create_assign_value([(None, ['(index, ' + mon_name + '_states_def, constant_index loop_var)'])])
                        )
                        statements.insert(index + 1, new_statement)
                    elif monitor_statement.monitor_reset == 'reset_on_failure':
                        new_statement.variable_statement = create_variable_statement_iterative(
                            mon_name + '_states',
                            [
                                create_iterative_assign(
                                    '(eq, loop_var, 0)',
                                    create_assign_value(
                                        [
                                            ('(eq, ' + var_name + ', ' + mon_name + '_UNSAFE)', ['True']),
                                            (None, ['(index, ' + mon_name + '_states, constant_index 0)'])
                                        ]
                                    )
                                )
                            ],
                            create_assign_value(
                                [
                                    ('(eq, ' + var_name + ', ' + mon_name + '_UNSAFE)', ['False']),
                                    (None, ['(index, ' + mon_name + '_states, constant_index loop_var)'])
                                ]
                            )
                        )
                        statements.insert(index + 1, new_statement)
                    statement.variable_statement = create_variable_statement(
                        var_name,
                        create_assign_value(
                            [
                                (
                                    '(and, ' + mon_name + '_ACCEPTING, (index, ' + mon_name + '_states_def, constant_index (sub, ' + mon_name + '_states_COUNT, 1)))',
                                    [mon_name + '_SAFE']
                                ),
                                (
                                    '(or, False, (loop, loop_var, [0, (sub, ' + mon_name + '_states_COUNT, 1)] such_that True, (index, ' + mon_name + '_states_def, constant_index loop_var)))',
                                    [mon_name + '_UNKNOWN']
                                ),
                                (
                                    None,
                                    [mon_name + '_UNSAFE']
                                )
                            ]
                        )
                    )
                    statement.monitor_statement = None
    model_to_dsl(model, os.path.join(location, os.path.basename(model_file)))
    return

def parse_ba(ba_file):
    monitor_name = os.path.basename(ba_file)
    if '.ba' not in monitor_name:
        return None
    monitor_name = monitor_name.split('.')[0]
    def find_closest_unit(cur_seg, start, delta):
        can_return = False
        paran_count = 0
        index = start
        inside = False
        while (paran_count != 0) or (not(can_return)) or inside:
            if cur_seg[index] == ')':
                paran_count = paran_count - 1
            elif cur_seg[index] == '(':
                paran_count = paran_count + 1
            elif cur_seg[index] == 'p':
                can_return = True
            index = index + delta
            if delta > 0:
                while cur_seg[index] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    index = index + delta
        return index - delta
    def replace_infix_symbol(guard_statement, symbol, replacement):
        while symbol in guard_statement:
            (left, right) = guard_statement.split(symbol, 1)
            left_index = find_closest_unit(left, len(left) - 1, -1)
            right_index = find_closest_unit(right, 0, 1)
            left_prefix = left[:left_index]
            left_group = left[left_index:]
            right_group = right[:(right_index + 1)]
            right_postfix = right[(right_index + 1):]
            guard_statement = left_prefix + '(' + replacement + ', ' + left_group.strip() + ', ' + right_group.strip() + ')' + right_postfix
        return guard_statement
    def replace_prefix_symbol(guard_statement, symbol, replacement):
        while symbol in guard_statement:
            (left, right) = guard_statement.split(symbol, 1)
            right_index = find_closest_unit(right, 0, 1)
            right_group = right[:(right_index + 1)]
            right_postfix = right[(right_index + 1):]
            guard_statement = left + '(' + replacement + ', ' + right_group.strip() + ')' + right_postfix
        return guard_statement
    def parse_guard(guard_statement):
        guard_statement = guard_statement.replace('!=', '_=')
        guard_statement = replace_prefix_symbol(guard_statement, '!', 'not')
        guard_statement = replace_infix_symbol(guard_statement, '==', 'eq')
        guard_statement = replace_infix_symbol(guard_statement, '_=', 'neq')
        guard_statement = replace_infix_symbol(guard_statement, '&&', 'and')
        guard_statement = replace_infix_symbol(guard_statement, '||', 'or')
        guard_statement = replace_infix_symbol(guard_statement, '->', 'im_lies')
        guard_statement = guard_statement.replace('(1)', 'True')
        guard_statement = re.sub(r'p([0-9]+)', lambda x: '(index, ' + monitor_name + '_p, constant_index ' + x.group(1) + ')', guard_statement)
        guard_statement = guard_statement.replace('im_lies',  'implies')
        return guard_statement

    state_to_index = {}
    initial_state = None
    accepting_state = None
    cur_state = None
    listed_initial = None
    listed_accepting = None
    with open(ba_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if 'never {' in line:
                continue
            counter = line.count(':')
            if counter == 0:
                if 'skip' in line:
                    accepting_state = cur_state
                continue
            if counter == 1:
                cur_state = line.split(':')[0].strip()
                if 'init' in cur_state:
                    initial_state = cur_state
                if len(state_to_index):
                    listed_initial = cur_state
                listed_accepting = cur_state
                state_to_index[cur_state] = len(state_to_index)
    if state_to_index[initial_state] != 0:
        initial_loc = state_to_index[initial_state]
        state_to_index[initial_state] = 0
        state_to_index[listed_initial] = initial_loc
    if (accepting_state is not None) and (state_to_index[accepting_state] != len(state_to_index) - 1):
        accepting_loc = state_to_index[accepting_state]
        state_to_index[accepting_state] = len(state_to_index) - 1
        state_to_index[listed_accepting] = accepting_loc
    state_trans = {}
    with open(ba_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if 'never {' in line:
                continue
            counter = line.count(':')
            if counter == 0:
                if 'skip' in line:
                    if cur_state not in state_trans:
                        state_trans[cur_state] = []
                    state_trans[cur_state].append(('True', cur_state))
                continue
            if counter == 1:
                cur_state = line.split(':')[0].strip()
                continue
            if counter == 2:
                line = line.replace(':', '')
                (guard, next_state) = line.split(' -> goto ')
                next_state = next_state.strip()
                if next_state not in state_trans:
                    state_trans[next_state] = []
                guard = guard.strip()
                state_trans[next_state].append((parse_guard(guard), cur_state))
                continue
    assigns = []
    for next_state in state_trans:
        index = state_to_index[next_state]
        assigns.append(
            create_loop_array(
                index,
                [
                    (
                        None,
                        [(
                            ('(or, ' if len(state_trans) > 1 else '')
                            + ', '.join(
                                [
                                    ('(and, (index, ' + monitor_name + '_states, constant_index ' + str(state_to_index[cur_state]) + '), ' + guard + ')')
                                    for (guard, cur_state) in state_trans[next_state]
                                ]
                            )
                            + (')' if len(state_trans) > 1 else '')
                        )]
                    )
                ]
            )
        )
    return (monitor_name, assigns, accepting_state, len(state_trans))

def handle_files_at_location(metamodel_file, model_file, location, recursion_limit):
    (model, _, _, _) = validate_model(metamodel_file, model_file, recursion_limit, True)
    for possible_file in os.listdir(location):
        result = parse_ba(os.path.join(location, possible_file))
        if result is None:
            continue
        (monitor_name, assigns, accepting_state, state_count) = result
        for variable in model.variables:
            if variable.name == monitor_name + '_states_def':
                variable.assigns = assigns
                break
        for constant in model.constants:
            if constant.name == (monitor_name + '_states_COUNT'):
                constant.val = state_count
            if constant.name == (monitor_name + '_ACCEPTING'):
                constant.val = accepting_state is not None
    model_to_dsl(model, os.path.join(location, os.path.basename(model_file)))
    return

if __name__ == '__main__':
    if sys.argv[1] == 'make_ltl2ba':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('metamodel_file')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        args = arg_parser.parse_args(sys.argv[2:])
        create_ltl2ba_command(args.metamodel_file, args.model_file, args.location, args.recursion_limit, args.no_checks)
    elif sys.argv[1] == 'ba_to_monitor':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('metamodel_file')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        args = arg_parser.parse_args(sys.argv[2:])
        handle_files_at_location(args.metamodel_file, args.model_file, args.location, args.recursion_limit)
