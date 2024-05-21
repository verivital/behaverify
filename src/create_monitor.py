
def create_ltl2ba_command(specification, declared_enumerations, variables, constants):
    def execute_loop(function_call, to_call, packaged_args, misc_args):
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
                return_vals.extend(to_call(packaged_args, misc_args))
            loop_references.pop(function_call.loop_variable)
        return return_vals

    def execute_code(code):
        cur_func = build_meta_func(code)
        return cur_func((constants, loop_references))

    def format_function_if(_, function_call, misc_args):
        return ['(' + format_code(function_call.values[1], misc_args)[0] + ' if ' + format_code(function_call.values[0], misc_args)[0] + ' else ' + format_code(function_call.values[2], misc_args)[0] + ')']

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, function_call.values[0], misc_args)

    def format_case_loop_recursive(function_call, misc_args, cond_func, values, index):
        if len(values) == index:
            if function_call.loop_variable in loop_references:
                loop_references.pop(function_call.loop_variable)
            return format_code(function_call.default_value, misc_args)
        loop_references[function_call.loop_variable] = values[index]
        if not cond_func((constants, loop_references))[0]:
            return format_case_loop_recursive(function_call, misc_args, cond_func, values, index + 1)
        return ['(' + format_code(function_call.values[0], misc_args)[0] + ' if ' + format_code(function_call.cond_value, misc_args)[0] + ' else ' + format_case_loop_recursive(function_call, misc_args, cond_func, values, index + 1)[0] + ')']

    def format_function_case_loop(_, function_call, misc_args):
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
        return format_case_loop_recursive(function_call, misc_args, cond_func, all_domain_values, 0)

    def format_function_before(function_name, function_call, misc_args):
        return [
            function_name + '('
            + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_between(function_name, function_call, misc_args):
        return [
            '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_implies(_, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return ['(' + '(not ' + formatted_values[0] + ') or ' + formatted_values[1] + ')']

    def format_function_division(_, function_call, misc_args):
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return ['(int(' + formatted_values[0] + ' / ' + formatted_values[1] + '))']

    def format_function_xnor(_, function_call, misc_args):
        return ['(not (' + function_format['xor'][1](function_format['xor'][0], function_call, misc_args)[0] + '))']

    def format_function_count(_, function_call, misc_args):
        return [
            '('
            + '[' + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values]) + '].count(True)'
            + ')'
        ]

    def format_function_index(_, function_call, misc_args):
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
        formatted_variable = format_variable_name_only(variable, misc_args)
        formatted_index = ''
        if function_call.constant_index == 'constant_index':
            index_func = build_meta_func(function_call.values[0])
            index = resolve_potential_reference_no_type(index_func((constants, loop_references))[0], declared_enumerations, {}, variables, constants, loop_references)[1]
            formatted_index = str(index)
        else:
            formatted_index = format_code(function_call.values[0], misc_args)[0]
        return [
            (formatted_variable + '(' + formatted_index + ')')
            if variable.model_as in ('DEFINE', 'NEURAL') and variable.static != 'static' else
            (
                formatted_variable + '['
                + (
                    ('serene_safe_assignment.index_func(' + formatted_index + ', ' + str(variable_array_size_map[variable.name]) + ')')
                    if safe_assignment else
                    formatted_index
                )
                + ']'
            )
        ]

    def format_function(code, misc_args):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def format_variable_name_only(variable, misc_args):
        return (
            (
                ('node.' if is_local(variable) else ('self.' if is_env(variable) else 'self.blackboard.'))
                if misc_args['loc'] == 'environment' else
                (
                    'blackboard_reader.'
                    if misc_args['loc'] == 'blackboard' else
                    (
                        ('self.' + ('' if is_local(variable) else 'blackboard.'))
                        if misc_args['loc'] == 'node' else
                        (
                            ('node.' if is_local(variable) else ('self.environment.' if is_env(variable) else 'self.blackboard.'))
                            if misc_args['loc'] == 'random' else
                            'ERROR ERROR ERROR'
                        )
                    )
                )
            )
            + variable.name
        )

    def format_variable(variable, misc_args):
        return format_variable_name_only(variable, misc_args) + ('()' if variable.model_as in ('DEFINE', 'NEURAL') and variable.static != 'static' else '')

    def handle_atom(code, misc_args):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException as bt_e:  # this should be an argument.
            if misc_args['loc'] == 'node':
                return 'self.' + code.atom.reference
            if misc_args['loc'] in {'environment', 'random'}:
                return 'node.' + code.atom.reference
            raise BTreeException([], 'Encountered unknown reference: ' + str(code.atom.reference)) from bt_e
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom, misc_args)

    def format_code(code, misc_args):
        return (
            [handle_atom(code, misc_args)]
            if code.atom is not None else
            (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)]
                if code.code_statement is not None else
                format_function(code, misc_args)
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
                    + indent(1) + 'return ' + format_code(code) + os.linesep
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
            ''.join(function_string),
            symbol.join(specification_strings),
            p_count
        )
