import os
import argparse
import re
import sys
from check_grammar import validate_model
from serene_functions import build_meta_func
from behaverify_common import indent, create_node_name, is_local, is_env, is_blackboard, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max, variable_type, BTreeException, constant_type, is_array

def create_ltl2ba_command(metamodel_file, model_file, location, recursion_limit, no_checks):
    def type_conversion(input_type):
        if input_type == 'ENUM':
            return 'char *'
        if input_type == 'BOOLEAN':
            return '_Bool'
        if input_type == 'INT':
            return 'int'
        if input_type == 'REAL':
            return 'float'
    def format_variable_with_type(variable):
        # print(variable)
        var_type = variable_type(variable, declared_enumerations, constants)
        return (format_variable_name_only(variable), type_conversion(var_type) + ' ' + format_variable_name_only(variable) + ('[]' if is_array(variable) else ''))
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
        return ['(' + format_code(function_call.values[0])[0] + ' ? ' + format_code(function_call.values[1])[0] + ' : ' + format_code(function_call.values[2])[0] + ')']
    def format_function_min(_, function_call):
        val0 = format_code(function_call.values[0])[0]
        val1 = format_code(function_call.values[1])[0]
        return ['((' + val0  + ' < ' + val1 + ') ? ' + val0 + ' : ' + val1 + ')']
    def format_function_max(_, function_call):
        val0 = format_code(function_call.values[0])[0]
        val1 = format_code(function_call.values[1])[0]
        return ['((' + val0  + ' > ' + val1 + ') ? ' + val0 + ' : ' + val1 + ')']

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
        return ['(' + format_code(function_call.cond_value)[0] + ' ? ' + format_code(function_call.values[0])[0] + ' : ' + format_case_loop_recursive(function_call, cond_func, values, index + 1)[0] + ')']

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
        for value in function_call.values:
            if value.atom is not None:
                (_, atom_type, _) = handle_constant_or_reference(value.atom, declared_enumerations, {}, variables, constants, loop_references)
                if atom_type == 'ENUM':
                    return [
                        '(strcmp(' 
                        + ', '.join([', '.join(format_code(value)) for value in function_call.values])
                        + ') ' + function_name + ' 0)'
                    ]
        return [
            '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value)) for value in function_call.values])
            + ')'
        ]

    def format_function_implies(_, function_call):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value))
        return ['(' + '(! ' + formatted_values[0] + ') || ' + formatted_values[1] + ')']

    def format_function_division(_, function_call):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value))
        return ['((int)(' + formatted_values[0] + ' / ' + formatted_values[1] + '))']

    def format_function_xnor(_, function_call):
        return ['(! (' + function_format['xor'][1](function_format['xor'][0], function_call)[0] + '))']

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
        return [formatted_variable + '[' + formatted_index + ']']

    def format_function(code):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call)

    def format_variable_name_only(variable):
        return variable.name

    def format_variable(variable):
        return format_variable_name_only(variable)

    def str_conversion(atom_type, atom):
        if atom_type in ('VARIABLE', 'NODE'):
            return str(atom)
        if atom_type == 'CONSTANT':
            atom_type = constant_type(atom, declared_enumerations)
        return (
            ('"' + atom + '"')
            if atom_type == 'ENUM' else
            (
                ('1' if atom else '0')
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
                    'static _Bool p' + str(p_count) + '_func(' + current_arguments + '){return ' + format_code(code)[0] + ';}' + os.linesep
                ),
                (
                    '_Bool p' + str(p_count) + '_func(' + current_arguments + ');' + os.linesep
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
            # all before cases that are relevant here take exactly one argument.
            (function_string, declaration_string, specification_string, p_count) = create_ltl2ba_command_internal(code.function_call.values[0], p_count)
            return (
                function_string,
                declaration_string,
                symbol + '(' + specification_string + ')',
                p_count
            )
        function_strings = []
        declaration_strings = []
        specification_strings = []
        for value in code.function_call.values:
            (function_string, declaration_string, specification_string, p_count) = create_ltl2ba_command_internal(value, p_count)
            function_strings.append(function_string)
            declaration_strings.append(declaration_string)
            specification_strings.append('(' + specification_string + ')')
        return (
            ''.join(function_strings),
            ''.join(declaration_strings),
            symbol.join(specification_strings),
            p_count
        )

    def find_used_variables_without_formatting_in_code(code):
        if code.atom is not None:
            (atom_class, atom) = handle_constant_or_reference_no_type(code.atom, declared_enumerations, {}, variables, constants, loop_references)
            return [atom] if atom_class == 'VARIABLE' else []
        if code.code_statement is not None:
            return find_used_variables_without_formatting_in_code(code.code_statement)
        function_call = code.function_call
        if function_call.function_name == 'loop':
            return execute_loop(function_call, find_used_variables_without_formatting_in_code, function_call.values[0])
        if function_call.function_name == 'case_loop':
            return (
                execute_loop(function_call, find_used_variables_without_formatting_in_code, function_call.cond_value)
                + execute_loop(function_call, find_used_variables_without_formatting_in_code, function_call.values[0])
                + find_used_variables_without_formatting_in_code(function_call.default_value)
            )
        used_variables = []
        for value in function_call.values:
            used_variables.extend(find_used_variables_without_formatting_in_code(value))
        if function_call.function_name != 'index':
            return used_variables
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        used_variables.append(variable)
        return used_variables

    function_format = {
        'if' : ('', format_function_if),
        'loop' : ('', format_function_loop),
        'case_loop' : ('', format_function_case_loop),
        'abs' : ('abs', format_function_before),
        'max' : ('max', format_function_max),
        'min' : ('min', format_function_min),
        # 'sin' : ('math.sin', format_function_before),
        # 'cos' : ('math.cos', format_function_before),
        # 'tan' : ('math.tan', format_function_before),
        # 'ln' : ('math.log', format_function_before),
        'not' : ('!', format_function_before),
        'and' : ('&&', format_function_between),
        'or' : ('||', format_function_between),
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
        # 'floor' : ('math.floor', format_function_before),
        # 'count' : ('count', format_function_count), # not implemented
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
    current_arguments = None
    for monitor in model.monitors:
        current_variables = find_used_variables_without_formatting_in_code(monitor.specification.code_statement)
        current_variables = sorted(list(set(map(format_variable_with_type, current_variables))))
        current_arguments = ', '.join(map(lambda x: x[1], current_variables))
        current_arguments_without_type = ', '.join(map(lambda x: x[0], current_variables))
        (function_string_, _, command_string, p_count) = create_ltl2ba_command_internal(monitor.specification.code_statement, 0)
        with open (location + monitor.name + '.txt', 'w', encoding = 'utf-8') as output_file:
            output_file.write(command_string)
        with open (location + monitor.name + '.h', 'w', encoding = 'utf-8') as output_file:
            # output_file.write(
            #     'extern int SAFE;' + os.linesep
            #     + 'extern int UNKNOWN;' + os.linesep
            #     + 'extern int UNSAFE;' + os.linesep
            #     + ''.join([('extern _Bool p' + str(index) + ';' + os.linesep) for index in range(p_count)])
            # )
            # output_file.write(declaration_string_)
            # output_file.write(
            #     'void set_p_values(' + current_arguments + ');' + os.linesep
            #     + 'int transition(_Bool *current_states, _Bool *next_states, ' + current_arguments + ');' + os.linesep
            #     + 'void reset(_Bool *states);' + os.linesep
            # )
            output_file.write(
                '#ifndef ' + monitor.name.upper() + '_INCLUDED' + os.linesep
                + '#define ' + monitor.name.upper() + '_INCLUDED' + os.linesep
                + '#include <stdint.h>' + os.linesep
                + '#include <string.h>' + os.linesep
                + '#include <stdbool.h>' + os.linesep
                + 'int ' + monitor.name + '_transition(_Bool *current_states, _Bool *next_states, ' + current_arguments + ');' + os.linesep
                + 'void ' + monitor.name + '_reset(_Bool *states);' + os.linesep
                + '#endif' + os.linesep
            )
        with open (location + monitor.name + '.c', 'w', encoding = 'utf-8') as output_file:
            output_file.write(
                'static int SAFE = 0;' + os.linesep
                + 'static int UNKNOWN = 1;' + os.linesep
                + 'static int UNSAFE = 2;' + os.linesep
                + ''.join([('static _Bool p' + str(index) + ';' + os.linesep) for index in range(p_count)])
                + '/*SPLIT ON ME*/' + os.linesep
            )
            output_file.write(function_string_)
            output_file.write(
                'static void set_p_values(' + current_arguments + '){' + os.linesep
                + ''.join(
                    [
                        (
                            indent(1) + 'p' + str(index) + ' = p' + str(index) + '_func(' + current_arguments_without_type + ');' + os.linesep
                        )
                    for index in range(p_count)
                    ]
                )
                + '}' + os.linesep
                + 'int ' + monitor.name + '_transition(_Bool *current_states, _Bool *next_states, ' + current_arguments + '){' + os.linesep
                + indent(1) + 'if (ACCEPTING_STATE_EXISTS && current_states[NUM_STATES - 1]){*next_states = *ACCEPTING_STATE; return SAFE;}' + os.linesep
                + indent(1) + 'if (evaluate_safety_of_states(current_states) == UNSAFE){*next_states = *REJECTING_STATE; return UNSAFE;}' + os.linesep
                + indent(1) + 'set_p_values(' + current_arguments_without_type + ');' + os.linesep
                + indent(1) + 'state_trans(current_states, next_states);' + os.linesep
                + indent(1) + 'return evaluate_safety_of_states(next_states);' + os.linesep
                + '}' + os.linesep
                + 'void ' + monitor.name + '_reset(_Bool *state){*state = *INITIAL_STATE;}' + os.linesep
            )
    return

def parse_ba(ba_file, c_file, h_file):
    state_trans = {}
    guards = []
    cur_state = ''
    initial_state = None
    accepting_state = None
    header_functions = []
    with open(ba_file, 'r', encoding = 'utf-8') as input_file:
        for line in input_file.readlines():
            if 'never {' in line:
                continue
            counter = line.count(':')
            if counter == 0:
                if 'skip' in line:
                    if cur_state not in state_trans:
                        state_trans[cur_state] = []
                    state_trans[cur_state].append(('guard__' + cur_state + '__TO__' + cur_state, cur_state))
                    guards.append('static _Bool guard__' + cur_state + '__TO__' + cur_state + '(void){return true;}' + os.linesep)
                    header_functions.append('_Bool guard__' + cur_state + '__TO__' + cur_state + '(void);' + os.linesep)
                    accepting_state = cur_state
                continue
            if counter == 1:
                cur_state = line.split(':')[0].strip()
                if 'init' in cur_state:
                    initial_state = cur_state
                continue
            if counter == 2:
                line = line.replace(':', '')
                (guard, next_state) = line.split(' -> goto ')
                next_state = next_state.strip()
                guard = guard.strip()
                if next_state not in state_trans:
                    state_trans[next_state] = []
                state_trans[next_state].append(('guard__' + cur_state + '__TO__' + next_state, cur_state))
                guards.append('static _Bool guard__' + cur_state + '__TO__' + next_state + '(void){return ' + guard + ';}' + os.linesep)
                header_functions.append('_Bool guard__' + cur_state + '__TO__' + cur_state + '(void);' + os.linesep)
                continue
    state_index = {}
    count = 0
    listed_initial = None
    listed_final = None
    for state in state_trans:
        state_index[state] = count
        if count == 0:
            listed_initial = state
        listed_final = state
        count = count + 1
    if initial_state != listed_initial:
        cur_index = state_index[initial_state]
        state_index[initial_state] = 0
        state_index[listed_initial] = cur_index
    if accepting_state is not None and accepting_state != listed_final:
        cur_index = state_index[accepting_state]
        state_index[accepting_state] = count - 1
        state_index[listed_final] = cur_index
    existing_c_info = ''
    with open(c_file, 'r', encoding = 'utf-8') as input_file:
        existing_c_info = input_file.read()
    (pre_info, post_info) = existing_c_info.split('/*SPLIT ON ME*/', 1)
    with open(c_file, 'w', encoding = 'utf-8') as output_file:
        output_file.write(
            '#include "' + os.path.basename(h_file) + '"' + os.linesep
        )
        output_file.write(pre_info)
        if initial_state is None:
            raise ValueError('no initial state?')
        output_file.write('static _Bool INITIAL_STATE[' + str(len(state_trans)) + '] = {' + ', '.join(['1'] + (['0'] * (len(state_trans) - 1))) + '};' + os.linesep)
        output_file.write('static _Bool ACCEPTING_STATE[' + str(len(state_trans)) + '] = {' + ', '.join((['0'] * (len(state_trans) - 1)) + (['1'] if accepting_state is not None else ['0'])) + '};' + os.linesep)
        output_file.write('static _Bool REJECTING_STATE[' + str(len(state_trans)) + '] = {' + ', '.join((['0'] * (len(state_trans)))) + '};' + os.linesep)
        output_file.write('static _Bool ACCEPTING_STATE_EXISTS = ' + ('1' if accepting_state is not None else '0') + ';' + os.linesep)
        output_file.write('static int NUM_STATES = ' + str(len(state_trans)) + ';' + os.linesep)
        output_file.write(
            'static int evaluate_safety_of_states(_Bool *states){' + os.linesep
            + indent(1) + 'if (ACCEPTING_STATE_EXISTS && states[NUM_STATES - 1]){return SAFE;}' + os.linesep
            + indent(1) + 'if (' + ' || '.join([('states[' + str(index) + ']') for index in range(len(state_trans))]) + '){return UNKNOWN;}' + os.linesep
            + indent(1) + 'return UNSAFE;' + os.linesep
            + '}' + os.linesep
        )
        output_file.write(''.join(guards))
        output_file.write(os.linesep)
        output_file.write(
            'static void state_trans(_Bool *current_states, _Bool *next_states){' + os.linesep
            + ''.join(
                [
                    (
                        indent(1) + 'next_states[' + str(state_index[to_state]) + '] = ('
                        + ' || '.join(
                            [
                                (
                                    '(current_states[' + str(state_index[from_state]) + '] && ' + guard + '())'
                                )
                                for (guard, from_state) in state_trans[to_state]
                            ]
                        )
                        + ');' + os.linesep
                    )
                    for to_state in state_trans
                ]
            )
            + '}' + os.linesep
        )
        output_file.write(post_info)
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
        arg_parser.add_argument('ba_file')
        arg_parser.add_argument('c_file')
        arg_parser.add_argument('h_file')
        args = arg_parser.parse_args(sys.argv[2:])
        parse_ba(args.ba_file, args.c_file, args.h_file)
