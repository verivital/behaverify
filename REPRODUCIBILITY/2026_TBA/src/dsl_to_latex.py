'''
This module is for internal use with BehaVerify.
It is used to convert .tree files to tikz.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2025-04-22
'''
import argparse
import os
from behaverify_common import create_node_name, is_local, is_env, is_neural, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max, BTreeException, constant_type
from serene_functions import build_meta_func
from check_grammar import validate_model

def indent(indent_level):
    return '\\begin{math}' + ('\\quad{}' * (indent_level)) + '\\end{math}'


def write_files(metamodel_file, model_file, output_file, insert_only, recursion_limit, on_sides):
    '''
    Used to write all the files.
    @metamodel_file ::> points to the file with the metamodel
    @model_file ::> points to the file with the model
    @main_name ::> main name to be used for files
    @write_location ::> where to write files
    @serene_print ::> boolean, should we use custom printing?
    @max_iter ::> how many iterations
    @no_var_print ::> turns off printing vars
    @py_tree_print ::> turns on PyTree printing
    '''

    # misc_args variable explained
    # misc_args is a dict {'init' : init, 'loc' : loc, 'indent_level' : indent_level}.
    # init is a boolean. if true, it means we are initializing. if false, we are not.
    # loc is a location. location can be node, blackboard, or environment, or DEFINE. DEFINE means we don't add { and } in some places.
    def create_misc_args(init, loc, indent_level):
        return {'init' : init, 'loc' : loc, 'indent_level' : indent_level}

    def str_conversion(atom_type, atom):
        if atom_type in ('VARIABLE', 'NODE'):
            return str(atom)
        if atom_type == 'CONSTANT':
            atom_type = constant_type(atom, declared_enumerations)
        return (
            ('\\texttt{\\textquotesingle{}' + atom + '\\textquotesingle{}}')
            if atom_type == 'ENUM' else
            (
                ('\\' + str(atom) + '{}')
                if atom_type == 'BOOLEAN' else
                (
                    ('(' + str(atom) + ')')
                    if atom < 0 else
                    str(atom)
                )
            )
        )

    def str_conversion_executed(executed):
        cur_type = type(executed)
        if cur_type == str:
            return str_conversion('ENUM', executed)
        if cur_type == bool:
            return str_conversion('BOOLEAN', executed)
        return str_conversion('NUMBER', executed)

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

    def format_function_one_arg(function_name, function_call, misc_args):
        return [function_name + '{' + format_code(function_call.values[0], misc_args) + '}']

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
        return [(formatted_variable + '[' + formatted_index + ']')]

    def format_function(code, misc_args):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def format_variable_name_only(variable, misc_args):
        return (
            (
                ('\\EnvVarTikz{')
                if is_env(variable) else
                (
                    ('\\NeuralVarTikz{')
                    if is_neural(variable) else
                    ('\\BlVarTikz{' + ('node.' if is_local(variable) else ''))
                )
            ) + variable.name + '}'
        )

    def format_variable(variable, misc_args):
        return format_variable_name_only(variable, misc_args)# + ('()' if variable.model_as == 'DEFINE' else '')

    def handle_atom(code, misc_args):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException as bt_e:  # this should be an argument.
            return '\\texttt{' + code.atom.reference + '}'
            # if misc_args['loc'] == 'node':
            #     return 'self.' + code.atom.reference
            # if misc_args['loc'] == 'environment':
            #     return 'node.' + code.atom.reference
            # raise BTreeException([], 'Encountered unknown reference: ' + str(code.atom.reference)) from bt_e
        return str_conversion(atom_type, atom) if atom_class == 'CONSTANT' else format_variable(atom, misc_args)

    def code_is_constant(code, misc_args):
        if code.atom is not None:
            try:
                (atom_class, _, _) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
            except BTreeException as bt_e:  # this should be an argument.
                # print('hello!')
                return [False] # arguments are functionally variables for our purpose.
            # print(str(atom_class) + ':---:' + str(atom))
            return [atom_class == 'CONSTANT']
        if code.code_statement is not None:
            return code_is_constant(code.code_statement, misc_args)
        function_call = code.function_call
        if function_call.function_name == 'loop':
            return [all(execute_loop(function_call, code_is_constant, function_call.values[0], misc_args))]
        if function_call.function_name == 'case_loop':
            return [all(
                execute_loop(function_call, code_is_constant, function_call.cond_value, misc_args)
                + execute_loop(function_call, code_is_constant, function_call.values[0], misc_args)
                + code_is_constant(function_call.default_value, misc_args)
            )]
        for value in function_call.values:
            if not (code_is_constant(value, misc_args))[0]:
                return [False]
        if function_call.function_name == 'index':
            return [False]
        return [True]

    def format_code(code, misc_args):
        try:
            if code_is_constant(code, misc_args)[0]:
                # print(list(map(str_conversion_executed, execute_code(code))))
                return list(map(str_conversion_executed, execute_code(code)))
        except Exception as e:
            print('FAILED:' + str(e))
            # print('FAILED')
            pass
        return (
            [handle_atom(code, misc_args)]
            if code.atom is not None else
            (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)]
                if code.code_statement is not None else
                format_function(code, misc_args)
            )
        )

    def update_method_check(node):
        return (
            '\\node[Blackboard](..--REPLACE--..){\\begin{tabular}{l}'
            + ('\\texttt{if }\\begin{math}' + format_code(node.condition, create_misc_args(False, 'node', 2))[0] + '\\end{math}\\texttt{:}\\\\{}\\begin{math}\\quad{}\\NodeStatusTikz{}\\coloneqq{} \\SuccessTikz{}\\end{math}\\\\{}\\texttt{else:}\\\\{}\\begin{math}\\quad{}\\NodeStatusTikz{}\\coloneqq{}\\FailureTikz{}\\end{math}')
            + '\\end{tabular}};'
        )

    def update_method_environment_check(node):
        return update_method_check(node)

    def resolve_variable_nondeterminism(values, misc_args):
        formatted_values = []
        no_bracket = misc_args['loc'] == 'DEFINE'
        for value in values:
            formatted_values.extend(format_code(value, misc_args))
        try:
            if len(formatted_values) > 1:
                int_vals = list(map(int, formatted_values))
                int_vals.sort()
                if all(((i + int_vals[0]) == int_vals[i]) for i in range(len(int_vals))):
                    formatted_values = ['[' + str(int_vals[0]) + ', ' + str(int_vals[-1]) + ']']
                    no_bracket = True
        except:
            pass
        return ('' if no_bracket else '\\{') + ', '.join(formatted_values) + ('' if no_bracket else '\\}')

    def handle_assign(assign, misc_args):
        case_results = assign.case_results
        default_result = assign.default_result
        if len(case_results) == 0:
            return '\\begin{math}' + resolve_variable_nondeterminism(default_result.values, misc_args) + '\\end{math}' # NOTE: no linesep at the end!
        return_string = ''
        branch_count = 0
        truth_terminated = False
        for case_result in case_results:
            cond = format_code(case_result.condition, misc_args)[0]
            if cond == '\\True{}':
                return_string += ('' if branch_count == 0 else indent(misc_args['indent_level'] + branch_count)) + '\\begin{math}' + resolve_variable_nondeterminism(case_result.values, misc_args) + '\\end{math}'
                truth_terminated = True
                break
            if cond == '\\False{}':
                continue
            return_string += (
                ('' if branch_count == 0 else indent(misc_args['indent_level'] + 1 + branch_count)) + '\\texttt{(}'
                + '\\begin{math}' + resolve_variable_nondeterminism(case_result.values, misc_args) + '\\end{math}\\\\'
                + indent(misc_args['indent_level'] + 1 + branch_count) + '\\texttt{if }\\begin{math}' + format_code(case_result.condition, misc_args)[0] + '\\end{math}\\texttt{ else}' + '\\\\'
            )
            branch_count = branch_count + 1
        if not truth_terminated:
            return_string += ('' if branch_count == 0 else indent(misc_args['indent_level'] + branch_count)) + '\\begin{math}' + resolve_variable_nondeterminism(default_result.values, misc_args) + '\\end{math}'
        return_string += '\\texttt{' + (')' * (branch_count)) + '}'
        return return_string
        # return (
        #     '\\texttt{(}'
        #     + ''.join(
        #         [
        #             (
        #                 # indent(misc_args['indent_level'] + 1 + index) +
        #                 '\\begin{math}' + resolve_variable_nondeterminism(case_result.values, misc_args) + '\\end{math}\\\\'
        #                 + indent(misc_args['indent_level'] + 1 + index) + '\\texttt{if }\\begin{math}' + format_code(case_result.condition, misc_args)[0] + '\\end{math}\\texttt{ else}' + '\\\\'
        #                 + indent(misc_args['indent_level'] + 1 + index) + '\\texttt{(}'
        #              ) for index, case_result in enumerate(case_results)
        #         ]
        #     )
        #     # + indent(misc_args['indent_level'] + len(case_results))
        #     + '\\begin{math}' + resolve_variable_nondeterminism(default_result.values, misc_args) + '\\end{math}'# + '$\\\\$'
        #     # + indent(misc_args['indent_level'])
        #     + '\\texttt{' + (')' * (1 + len(case_results))) + '}'  # NOTE: no linesep at the end!
        # )

    def handle_loop_array_index(packed_args, misc_args):
        (loop_array_index, constant_index) = packed_args
        if loop_array_index.array_index is not None:
            results = handle_assign(loop_array_index.array_index.assign, misc_args)
            indices = []
            for index_expr in loop_array_index.array_index.index_expr:
                if constant_index:
                    index_func = build_meta_func(index_expr)
                    for index in index_func((constants, loop_references)):
                        new_index = resolve_potential_reference_no_type(index, declared_enumerations, {}, variables, constants, loop_references)[1]
                        indices.append(str(new_index))
                else:
                    for index in format_code(index_expr, misc_args):
                        indices.append(index)
            return [(indices, results)]
        return execute_loop(loop_array_index, handle_loop_array_index, (loop_array_index.loop_array_index, constant_index), misc_args)

    def variable_assignment(variable, assign_value, misc_args, array_mode):
        '''
        array_mode in {0, 1, 2} -> 0 means no, 1 means yes, 2 means iterative assign
        '''
        # i don't think we should be able to have define variables here.
        assign_token = (' \\in ' if variable.model_as in ('VAR', 'FROZENVAR') else ' \\coloneqq{} ')
        return (
            (
                indent(misc_args['indent_level']) + '\\begin{math}\\texttt{temp} \\coloneqq{}\\end{math}' + assign_value + '\\\\'
                + (
                    (
                        indent(misc_args['indent_level']) + '\\texttt{for (index, val) in temp:}\\\\'
                        + indent(misc_args['indent_level'] + 1) + '\\begin{math}' + format_variable_name_only(variable, misc_args) + '[\\texttt{index}]' + assign_token + '\\texttt{val}' + '\\end{math}\\\\'
                    )
                    if array_mode == 1 else
                    (
                        indent(misc_args['indent_level']) + '\\texttt{for index in len(temp):}\\\\'
                        + indent(misc_args['indent_level'] + 1) + '\\begin{math}' + format_variable_name_only(variable, misc_args) + '[\\texttt{index}]' + assign_token + '\\texttt{temp[index]}' + '\\end{math}\\\\'
                    )
                )
            )
            if array_mode > 0 else
            (indent(misc_args['indent_level']) + '\\begin{math}' + format_variable_name_only(variable, misc_args) + assign_token + '\\end{math}' + assign_value + '\\\\')
        )

    def handle_variable_statement(variable_statement, misc_args, assign_to_var):
        # assign_to_var is False ONLY when we're doing shenanigans with read statements.
        variable = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 2)
        if is_array(variable):
            if variable_statement.iterative_assign == 'iterative_assign':
                iterative_condition_assign_list = [(build_meta_func(iterative_assign_conditional.condition), iterative_assign_conditional.assign) for iterative_assign_conditional in variable_statement.iterative_assign_conditionals]
                index_var_name = variable_statement.index_var_name
                return_string = ''
                all_values = []
                for index in range(variable_array_size_map[variable.name]):
                    loop_references[index_var_name] = index
                    need_default = True
                    for (condition_func, assign) in iterative_condition_assign_list:
                        if condition_func((constants, loop_references))[0]:
                            assign_string = handle_assign(assign, new_misc_args)
                            need_default = False
                            break
                    if need_default:
                        assign_string = handle_assign(variable_statement.assign, new_misc_args)
                    # return_string += (indent(misc_args['indent_level']) + format_variable_name_only(variable, misc_args) + '[' + str(index) + '] = ' + assign_string + os.linesep)
                    if len(all_values) % 11 == 8:
                        all_values.append('\\\\')
                    all_values.append(assign_string)
                loop_references.pop(index_var_name)
                assign_string = '[' + (', '.join(all_values)).replace('\\\\, ', '\\\\' + indent(1)) + ']'
                return_string = variable_assignment(variable, assign_string, misc_args, array_mode = 2)
                return return_string
            meta_results = []
            for loop_array_index in variable_statement.assigns:
                meta_results.extend(handle_loop_array_index((loop_array_index, variable_statement.constant_index), new_misc_args))
            assign_string = (
                '['
                + ', '.join(
                    [
                        ('(' + index + ', ' + results + ')')
                        for (indices, results) in meta_results
                        for index in indices
                    ]
                )
                + ']'
            )
            return (variable_assignment(variable, assign_string, misc_args, array_mode = 1) if assign_to_var else assign_string)
        return (variable_assignment(variable, handle_assign(variable_statement.assign, misc_args), misc_args, array_mode = 0) if assign_to_var else handle_assign(variable_statement.assign, misc_args))

    def handle_read_statement(read_statement, misc_args):
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 1)
        return (
            indent(misc_args['indent_level']) + 'if ' + 'self.environment.' + read_statement.name + '__condition(self):' + '$\\\\$'
            + (
                variable_assignment(read_statement.condition_variable,
                                    (
                                        '[(' +
                                        (
                                            resolve_potential_reference_no_type(execute_code(read_statement.index_of)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                                            if read_statement.constant_index == 'constant_index' else
                                            format_code(read_statement.index_of, new_misc_args)[0]
                                        )
                                        + ', True)]'
                                    )
                                    if is_array(read_statement.condition_variable) else
                                    'True',
                                    new_misc_args,
                                    array_mode = (1 if is_array(read_statement.condition_variable) else 0))
                if read_statement.condition_variable is not None else
                ''
            )
            + ''.join(
                [
                    (
                        variable_assignment(read_var_state.variable,
                                            ('self.environment.' + read_statement.name + '__' + str(index) + '(self)'),
                                            misc_args = new_misc_args,
                                            array_mode = (1 if is_array(read_var_state.variable) else 0))
                    )
                    for index, read_var_state in enumerate(read_statement.variable_statements)
                ]
            )
            + (
                (
                    indent(2) + 'else:' + '$\\\\$'
                    + variable_assignment(read_statement.condition_variable,
                                          (
                                              '[(' +
                                              (
                                                  resolve_potential_reference_no_type(execute_code(read_statement.index_of)[0], declared_enumerations, {}, variables, constants, loop_references)[1]
                                                  if read_statement.constant_index == 'constant_index' else
                                                  format_code(read_statement.index_of, new_misc_args)[0]
                                              )
                                              + ', False)]'
                                          )
                                          if is_array(read_statement.condition_variable) else
                                          'False',
                                          misc_args = new_misc_args,
                                          array_mode = (1 if is_array(read_statement.condition_variable) else 0))
                )
                if read_statement.condition_variable is not None else
                ''
            )
        )

    def handle_write_statement(write_statement, misc_args):
        return ''.join(
            [
                (indent(misc_args['indent_level']) + 'self.environment.' + write_statement.name + '__' + str(index) + '(self)' + '$\\\\$')
                if update_env.instant else
                (indent(misc_args['indent_level']) + 'self.environment.delay_this_action(' + 'self.environment.' + write_statement.name + '__' + str(index) + ', self)' + '$\\\\$')
                for index, update_env in enumerate(write_statement.update)
            ]
        )

    def format_returns(status_result):
        return '\\' + status_result.status.lower().capitalize() + 'Tikz{}'

    def handle_return_statement(statement, misc_args):
        variable_name = '\\NodeStatusTikz{}'
        if len(statement.case_results) == 0:
            return indent(misc_args['indent_level']) + '\\begin{math}' + variable_name + ' \\coloneqq{} ' + format_returns(statement.default_result) + '\\end{math}\\\\'
        return (
            (''.join(
                [
                    (indent(misc_args['indent_level']) + '\\texttt{elif }\\begin{math}' + format_code(case_result.condition, misc_args)[0] + '\\end{math}\\texttt{:}' + '\\\\'
                     + (indent(misc_args['indent_level'] + 1) + '\\begin{math}' + variable_name + ' \\coloneqq ' + format_returns(case_result) + '\\end{math}\\\\')
                     ) for case_result in statement.case_results
                ]
            )).replace('elif', 'if', 1)
            + indent(misc_args['indent_level']) + '\\texttt{else:}' + '\\\\'
            + indent(misc_args['indent_level'] + 1) + '\\begin{math}' + variable_name + ' \\coloneqq{} ' + format_returns(statement.default_result) + '\\end{math}\\\\'
        )

    def handle_statement(statement, misc_args):
        return (
            handle_variable_statement(statement.variable_statement, misc_args, assign_to_var = True)
            if statement.variable_statement is not None else
            (
                handle_read_statement(statement.read_statement, misc_args)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, misc_args)
            )
        )

    def update_method_action(node):
        misc_args = create_misc_args(False, 'node', 0)
        return (
            '\\node[Blackboard](..--REPLACE--..){\\begin{tabular}{l}'
            # + ''.join([('$' + handle_statement(statement, misc_args).replace('_', '\\_') + '$\\\\') for statement in node.pre_update_statements])
            # + ('$' + handle_return_statement(node.return_statement, misc_args).replace('_', '\\_') + '$\\\\')
            # + ''.join([('$' + handle_statement(statement, misc_args).replace('_', '\\_') + '$\\\\') for statement in node.post_update_statements])
            + '\\\\'.join(
                [(handle_statement(statement, misc_args)) for statement in node.pre_update_statements]
                + [handle_return_statement(node.return_statement, misc_args)]
                + [handle_statement(statement, misc_args) for statement in node.post_update_statements]
            )
            + '\\end{tabular}};'
        )

    def arg_method(node):
        return [
            ('\\texttt{' + arg_pair.argument_name + '}')
            for arg_pair in node.arguments
        ]

    def handle_initial_value(variable):
        initial_misc_args = create_misc_args(True, ('DEFINE' if variable.model_as == 'DEFINE' else ''), 0)
        if variable.model_as == 'NEURAL':
            return (
                '\\begin{math}'
                + format_variable(variable, initial_misc_args)
                + '\\end{math}'
                + '\\texttt{ -INPUTS- (}'
                + '\\begin{math}'
                + ', '.join(
                    (
                        ', '.join(
                            formatted_code
                            for formatted_code in format_code(input_code, create_misc_args(False, 'blackboard', 0))
                        )
                    )
                    for input_code in variable.inputs
                )
                + '\\end{math}'
                + '\\texttt{)}\\\\{}'
            )
        return handle_variable_statement(variable, initial_misc_args, True)

    def walk_tree_recursive(current_node, node_names):
        while hasattr(current_node, 'sub_root'):
            current_node = current_node.sub_root
        node_name = current_node.name if hasattr(current_node, 'name') and current_node.name is not None else current_node.leaf.name
        arguments = []
        if hasattr(current_node, 'leaf'):
            arguments = current_node.arguments
            current_node = current_node.leaf
        # next, we get the name of this node, and correct for duplication
        node_names.add(node_name)

        if current_node.node_type in ('check', 'environment_check', 'action'):
            arg_vals = []
            arg_names = node_arguments[current_node.name]
            for argument_code in arguments:
                for argument in execute_code(argument_code):
                    arg_vals.append(str_conversion(*resolve_potential_reference_no_type(argument, declared_enumerations, {}, variables, constants, loop_references)))
            if len(arg_vals) != len(arg_names):
                raise ValueError('Number of arguments mismatched in node: ' + node_name)
            arg_string = ('\\\\\\begin{math}\\{' + ', '.join([(arg_names[i] + '\\coloneqq{}' + arg_vals[i]) for i in range(len(arg_vals))]) + '\\}\\end{math}') if len(arguments) > 0 else ''
            node_ids.append('(' + node_name.replace('_', '') + 'UPDATEBLACKBOARD)')
            if current_node.node_type == 'action':
                return '[.\\node[Action](' + node_name.replace('_', '') + '){\\begin{tabular}{c}$' + node_name + '$' + arg_string + '\\end{tabular}};' + tikz_nodes[current_node.name].replace('(..--REPLACE--..)', '(' + node_name.replace('_', '') + 'UPDATEBLACKBOARD)') + ']' + os.linesep
                # return '[.\\node[Action](' + node_name.replace('_', '') + '){$' + node_name.replace('_', '\\_') + '$};' + ']' + os.linesep
            return '[.\\node[Check](' + node_name.replace('_', '') + '){\\begin{tabular}{c}$' + node_name + '$' + arg_string + '\\end{tabular}};' + tikz_nodes[current_node.name].replace('(..--REPLACE--..)', '(' + node_name.replace('_', '') + 'UPDATEBLACKBOARD)') + ']' + os.linesep
            # return '[.\\node[Check](' + node_name.replace('_', '') + '){$' + node_name.replace('_', '\\_') + '$};' + ']' + os.linesep
        if current_node.node_type in ('X_is_Y', 'inverter', 'repeat', 'one_shot'):
            return (
                '[.\\node[Decorator](' + node_name.replace('_', '') + '){$' + node_name
                + '$\\{'
                + (
                    ('\\begin{math}\\' + current_node.x.capitalize() + 'Tikz{}\\mapsto{}\\' + current_node.y.capitalize() + 'Tikz{}\\end{math}')
                    if current_node.x is not None else
                    (
                        ('x' + str(current_node.repeat))
                        if current_node.repeat is not None else
                        (
                            (
                                ('\\begin{math}\\Success{}\\end{math}')
                                if current_node.one_shot == 'success_only' else
                                (
                                    ('$\\FailureTikz{}$')
                                    if current_node.one_shot == 'failure_only' else
                                    ('$\\SuccessTikz{}\\lor{}\\FailureTikz{}$')
                                )
                            )
                            if current_node.one_shot is not None else
                            ('$\\SuccessTikz{}\\SwapArrow{}\\FailureTikz{}$')
                        )
                    )
                )
                + '\\}};' + os.linesep
                + walk_tree_recursive(current_node.child, node_names)
                + ']' + os.linesep
            )
        return (
            '[.\\node[' + current_node.node_type.capitalize() + '](' + node_name.replace('_', '') + '){$' + node_name + '$' + ('\\textcircled{M}' if current_node.memory != '' else '') + ('' if current_node.parallel_policy is None else ('\\{All\\}' if current_node.parallel_policy == 'success_on_all' else '\\{One\\}')) + '};' + os.linesep
            + ''.join([
                walk_tree_recursive(child, node_names)
                for child in current_node.children
            ])
            + ']' + os.linesep
        )

    def get_root_id(node):
        while hasattr(node, 'sub_root'):
            node = node.sub_root
        node_name = node.name if hasattr(node, 'name') and node.name is not None else node.leaf.name
        return (node_name).replace('_', '')

    def handle_domain_codes(domain_codes):
        return (
            '\\texttt{\\{}'
            + ', '.join(
                (
                    ', '.join(
                        [
                            str_conversion(*resolve_potential_reference_no_type(domain_value, declared_enumerations, {}, variables, constants, loop_references))
                            for domain_value in execute_code(domain_code)
                        ]
                    )
                )
                for domain_code in domain_codes
            )
            + '\\texttt{\\}}'
        )

    def handle_min_max(min_val_code, max_val_code):
        (min_val, max_val) = get_min_max(min_val_code, max_val_code, declared_enumerations, {}, variables, constants, loop_references)
        return ('[' + str(min_val) + ', ' + str(max_val) + ']')

    function_format = {
        'if' : ('', format_function_if),
        'loop' : ('', format_function_loop),
        'abs' : ('abs', format_function_one_arg),
        'max' : ('max', format_function_before),
        'min' : ('min', format_function_before),
        'sin' : ('sin', format_function_before),
        'cos' : ('cos', format_function_before),
        'tan' : ('tan', format_function_before),
        'ln' : ('log', format_function_before),
        'not' : ('\\neg ', format_function_before),  # space intentionally added here.
        'and' : ('\\land', format_function_between),
        'or' : ('\\lor', format_function_between),
        'xor' : ('\\oplus', format_function_between),
        'xnor' : ('\\odot', format_function_between),
        'implies' : ('\\implies', format_function_between),
        'equivalent' : ('\\Biconditional', format_function_between),
        'eq' : ('=', format_function_between),
        'neq' : ('\\neq', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('\\leq', format_function_between),
        'gte' : ('\\geq', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('\\cdot', format_function_between),
        # 'division' : ('//', format_function_between),  # this rounds to negative infinity, we want rounds to 0.
        'idiv' : ('//', format_function_between),
        'mod' : ('mod', format_function_between),
        'rdiv' : ('/', format_function_between),
        'floor' : ('\\floor', format_function_one_arg),
        'count' : ('count', format_function_before),
        'index' : ('index', format_function_index)
    }

    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit, True)
    variable_array_size_map = {
        variable.name : variable_array_size(variable, declared_enumerations, {}, variables, constants, {})
        for variable in model.variables if is_array(variable)# or (variable.model_as == 'NEURAL')
    }
    loop_references = {}
    initial_variable_values = {
        variable.name : handle_initial_value(variable)
        for variable in model.variables #if (variable.model_as != 'NEURAL' and variable.model_as != 'DEFINE')
    }
    environment_updates = [
        handle_variable_statement(environment_update, create_misc_args(False, 'environment', 0), True)
        for environment_update in model.update
    ]
    variable_infos = [
        (
            format_variable(variable, create_misc_args(False, 'blackboard', 0))
            + ((' - \\texttt{array ' + str(variable_array_size_map[variable.name]) + '}') if variable.name in variable_array_size_map else '')
            + ' - \\texttt{' + variable.model_as + '}'
            + ' - ' + (
                ('\\texttt{' + variable.domain + '}')
                if variable.model_as == 'DEFINE' else
                (
                    (
                        handle_domain_codes(variable.domain_codes)
                        if variable.neural_mode == 'classification' else
                        ('\\texttt{' + variable.domain + '}')
                    )
                    if variable.model_as == 'NEURAL' else
                    (
                        ('\\texttt{BOOLEAN}')
                        if variable.domain.boolean is not None else
                        (
                            ('\\texttt{INT}')
                            if variable.domain.true_int is not None else
                            (
                                ('\\texttt{REAL}')
                                if variable.domain.true_real is not None else
                                (
                                    handle_min_max(variable.domain.min_val, variable.domain.max_val)
                                    if variable.domain.min_val is not None else
                                    handle_domain_codes(variable.domain.domain_codes)
                                )
                            )
                        )
                    )
                )
            )
        )
        for variable in model.variables
    ]

    tikz_nodes = {}
    node_arguments = {}
    for action in model.action_nodes:
        tikz_nodes[action.name] = update_method_action(action)
        node_arguments[action.name] = arg_method(action)
    for check in model.check_nodes:
        tikz_nodes[check.name] = update_method_check(check)
        node_arguments[check.name] = arg_method(check)
    for environment_check in model.environment_checks:
        tikz_nodes[environment_check.name] = update_method_environment_check(environment_check)
        node_arguments[environment_check.name] = arg_method(environment_check)
    root_id = get_root_id(model.root)
    # for var in initial_variable_values:
    #     print('-----')
    #     print(var)
    #     print(initial_variable_values[var])
    node_ids = []
    tikz_picture = (
        '\\begin{tikzpicture}' + os.linesep
        + '\\tikzset{level distance=20pt}' + os.linesep
        + '\\tikzset{sibling distance=0.5pt}' + os.linesep
        + '\\Tree'
        +  walk_tree_recursive(model.root, set()).replace('$$\\\\', '').replace('\\\\\\end{tabular}', '\\end{tabular}')
        + (
            ('\\node[draw=none,inner sep=0pt, fit=' + ''.join(node_ids) + '] (sereneblackboardfitbox) {};' + os.linesep)
            if on_sides else
            ''
        )
        # +  walk_tree_recursive(model.root, set(), {}, tikz_nodes)
        + (
            ('\\node[Blackboard, anchor=south east] (initialValues) at ([xshift=-5pt]sereneblackboardfitbox.south west){\\begin{tabular}{l}')
            if on_sides else
            ('\\node[Blackboard, anchor=south east] (initialValues) at ([xshift=-5pt, yshift=5pt]' + root_id + '.north west){\\begin{tabular}{l}')
        )
        + '\\texttt{-INITIAL VALUES-}\\\\{}'
        + ''.join(
            initial_variable_values[variable.name]
            for variable in model.variables # if (variable.model_as != 'NEURAL')
        )
        + '\\end{tabular}};' + os.linesep
        + '\\node[Blackboard, anchor=south east] (varInfo) at ([xshift=-5pt]initialValues.south west){\\begin{tabular}{l}'
        + '\\texttt{-VARIABLE INFO-}\\\\{}'
        + '\\\\{}'.join(
            # list(('\\begin{math}\\texttt{' + constant_decl.name+ '} \\coloneqq{} ' + str(constant_decl.val)+ '\\end{math}') for constant_decl in model.constants)
            # +
            list(var_info for var_info in variable_infos)
        )
        + '\\end{tabular}};' + os.linesep
        + (
            ('\\node[Blackboard, anchor=south west] (environmentUpdates) at ([xshift=5pt]sereneblackboardfitbox.south east){\\begin{tabular}{l}')
            if on_sides else
            ('\\node[Blackboard, anchor=south west] (environmentUpdates) at ([xshift=5pt, yshift=5pt]' + root_id + '.north east){\\begin{tabular}{l}')
        )
        + '\\texttt{-ENVIRONMENT UPDATES-}\\\\{}'
        + ''.join(
            environment_update
            for environment_update in environment_updates
        )
        + '\\end{tabular}};' + os.linesep
        + '\\end{tikzpicture}' + os.linesep
    )
    tikz_picture = tikz_picture.replace('_', '\\_')
    while '\\\\\\\\' in tikz_picture:
        tikz_picture = tikz_picture.replace('\\\\\\\\', '\\\\')
    with open(output_file, 'w', encoding = 'utf-8') as output_file_:
        if insert_only:
            output_file_.write(tikz_picture)
        else:
            start = ''
            end = ''
            with open(os.path.dirname(os.path.realpath(__file__)) + '/tikz_files/start.tex', 'r', encoding = 'utf-8') as start_file:
                start = start_file.read()
            with open(os.path.dirname(os.path.realpath(__file__)) + '/tikz_files/end.tex', 'r', encoding = 'utf-8') as end_file:
                end = end_file.read()
            output_file_.write(start + os.linesep + tikz_picture + end)
    return


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('--insert_only', action = 'store_true')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    arg_parser.add_argument('--on_sides', action = 'store_true')
    args = arg_parser.parse_args()
    write_files(args.metamodel_file, args.model_file, args.output_file, args.insert_only, args.recursion_limit, args.on_sides)
