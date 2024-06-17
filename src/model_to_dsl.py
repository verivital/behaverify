'''
Made by Serena Serafina Serbinowska
'''
import os

def model_to_dsl(model, output_file):
    '''Writes the model to a dsl. Assumes you have already added the monitor vars into the model.'''
    def format_function_loop(function_call):
        return (
            '(loop, ' + function_call.loop_variable + ', ' + ('reverse ' if function_call.reverse is not None else '')
            + (
                (
                    '{'
                    + ', '.join(map(format_code, function_call.loop_variable_domain))
                    + '}'
                )
                if function_call.min_val is None else
                ('[' + format_code(function_call.min_val) + ', ' + format_code(function_call.max_val) + ']')
            )
            + ' such_that ' + format_code(function_call.loop_condition)
            + ', '
            + format_code(function_call.values[0])
            + ')'
        )

    def format_function_case_loop(function_call):
        return (
            '(case_loop, ' + function_call.loop_variable + ', ' + ('reverse ' if function_call.reverse is not None else '')
            + (
                (
                    '{'
                    + ', '.join(map(format_code, function_call.loop_variable_domain))
                    + '}'
                )
                if function_call.min_val is None else
                ('[' + format_code(function_call.min_val) + ', ' + format_code(function_call.max_val) + ']')
            )
            + ' such_that ' + format_code(function_call.loop_condition)
            + ', '
            + format_code(function_call.values[0])
            + ', '
            + format_code(function_call.default_value)
            + ')'
        )

    def format_function_index(function_call):
        return (
            '(index, '  + format_code(function_call.to_index)
            + ' ' + (format_code(function_call.node_name) if function_call.node_name is not None else '')
            + ' ' + (format_code(function_call.read_at) if function_call.read_at is not None else '')
            + ' ' + (format_code(function_call.trace_num) if function_call.trace_num is not None else '')
            + ', '
            + ('constant_index ' if function_call.constant_index == 'constant_index' else '')
            + format_code(function_call.values[0])
            + ')'
        )

    def format_function_default(function_call):
        return (
            '(' + function_call.function_name + ', '
            + (
                ('[' + format_code(function_call.bound_statement.lower_bound) + ', ' + format_code(function_call.bound_statement.upper_bound) + '], ')
                if function_call.bound is not None else
                ''
            )
            + (
                ', '.join(map(format_code, function_call.values))
                if function_call.node_name is None else
                format_code(function_call.node_name)
            )
            + ')'
        )
    def format_function(function_call):
        if function_call.function_name == 'loop':
            return format_function_loop(function_call)
        if function_call.function_name == 'case_loop':
            return format_function_case_loop(function_call)
        if function_call.function_name == 'index':
            return format_function_index(function_call)
        return format_function_default(function_call)

    def handle_atom(code):
        atom_val = code.atom.constant if code.atom.constant is not None else code.atom.reference
        return (
            (('\'' + str(atom_val) + '\'') if atom_val in enumerations else str(atom_val))
            + ((' node ' + format_code(code.node_name)) if code.node_name is not None else '')
            + ((' at ' + format_code(code.read_at)) if code.read_at is not None else '')
            + ((' trace ' + format_code(code.trace_num)) if code.trace_num is not None else '')
        )

    def format_code(code):
        try:
            return (
                handle_atom(code)
                if code.atom is not None else
                (
                    ('(' + format_code(code.code_statement) + ')')
                    if code.code_statement is not None else
                    format_function(code.function_call)
                )
            )
        except AttributeError as e:
            return str(code)

    def handle_assign(assign):
        return (
            'assign{'
            + ''.join(
                [
                    ('case{' + format_code(case_result.condition) + '}result{' + ', '.join(map(format_code, case_result.values)) + '}')
                    for case_result in assign.case_results
                ]
            )
            + 'result{' + ', '.join(map(format_code, assign.default_result.values)) + '}'
            + '}'
        )

    def handle_array_index(array_index):
        return 'index_of{' + ', '.join(map(format_code, array_index.index_expr)) + '}' + handle_assign(array_index.assign)

    def handle_loop_array_index(loop_array_index):
        return (
            (
                '(loop, ' + loop_array_index.loop_variable + ', ' + ('reverse ' if loop_array_index.reverse is not None else '')
                + (
                    (
                        '{'
                        + ', '.join(map(format_code, loop_array_index.loop_variable_domain))
                        + '}'
                    )
                    if loop_array_index.min_val is None else
                    ('[' + format_code(loop_array_index.min_val) + ', ' + format_code(loop_array_index.max_val) + ']')
                )
                + ' such_that ' + format_code(loop_array_index.loop_condition)
                + ', '
                + handle_loop_array_index(loop_array_index.loop_array_index)
                + ')'
            )
            if loop_array_index.loop_array_index is not None else
            handle_array_index(loop_array_index.array_index)
        )

    def handle_variable_statement(statement):
        return (
            'variable_statement{'
            + ('instant ' if statement.instant else '')
            + (statement.variable.name if hasattr(statement.variable, 'name') else statement.variable)
            + ' '
            + (
                (
                    (
                        ('default{' + format_code(statement.default_value) + '}')
                        if hasattr(statement, 'default_value') and statement.default_value is not None else
                        ''
                    )
                    + statement.constant_index + ' ' + ' '.join(map(handle_loop_array_index, statement.assigns))
                )
                if statement.constant_index is not None and statement.constant_index == 'constant_index' else
                (
                    (
                        (
                            'iterative_assign, ' + statement.index_var_name + ' '
                            + ' '.join(
                                [
                                    ('condition{' + format_code(conditional.condition) + '}' + handle_assign(conditional.assign))
                                    for conditional in statement.iterative_assign_conditionals
                                ]
                            )
                            + ' '
                        )
                        if statement.iterative_assign is not None else
                        ''
                    )
                    + handle_assign(statement.assign)
                )
            )
            + '}' + os.linesep
        )

    def handle_read_statement(statement):
        return (
            'read_environment{' + statement.name + ' '
            + (
                (
                    'condition_variable{'
                    + (
                        (
                            '(' + statement.constant_index + ' ' + statement.condition_variable.name + ', ' + format_code(statement.index_of) + ')'
                        )
                        if statement.index_of is not None else
                        statement.condition_variable.name
                    )
                    + '}'
                )
                if statement.condition_variable is not None else
                ''
            )
            + 'condition{' + statement.non_determinism + (', ' if statement.non_determinism == 'non_determinism' else '') + format_code(statement.condition) + '}'
            + (os.linesep).join(map(handle_variable_statement, statement.variable_statements))
            + os.linesep
            + '}' + os.linesep
        )

    def handle_write_statement(statement):
        return (
            'write_environment{' + statement.name + ' '
            + (os.linesep).join(map(handle_variable_statement, statement.update))
            + os.linesep
            + '}' + os.linesep
        )

    def handle_statement(statement):
        return (
            handle_variable_statement(statement.variable_statement)
            if statement.variable_statement is not None else
            (
                handle_read_statement(statement.read_statement)
                if statement.read_statement is not None else
                (
                    handle_write_statement(statement.write_statement)
                    if statement.write_statement is not None else
                    ''
                )
            )
        )

    def handle_argument(argument):
        return (argument.argument_name + ' := ' +  argument.argument_type)

    def handle_tree(tree):
        if hasattr(tree, 'sub_root'):
            return 'insert{' + tree.sub_root.name + '}'
        if hasattr(tree, 'leaf'):
            return (
                ((tree.name + ' : ') if tree.name is not None else '')
                + tree.leaf.name
                + '{' + ', '.join(map(format_code, tree.leaf.arguments)) + '}'
            )
        if tree.node_type in {'X_is_Y', 'inverter'}:
            return (
                'decorator{' + tree.name + ' ' + tree.node_type + ' '
                + (
                    ('X ' + tree.x + ' Y ' + tree.y + ' ')
                    if tree.node_type == 'X_is_Y' else
                    ''
                )
                + 'child {' + handle_tree(tree.child) + '}'
                + '}' + os.linesep
            )
        return (
            'composite{' + tree.name + ' ' + tree.node_type + ' '
            + (
                ('policy ' + tree.parallel_policy + ' ')
                if tree.node_type == 'parallel' else
                ''
            )
            + tree.memory + ' '
            + 'children {' + (os.linesep).join(map(handle_tree, tree.children)) + '}'
            + '}' + os.linesep
        )

    enumerations = set(model.enumerations)
    output_string = (
        'configuration{ '
        + ('hypersafety ' if model.hypersafety else '')
        + ('use_reals ' if model.use_reals else '')
        + (
            (
                'neural{'
                + (model.neural.model_mode if model.neural.model_mode is not None else '')
                + ' '
                + (('total ' + str(model.neural.total)) if model.neural.total is not None else '')
                + ' '
                + (('int_part ' + str(model.neural.int_part)) if model.neural.int_part is not None else '')
                + ' '
                + (('float_part ' + str(model.neural.float_part)) if model.neural.float_part is not None else '')
                + '}'
            )
            if model.neural is not None else
            ''
        )
        + '}' + os.linesep
        + 'enumerations{' + ', '.join(map(lambda x: '\'' + x + '\'', model.enumerations)) + '}' + os.linesep
        + 'constants{' + ', '.join(map(lambda x: x.name + ' := ' + (('\'' + x.val + '\'') if x.val in enumerations else str(x.val)), model.constants)) + '}' + os.linesep
        + 'variables{'
        + ''.join(
            [
                (
                    'variable{' + variable.var_type + ' ' + variable.name + ' '
                    + (
                        (
                            'NEURAL '
                            + (
                                ('classification{' + ', '.join(map(format_code, variable.domain_codes)) + '}inputs{' + ', '.join(map(format_code, variable.inputs)) + '}')
                                if variable.neural_mode == 'classification' else
                                ('regression ' + variable.domain + ' inputs{' + ', '.join(map(format_code, variable.inputs)) + '}num_outputs{' + format_code(variable.num_outputs) + '}')
                            )
                            + ('table' if variable.table_mode else '')
                            + 'source{' + format_code(variable.source) + '}'
                        )
                        if variable.model_as == 'NEURAL' else
                        (
                            variable.model_as + ' '
                            + (
                                (variable.domain + ' ' + variable.static)
                                if variable.model_as == 'DEFINE' else
                                (
                                    variable.domain
                                    if isinstance(variable.domain, str) else
                                    (
                                        'BOOLEAN'
                                        if variable.domain.boolean is not None else
                                        (
                                            'INT'
                                            if variable.domain.true_int is not None else
                                            (
                                                'REAL'
                                                if variable.domain.true_real is not None else
                                                (
                                                    ('[' + format_code(variable.domain.min_val) + ', ' + format_code(variable.domain.max_val) + ']')
                                                    if variable.domain.min_val is not None else
                                                    ('{' + ', '.join(map(format_code, variable.domain.domain_codes)) + '}')
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                            + ' '
                            + (
                                (
                                    'array ' + format_code(variable.array_size) + ' '
                                    + (
                                        (
                                            'iterative_assign, ' + variable.index_var_name + ' '
                                            + ' '.join(
                                                [
                                                    ('condition{' + format_code(conditional.condition) + '}' + handle_assign(conditional.assign))
                                                    for conditional in variable.iterative_assign_conditionals
                                                ]
                                            )
                                            + handle_assign(variable.assign)
                                        )
                                        if variable.iterative_assign is not None else
                                        (
                                            'default{' + handle_assign(variable.default_value) + '} '
                                            + variable.constant_index + ' '
                                            + ' '.join(map(handle_loop_array_index, variable.assigns))
                                        )
                                    )
                                )
                                if variable.array_size is not None else
                                handle_assign(variable.assign)
                            )
                        )
                    )
                    + '}' + os.linesep
                )
                for variable in model.variables
            ]
        )
        + '}' + os.linesep
        + 'environment_update{'
        + (os.linesep).join(map(handle_variable_statement, model.update))
        + os.linesep
        + '}' + os.linesep
        + 'monitors{}' + os.linesep
        + 'checks{' + os.linesep
        + (os.linesep).join(
            [
                (
                    'check{' + node.name + ' arguments{' + ', '.join(map(handle_argument, node.arguments)) + '}' + os.linesep
                    + 'read_variables{' + ', '.join(map(lambda x: x.name, node.read_variables)) + '}' + os.linesep
                    + 'condition{' + format_code(node.condition) + '}'
                    + '}' + os.linesep
                )
                for node in model.check_nodes
            ]
        )
        + os.linesep
        + '}' + os.linesep
        + 'environment_checks{' + os.linesep
        + (os.linesep).join(
            [
                (
                    'environment_check{' + node.name + ' arguments{' + ', '.join(map(handle_argument, node.arguments)) + '}' + os.linesep
                    + 'read_variables{' + ', '.join(map(lambda x: x.name, node.read_variables)) + '}' + os.linesep
                    + 'condition{' + format_code(node.condition) + '}'
                    + '}' + os.linesep
                )
                for node in model.environment_checks
            ]
        )
        + os.linesep
        + '}' + os.linesep
        + 'actions{' + os.linesep
        + (os.linesep).join(
            [
                (
                    'action{' + node.name + ' arguments{' + ', '.join(map(handle_argument, node.arguments)) + '}' + os.linesep
                    + 'local_variables{' + ', '.join(map(lambda x: (x.name if hasattr(x, 'name') else x), node.local_variables)) + '}' + os.linesep
                    + 'read_variables{' + ', '.join(map(lambda x: (x.name if hasattr(x, 'name') else x), node.read_variables)) + '}' + os.linesep
                    + 'write_variables{' + ', '.join(map(lambda x: (x.name if hasattr(x, 'name') else x), node.write_variables)) + '}' + os.linesep
                    + 'initial_values{'
                    + (os.linesep).join(map(handle_variable_statement, node.init_statements))
                    + os.linesep
                    + '}' + os.linesep
                    + 'update{'
                    + (os.linesep).join(map(handle_statement, node.pre_update_statements))
                    + 'return_statement{'
                    + (os.linesep).join(
                        [
                            ('case{' + format_code(case_result.condition) + '}result{' + case_result.status + '}')
                            for case_result in node.return_statement.case_results
                        ]
                    )
                    + 'result{' + node.return_statement.default_result.status + '}'
                    + '}'
                    + (os.linesep).join(map(handle_statement, node.post_update_statements))
                    + '}' + os.linesep
                    + '}' + os.linesep
                )
                for node in model.action_nodes
            ]
        )
        + os.linesep
        + '}' + os.linesep
        + 'sub_trees{'
        + (os.linesep).join(
            [
                (
                    'sub_tree{' + sub_tree.name + os.linesep
                    + handle_tree(sub_tree.sub_root) + os.linesep
                    + '}'
                )
                for sub_tree in model.sub_trees
            ]
        )
        + '}' + os.linesep
        + 'tree{'
        + handle_tree(model.root)
        + os.linesep
        + '}' + os.linesep
        + 'tick_prerequisite{'
        + format_code(model.tick_condition)
        + '}' + os.linesep
        + 'specifications {'
        + (os.linesep).join(
            [
                (spec.spec_type + '{' + format_code(spec.code_statement) + '}')
                for spec in model.specifications
            ]
        )
        + '}' + os.linesep
    )
    with open(output_file, 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(output_string)
