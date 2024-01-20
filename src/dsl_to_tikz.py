'''
This module is for internal use with BehaVerify.
It is used to convert .tree files to tikz.
It contains a variety of utility functions.


Author: Serena Serafina Serbinowska
Last Edit: 2024-01-19
'''
import argparse
import os
from behaverify_common import indent, create_node_name, is_local, is_env, is_array, handle_constant_or_reference, resolve_potential_reference_no_type, variable_array_size, get_min_max, BTreeException, constant_type
from serene_functions import build_meta_func
from check_grammar import validate_model


def write_files(metamodel_file, model_file, output_file, recursion_limit):
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
    # loc is a location. location can be node, blackboard, or environment.
    def create_misc_args(init, loc, indent_level):
        return {'init' : init, 'loc' : loc, 'indent_level' : indent_level}

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
        return [
            (formatted_variable + '(' + formatted_index + ')')
            if variable.model_as in ('DEFINE', 'NEURAL') else
            (formatted_variable + '[serene_safe_assignment.index_func(' + formatted_index + ', ' + str(variable_array_size_map[variable.name]) + ')]')
        ]

    def format_function(code, misc_args):
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def format_variable_name_only(variable, misc_args):
        return (
            (
                ('node.' if is_local(variable) else ('self.' if is_env(variable) else 'self.blackboard.'))
                + variable.name
            )
            if misc_args['loc'] == 'environment'
            else
            (
                (
                    ('blackboard_reader.')
                    if misc_args['loc'] == 'blackboard' else
                    ('self.' + ('' if is_local(variable) else 'blackboard.'))
                )
                + variable.name
            )
        )

    def format_variable(variable, misc_args):
        return format_variable_name_only(variable, misc_args) + ('()' if variable.model_as == 'DEFINE' else '')

    def handle_atom(code, misc_args):
        try:
            (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, {}, variables, constants, loop_references)
        except BTreeException as bt_e:  # this should be an argument.
            if misc_args['loc'] == 'node':
                return 'self.' + code.atom.reference
            if misc_args['loc'] == 'environment':
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

    def update_method_check(node):
        return (
            '\\node[Blackboard]{\begin{tabular}{l}' + os.linesep
            + ('$' + format_code(node.condition, create_misc_args(False, 'node', 2))[0].replace('_', '\\_') + '$\\\\' + os.linesep)
            + '\\end{tabular}};'
        )

    def update_method_environment_check(node):
        return (
            '\\node[Blackboard]{\begin{tabular}{l}' + os.linesep
            + ('$' + format_code(node.condition, create_misc_args(False, 'node', 2))[0].replace('_', '\\_') + '$\\\\' + os.linesep)
            + '\\end{tabular}};'
        )

    def resolve_variable_nondeterminism(values, misc_args):
        formatted_values = []
        for value in values:
            formatted_values.extend(format_code(value, misc_args))
        return '\\{' + ', '.join(formatted_values) + '\\}'

    def handle_assign(assign, misc_args):
        case_results = assign.case_results
        default_result = assign.default_result
        if len(case_results) == 0:
            return resolve_variable_nondeterminism(default_result.values, misc_args)  # NOTE: no linesep at the end!
        return (
            '(' + os.linesep
            + ''.join(
                [
                    (
                        indent(misc_args['indent_level'] + 1 + index)
                        + resolve_variable_nondeterminism(case_result.values, misc_args) + os.linesep
                        + indent(misc_args['indent_level'] + 1 + index) + 'if ' + format_code(case_result.condition, misc_args)[0] + ' else' + os.linesep
                        + indent(misc_args['indent_level'] + 1 + index) + '(' + os.linesep
                     ) for index, case_result in enumerate(case_results)
                ]
            )
            + indent(misc_args['indent_level'] + len(case_results))
            + resolve_variable_nondeterminism(default_result.values, misc_args) + os.linesep
            + indent(misc_args['indent_level']) + (')' * (1 + len(case_results)))  # NOTE: no linesep at the end!
        )

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
        # i don't think we should be able to have define variables here.
        safety_1 = '' if variable.model_as == 'DEFINE' else ('serene_safe_assignment.' + variable.name + '(')
        safety_2 = '' if variable.model_as == 'DEFINE' else ')'
        return (
            (
                indent(misc_args['indent_level']) + '__temp_var__ = ' + safety_1 + assign_value + safety_2 + os.linesep
                + indent(misc_args['indent_level']) + 'for (index, val) in __temp_var__:' + os.linesep
                + indent(misc_args['indent_level'] + 1) + format_variable_name_only(variable, misc_args) + '[index] = val' + os.linesep
            )
            if array_mode else
            (indent(misc_args['indent_level']) + format_variable_name_only(variable, misc_args) + ' = ' + safety_1 + assign_value + safety_2 + os.linesep)
        )

    def handle_variable_statement(variable_statement, misc_args, assign_to_var):
        # assign_to_var is False ONLY when we're doing shenanigans with read statements.
        variable = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 2)
        if is_array(variable):
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
            return (variable_assignment(variable, assign_string, misc_args, array_mode = True) if assign_to_var else assign_string)
        return (variable_assignment(variable, handle_assign(variable_statement.assign, misc_args), misc_args, array_mode = False) if assign_to_var else handle_assign(variable_statement.assign, misc_args))

    def handle_read_statement(read_statement, misc_args):
        new_misc_args = create_misc_args(misc_args['init'], misc_args['loc'], misc_args['indent_level'] + 1)
        return (
            indent(misc_args['indent_level']) + 'if ' + 'self.environment.' + read_statement.name + '__condition(self):' + os.linesep
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
                                    array_mode = is_array(read_statement.condition_variable))
                if read_statement.condition_variable is not None else
                ''
            )
            + ''.join(
                [
                    (
                        variable_assignment(read_var_state.variable,
                                            ('self.environment.' + read_statement.name + '__' + str(index) + '(self)'),
                                            misc_args = new_misc_args,
                                            array_mode = is_array(read_var_state.variable))
                    )
                    for index, read_var_state in enumerate(read_statement.variable_statements)
                ]
            )
            + (
                (
                    indent(2) + 'else:' + os.linesep
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
                                          array_mode = is_array(read_statement.condition_variable))
                )
                if read_statement.condition_variable is not None else
                ''
            )
        )

    def handle_write_statement(write_statement, misc_args):
        return ''.join(
            [
                (indent(misc_args['indent_level']) + 'self.environment.' + write_statement.name + '__' + str(index) + '(self)' + os.linesep)
                if update_env.instant else
                (indent(misc_args['indent_level']) + 'self.environment.delay_this_action(' + 'self.environment.' + write_statement.name + '__' + str(index) + ', self)' + os.linesep)
                for index, update_env in enumerate(write_statement.update)
            ]
        )

    def format_returns(status_result):
        return '\\' + status_result.status.to_lower().capitalize()

    def handle_return_statement(statement, misc_args):
        variable_name = 'return_status'
        if len(statement.case_results) == 0:
            return indent(misc_args['indent_level']) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep
        return (
            (''.join(
                [
                    (indent(misc_args['indent_level']) + 'elif ' + format_code(case_result.condition, misc_args)[0] + ':' + os.linesep
                     + (indent(misc_args['indent_level'] + 1) + variable_name + ' = ' + format_returns(case_result) + os.linesep)
                     ) for case_result in statement.case_results
                ]
            )).replace('elif', 'if', 1)
            + indent(misc_args['indent_level']) + 'else:' + os.linesep
            + indent(misc_args['indent_level'] + 1) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep
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
        misc_args = create_misc_args(False, 'node', 2)
        return (
            '\\node[Blackboard]{\begin{tabular}{l}' + os.linesep
            + ''.join([('$' + handle_statement(statement, misc_args).replace('_', '\\_') + '$\\\\' + os.linesep) for statement in node.pre_update_statements])
            + ('$' + handle_return_statement(node.return_statement, misc_args).replace('_', '\\_') + '$\\\\' + os.linesep)
            + ''.join([('$' + handle_statement(statement, misc_args).replace('_', '\\_') + '$\\\\' + os.linesep) for statement in node.post_update_statements])
            + '\\end{tabular}};'
        )

    def walk_tree_recursive(current_node, node_names, node_names_map, tikz_nodes):
        while True:
            if hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
                continue
            current_name = current_node.leaf.name if current_node.name is None else current_node.name
            if hasattr(current_node, 'leaf'):
                current_node = current_node.leaf
            break
        # next, we get the name of this node, and correct for duplication
        new_name = create_node_name(current_name, node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        node_names.add(node_name)
        node_names_map[node_name] = modifier

        if current_node.node_type in ('check', 'environment_check', 'action'):
            if current_node.node_type == 'action':
                # return '[.\\node[Action](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + tikz_nodes[current_name] + ']' + os.linesep
                return '[.\\node[Action](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + ']' + os.linesep
            # return '[.\\node[Check](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + tikz_nodes[current_name] + ']' + os.linesep
            return '[.\\node[Check](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + ']' + os.linesep
        if current_node.node_type in ('X_is_Y', 'inverter'):
            return (
                '[.\\node[Decorator](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + os.linesep
                + walk_tree_recursive(current_node.child, node_names, node_names_map, tikz_nodes)
                + ']' + os.linesep
            )
        return (
            '[.\\node[' + current_node.node_type.capitalize() + '](' + node_name.replace('_', '') + '){$' + current_name.replace('_', '\\_') + '$};' + os.linesep
            + ''.join([
                walk_tree_recursive(child, node_names, node_names_map, tikz_nodes)
                for child in current_node.children
            ])
            + ']' + os.linesep
        )

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
        'neq' : ('\neq', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('\\lte', format_function_between),
        'gte' : ('\\gte', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('\\Multiply', format_function_between),
        # 'division' : ('//', format_function_between),  # this rounds to negative infinity, we want rounds to 0.
        'idiv' : ('//', format_function_between),
        'mod' : ('mod', format_function_between),
        'rdiv' : ('/', format_function_between),
        'floor' : ('\\floor', format_function_one_arg),
        'count' : ('count', format_function_before),
        'index' : ('index', format_function_index)
    }

    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit)
    variable_array_size_map = {
        variable.name : variable_array_size(variable, declared_enumerations, {}, variables, constants, {})
        for variable in model.variables if is_array(variable) or (variable.model_as == 'NEURAL')
    }
    loop_references = {}

    # tikz_nodes = {}
    # for action in model.action_nodes:
    #     tikz_nodes[action.name] = update_method_action(action)
    # for check in model.check_nodes:
    #     tikz_nodes[check.name] = update_method_check(check)
    # for environment_check in model.environment_checks:
    #     tikz_nodes[environment_check.name] = update_method_environment_check(environment_check)

    with open(output_file, 'w', encoding = 'utf-8') as output_file_:
        output_file_.write(
            '\\begin{tikzpicture}' + os.linesep
            + '\\tikzset{level distance=22pt}' + os.linesep
            + '\\tikzset{sibling distance=0.5pt}' + os.linesep
            + '\\Tree'
            +  walk_tree_recursive(model.root, set(), {}, {})
            # +  walk_tree_recursive(model.root, set(), {}, tikz_nodes)
            + '\\end{tikzpicture}' + os.linesep
        )
    return


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    args = arg_parser.parse_args()
    write_files(args.metamodel_file, args.model_file, args.output_file, args.recursion_limit)
