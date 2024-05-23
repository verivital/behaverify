import os
import argparse
import re
import sys
from check_grammar import validate_model
from serene_functions import build_meta_func
from behaverify_common import indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type, BTreeException, constant_type

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
            return (
                (
                    'def p' + str(p_count) + '_func(model_state):' + os.linesep
                    + indent(1) + 'return ' + format_code(code)[0] + os.linesep
                ),
                'p' + str(p_count),
                p_count + 1
            )
        if code.code_statement is not None:
            return create_ltl2ba_command_internal(code.code_statement, p_count)
        if code.function_call.function_name not in function_format_ltl:
            raise NotImplementedError('The ltl function ' + str(code.function_call.function_name) + ' is not yet implemented for monitoring.')
        (symbol, mode) = function_format_ltl[code.function_call.function_name]
        if mode == 'before':
            (function_string, specification_string, p_count) = create_ltl2ba_command_internal(code.function_call.values[0], p_count)
            return (
                function_string,
                symbol + '(' + specification_string + ')',
                p_count
            )
        function_strings = []
        specification_strings = []
        for value in code.function_call.values:
            (function_string, specification_string, p_count) = create_ltl2ba_command_internal(value, p_count)
            function_strings.append(function_string)
            specification_strings.append('(' + specification_string + ')')
        return (
            ''.join(function_strings),
            symbol.join(specification_strings),
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
        (function_string, command_string, p_count) = create_ltl2ba_command_internal(monitor.specification.code_statement, 0)
        with open (location + monitor.name + '.txt', 'w', encoding = 'utf-8') as output_file:
            output_file.write(command_string)
        with open (location + monitor.name + '.py', 'w', encoding = 'utf-8') as output_file:
            output_file.write(
                'SAFE = ' + (('\'' + monitor.safe_val + '\'') if isinstance(monitor.safe_val, str) else str(monitor.safe_val)) + os.linesep
                + 'UNSAFE = ' + (('\'' + monitor.unsafe_val + '\'') if isinstance(monitor.unsafe_val, str) else str(monitor.unsafe_val)) + os.linesep
                + 'UNKNOWN = ' + (('\'' + monitor.unknown_val + '\'') if isinstance(monitor.unknown_val, str) else str(monitor.unknown_val)) + os.linesep
            )
            output_file.write(function_string)
            output_file.write(
                'MODEL_INFO_FUNCTIONS = {' + os.linesep
                + ''.join(
                    (indent(1) + '\'p' + str(i) + '\' : p' + str(i) + '_func,' + os.linesep)
                    for i in range(p_count)
                )
                + '}' + os.linesep
            )
            output_file.write(
                'def model_state_to_model_info(model_state):' + os.linesep
                + indent(1) + 'return {' + os.linesep
                + indent(2) + 'key : item(model_state)' + os.linesep
                + indent(2) + 'for (key, item) in MODEL_INFO_FUNCTIONS.items()' + os.linesep
                + indent(1) + '}' + os.linesep
                + os.linesep
                + 'def transition(automaton_states, model_state):' + os.linesep
                + indent(1) + 'if ACCEPTING_STATE is not None and ACCEPTING_STATE in automaton_states:' + os.linesep
                + indent(2) + 'return ({ACCEPTING_STATE}, SAFE)' + os.linesep
                + indent(1) + 'if len(automaton_states) == 0:' + os.linesep
                + indent(2) + 'return (set(), UNSAFE)' + os.linesep
                + indent(1) + 'model_info = model_state_to_model_info(model_state)' + os.linesep
                + indent(1) + 'new_automaton_states = {' + os.linesep
                + indent(2) + 'new_automaton_state' + os.linesep
                + indent(2) + 'for automaton_state in automaton_states' + os.linesep
                + indent(2) + 'for (guard, new_automaton_state) in STATE_TRANS[automaton_state]' + os.linesep
                + indent(2) + 'if guard(model_info)' + os.linesep
                + indent(1) + '}' + os.linesep
                + indent(1) + 'if ACCEPTING_STATE is not None and ACCEPTING_STATE in new_automaton_states:' + os.linesep
                + indent(2) + 'return ({ACCEPTING_STATE}, SAFE)' + os.linesep
                + indent(1) + 'if len(new_automaton_states) == 0:' + os.linesep
                + indent(2) + 'return (set(), UNSAFE)' + os.linesep
                + indent(1) + 'return (new_automaton_states, UNKNOWN)' + os.linesep
                + os.linesep
                + 'def reset():' + os.linesep
                + indent(1) + 'return {INITIAL_STATE}' + os.linesep
            )
    return

def parse_ba(ba_file, python_file):
    state_trans = {}
    guards = []
    cur_state = ''
    initial_state = None
    accepting_state = None
    with open(ba_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if 'never {' in line:
                continue
            counter = line.count(':')
            if counter == 0:
                if 'skip' in line:
                    state_trans[cur_state].append(('guard__' + cur_state + '__TO__' + cur_state, cur_state))
                    guards.append('def ' + 'guard__' + cur_state + '__TO__' + cur_state + '(_):' + os.linesep + indent(1) + 'return True' + os.linesep)
                    accepting_state = cur_state
                continue
            if counter == 1:
                cur_state = line.split(':')[0].strip()
                state_trans[cur_state] = []
                if 'init' in cur_state:
                    initial_state = cur_state
                continue
            if counter == 2:
                line = line.replace(':', '')
                (guard, next_state) = line.split(' -> goto ')
                next_state = next_state.strip()
                guard = guard.strip()
                state_trans[cur_state].append(('guard__' + cur_state + '__TO__' + next_state, next_state))
                guards.append(
                    'def ' + 'guard__' + cur_state + '__TO__' + next_state + '(model_info):' + os.linesep
                    + indent(1) + 'return ' + re.sub(r'p[0-9]*', lambda x: 'model_info[\'' + x.group(0) + '\']', guard.replace('&&', 'and').replace('||', 'or').replace('!', 'not ')) + os.linesep
                )
                continue
    existing_info = ''
    with open(python_file, 'r', encoding = 'utf-8') as input_file:
        existing_info = input_file.read()
    with open(python_file, 'w', encoding = 'utf-8') as output_file:
        output_file.write(''.join(guards))
        output_file.write(os.linesep)
        output_file.write(
            'STATE_TRANS = {' + os.linesep
            + ''.join(
                (
                    indent(1) + '\'' + state + '\' : {' + os.linesep
                    + ''.join(
                        indent(2) + '(' + guard_state[0] + ', \'' + guard_state[1] + '\'),' + os.linesep
                        for guard_state in guard_states
                    )
                    + indent(1) + '},' + os.linesep
                )
                for (state, guard_states) in state_trans.items()
            )
            + '}' + os.linesep
        )
        if initial_state is None:
            raise ValueError('no initial state?')
        output_file.write('INITIAL_STATE = ' + '\'' + initial_state + '\'' + os.linesep)
        output_file.write('ACCEPTING_STATE = ' + (('\'' + accepting_state + '\'') if accepting_state is not None else str(accepting_state)) + os.linesep)
        output_file.write(existing_info)
    return

if __name__ == '__main__':
    if sys.argv[1] == 'command':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('metamodel_file')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        args = arg_parser.parse_args(sys.argv[2:])
        create_ltl2ba_command(args.metamodel_file, args.model_file, args.location, args.recursion_limit, args.no_checks)
    elif sys.argv[1] == 'mode':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('ba_file')
        arg_parser.add_argument('python_file')
        args = arg_parser.parse_args(sys.argv[2:])
        parse_ba(args.ba_file, args.python_file)
