'''
This module is part of BehaVerify and used to convert .tree files to .smv files for use with nuXmv. It indexes arrays manually.


Author: Serena Serafina Serbinowska
Last Edit: 2024-02-12
'''
import argparse
import pprint
import os
import copy
from behaverify_to_smv import write_smv
from serene_functions import build_meta_func
from check_grammar import validate_model

from behaverify_common import create_node_name, create_node_template, create_variable_template, indent, is_local, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max, BTreeException, variable_type

# a NEXT_VALUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE

def dsl_to_nuxmv(metamodel_file, model_file, output_file, recursion_limit):
    '''
    This method is used to convert the dsl to behaverify.
    '''
    def copy_loop_references(loop_references):
        return {
            key : loop_references[key]
            for key in loop_references
        }
    def copy_misc_args(misc_args):
        return create_misc_args(misc_args['define_call'], copy_loop_references(misc_args['loop_references']), misc_args['node_name'], misc_args['specification_mode'], misc_args['inactive_condition'])

    def execute_loop(function_call, to_call, packaged_args, misc_args):
        # to_call is expected to return a list (or something) of items to be added. (E.G., format_code)
        new_misc_args = copy_misc_args(misc_args)
        loop_references = new_misc_args['loop_references']
        return_vals = []
        all_domain_values = []
        if function_call.min_val is None:
            for domain_code in function_call.loop_variable_domain:
                domain_func = build_meta_func(domain_code)
                for domain_value in domain_func((constants, loop_references)):
                    resolved = resolve_potential_reference_no_type(domain_value, declared_enumerations, nodes, variables, constants, loop_references)
                    all_domain_values.append(resolved[1])
        else:
            (min_val, max_val) = get_min_max(function_call.min_val, function_call.max_val, declared_enumerations, nodes, variables, constants, loop_references)
            all_domain_values = range(min_val, max_val + 1)
        cond_func = build_meta_func(function_call.loop_condition)
        for domain_member in all_domain_values:
            loop_references[function_call.loop_variable] = domain_member
            if cond_func((constants, loop_references))[0]:
                return_vals.extend(to_call(packaged_args, new_misc_args))
            loop_references.pop(function_call.loop_variable)
        return return_vals

    def format_function_if(_, function_call, misc_args):
        return ['(ifThenElse ' + format_code(function_call.values[0], misc_args)[0] + ' ' + format_code(function_call.values[1], misc_args)[0] + ' ' + format_code(function_call.values[2], misc_args)[0] + ')']

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, function_call.values[0], misc_args)

    def format_function_ctl(function_name, function_call, misc_args):
        '''this is used to format the majority of functions'''
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) <= 0:
            raise BTreeException([], 'no arguments for function')
        return ['(' + function_name + ' ' + ' '.join([('(\\state -> ' + formatted_value + ')') for formatted_value in formatted_values])]

    def format_function_default_recursion(function_name, formatted_values, index):
        return (
            ('(' + function_name + ' ' + formatted_values[index] + ')')
            if len(formatted_values) - index == 0 else
            (
                ('(' + function_name + ' ' + formatted_values[index] + ' ' + formatted_values[index + 1] + ')')
                if len(formatted_values) - index == 1 else
                ('(' + function_name + ' ' + formatted_values[index] + ' ' + format_function_default_recursion(function_name, formatted_values, index + 1) + ')')
            )
        )

    def format_function_default(function_name, function_call, misc_args):
        '''this is used to format the majority of functions'''
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        if len(formatted_values) <= 0:
            raise BTreeException([], 'no arguments for function')
        return [format_function_default_recursion(function_name, formatted_values, 0)]

    def format_function(code, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.
        returns ::> (formated string, list of return types of each 
        '''
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def create_misc_args(define_call, loop_references, node_name, specification_mode, inactive_condition):
        '''
        -- ARGUMENTS
        @ node_name := the name of the node which caused this to be called. used for formatting local variables.
        @ use_stages := are we using stages for this? (note: does not affect variable renaming).
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        return {
            'define_call' : define_call,
            'loop_references' : loop_references,
            'node_name' : node_name,
            'specification_mode' : specification_mode,
            'inactive_condition' : inactive_condition
        }

    def format_variable_name_only(variable, misc_args):
        return (
            (((misc_args['node_name'] + '___') if is_local(variable) else '') + variable.name + '___DEF')
            if variable.model_as == 'DEFINE' else
            (
                (((misc_args['node_name'] + '___') if is_local(variable) else '') + variable.name + '___')
                if misc_args['specification_mode'] else
                (((misc_args['node_name'] + '___') if is_local(variable) else '') + variable.name + '___VAL')
            )
        )

    def format_variable(variable, misc_args):
        '''
        -- GLOBALS
        @ variables := a dict of all variables
        -- ARGUMENTS
        @ variable_obj := a textx object of a variable that we will be formatting.
        @ node_name := the name of the node which caused this to be called.
        @ use_stages := are we using stages for this?
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        return (
            misc_args['define_call'][format_variable_name_only(variable, misc_args)]
            if variable.model_as == 'DEFINE' else
            (
                ('(' + format_variable_name_only(variable, misc_args) + ' state)')
                if misc_args['specification_mode'] else
                format_variable_name_only(variable, misc_args)
            )
        )

    def adjust_args(code, misc_args):
        '''
        creates a new arg based on the old one, but modifies it (if necessary). should only be used by format_code
        Declared not as nested function cuz that would tank performance.
        '''
        if code.node_name is not None:
            new_misc_args = copy_misc_args(misc_args)
            node_name_func = build_meta_func(code.node_name)
            new_misc_args['node_name'] = resolve_potential_reference_no_type(node_name_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
            return new_misc_args
        return misc_args

    def handle_atom(code, misc_args):
        (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        return (str(atom).capitalize() if atom_type == 'BOOLEAN' else str(atom)) if atom_class == 'CONSTANT' else (format_variable(atom, adjust_args(code, misc_args)))

    def format_code(code, misc_args):
        return (
            [handle_atom(code, misc_args)] if code.atom is not None else (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)] if code.code_statement is not None else (
                    format_function(code, misc_args)
                )
            )
        )

    def handle_case_result(case_result, case_number, misc_args):
        guard_string = 'guard_' + str(case_number) + ' = ' + (
            format_code(case_result.condition, misc_args)
            if hasattr(case_result, 'condition') else
            'True'
        ) + os.linesep
        vals = []
        for value in case_result.values:
            vals.extend(format_code(value, misc_args))
        value_string = ''.join([
            ('value_' + str(case_number) + '_' + str(value_number) + ' = ' + value + os.linesep)
            for (value_number, value) in enumerate(vals)
        ])
        return (
            guard_string + value_string,
            indent(1) + '| guard_' + str(case_number) + ' = ' + (
                ('Set.singleton value_' + str(case_number) + '_0')
                if len(vals) > 1 else
                ('Set.fromList [' + ', '.join(map(lambda x: 'value_' + str(case_number) + '_' + str(x), range(len(vals)))) + ']')
            ) + os.linesep
        )

    def handle_case_result_define(case_result, misc_args):
        vals = []
        for value in case_result.values:
            vals.extend(format_code(value, misc_args))
        # define must be deterministic, so there should only be one value actually.
        return ((format_code(case_result.condition, misc_args) if hasattr(case_result, 'condition') else 'True'), vals[0])

    def handle_assign_value(variable, assign_value, misc_args):
        case_result_strings = [handle_case_result(case_result, case_number, misc_args) for (case_number, case_result) in enumerate(assign_value.case_results)] + [handle_case_result(assign_value.default_result, len(assign_value.case_results), misc_args)]
        return (
            '-- for ' + format_variable_name_only(variable, misc_args) + os.linesep
            + ''.join(map(lambda x: x[0], case_result_strings))
            + 'values' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_variable_name_only(variable, misc_args) + os.linesep
            + ''.join(map(lambda x: x[1], case_result_strings))
            + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: ' + variable_type(variable, declared_enumerations, constants) + ' -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + format_variable_name_only(variable, misc_args) + ' = result' + os.linesep
            + indent(3) + 'where' + os.linesep
        )

    def handle_assign_value_define(assign_value, misc_args):
        case_result_strings = [handle_case_result_define(case_result, misc_args) for case_result in assign_value.case_results] + [handle_case_result_define(assign_value.default_result, misc_args)]
        return ''.join(map(lambda x : (indent(1) + '| ' + x[0] + ' = ' + x[1] + os.linesep), case_result_strings))

    def handle_variable_statement_define(variable, statement, known_dependencies, misc_args):
        '''
        1 ::> the function;
        2 ::> value of depends on;
        3 ::> the function call in specification mode;
        4 ::> the function call in iteration mode;
        '''
        depends_on = sorted(list(set(find_used_variables_without_formatting_in_statement(statement, is_array(variable), None, known_dependencies))))
        variable_name = format_variable_name_only(variable, misc_args)
        new_misc_args = copy_misc_args(misc_args)
        if is_array(variable):
            raise ValueError
        return (
            variable_name + ' :: ' + ' -> '.join(map(lambda x : x[2], depends_on)) + (' -> ' if len(depends_on) > 0 else '') + variable_type(variable, declared_enumerations, constants) + os.linesep
            + variable_name + ' ' + ' '.join(map(lambda x : x[0], depends_on)) + os.linesep
            + handle_assign_value_define(statement.assign, new_misc_args),
            depends_on,
            '(' + variable_name + ' ' + ' '.join(map(lambda x: x[1], depends_on)) + ')',
            '(' + variable_name + ' ' + ' '.join(map(lambda x: x[0], depends_on)) + ')'
        )

    def handle_variable_statement(variable_statement, misc_args):
        '''should only be called if init_mode is true or from variable_assignment'''
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        # if is_array(assign_var):
        #     return (
        #         handle_array_constant_index(variable_statement, condition, misc_args)
        #         if variable_statement.constant_index == 'constant_index' else
        #         handle_array_unknown_index(variable_statement, condition, misc_args)
        #     )
        if is_array(assign_var):
            raise ValueError
        return ([(handle_assign_value(assign_var, variable_statement.assign, misc_args), 4)], [])

    def handle_write_statement(write_statement, misc_args):
        new_misc_args = copy_misc_args(misc_args)
        delayed_misc_args = copy_misc_args(misc_args)
        delayed_misc_args['indent_level'] = 0
        results = []
        delayed_results = []
        for variable_statement in write_statement.update:
            if variable_statement.instant:
                results.extend(handle_variable_statement(variable_statement, new_misc_args)[0])
            else:
                delayed_results.extend(handle_variable_statement(variable_statement, new_misc_args)[0])
        return (results, delayed_results)

    def handle_read_statement(read_statement, misc_args):
        misc_args = copy_misc_args(misc_args)
        results = [(
            '-- for READ STATEMENT: ' + str(read_statement.name) + os.linesep
            + 'values' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = Set.singleton False' + os.linesep
            + indent(1) + '| ' + format_code(read_statement.condition, misc_args) + ' = ' + ('Set.fromList [True, False]' if read_statement.non_determinism else 'Set.singleton True') + os.linesep
            + indent(1) + '| otherwise = Set.singleton False' + os.linesep
            + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: Bool -> Set.Set State' + os.linesep
            + indent(2) + 'next_func read_condition = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4)]
        if read_statement.condition_variable is not None:
            if is_array(read_statement.condition_variable):
                raise ValueError
            results.append((
                'values' + os.linesep
                + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_variable_name_only(read_statement.condition_variable, misc_args) + os.linesep
                + indent(1) + '| read_condition = ' + (('Set.fromList [True, False]') if read_statement.non_determinism == 'non_determinism' else 'Set.singleton True') + os.linesep
                + indent(1) + '| otherwise = Set.singleton False' + os.linesep
                + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
                + indent(1) + 'where' + os.linesep
                + indent(2) + 'next_func :: Bool -> Set.Set State' + os.linesep
                + indent(2) + 'next_func ' + format_variable_name_only(read_statement.condition_variable, misc_args) + ' = result' + os.linesep
                + indent(3) + 'where' + os.linesep
                , 4))
        misc_args['inactive_condition'] = '(||) ' + misc_args['inactive_condition'] + '(not read_condition)'
        for variable_statement in read_statement.variable_statements:
            results.extend(handle_variable_statement(variable_statement, misc_args)[0])
        return (results, [])

    def handle_statement(statement, misc_args):
        '''
        1 ::> result
        2 ::> delayed_results
        3 ::> new_indent_level
        '''
        return (
            handle_variable_statement(statement.variable_statement, misc_args)
            if statement.variable_statement is not None else
            (
                handle_read_statement(statement.read_statement, misc_args)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, misc_args)
            )
        )

    def find_used_variables_without_formatting_in_code(code, known_dependencies, misc_args):
        if code.atom is not None:
            (atom_class, atom) = handle_constant_or_reference_no_type(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
            return (
                (
                    known_dependencies[format_variable_name_only(atom, misc_args)]
                    if atom.model_as == 'DEFINE' else
                    [(
                        format_variable_name_only(atom, create_misc_args(define_call = {}, loop_references = {}, node_name = misc_args['node_name'], specification_mode = False, inactive_condition = '')),
                        format_variable_name_only(atom, create_misc_args(define_call = {}, loop_references = {}, node_name = misc_args['node_name'], specification_mode = True, inactive_condition = '')),
                        variable_type(atom, declared_enumerations, constants)
                    )]
                )
                if atom_class == 'VARIABLE' else []
            )
        if code.code_statement is not None:
            return find_used_variables_without_formatting_in_code(code.code_statement, known_dependencies, misc_args)
        function_call = code.function_call
        if function_call.function_name == 'loop':
            return execute_loop(function_call, find_used_variables_without_formatting_in_code, function_call.values[0], misc_args)
        used_variables = []
        for value in function_call.values:
            used_variables.extend(find_used_variables_without_formatting_in_code(value, known_dependencies, misc_args))
        if function_call.function_name != 'index':
            return used_variables
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
        new_misc_args = adjust_args(function_call, misc_args)
        used_variables.append((
            format_variable_name_only(variable, create_misc_args(define_call = None, loop_references = None, node_name = new_misc_args['node_name'], specification_mode = False, inactive_condition = '')),
            format_variable_name_only(variable, create_misc_args(define_call = None, loop_references = None, node_name = new_misc_args['node_name'], specification_mode = True, inactive_condition = '')),
            variable_type(atom, declared_enumerations, constants)
        ))
        return used_variables

    def find_used_variables_without_formatting_in_assign(assign, known_dependencies, misc_args):
        used_variables = []
        for case_result in assign.case_results:
            used_variables.extend(find_used_variables_without_formatting_in_code(case_result.condition, known_dependencies, misc_args))
            for value in case_result.values:
                used_variables.extend(find_used_variables_without_formatting_in_code(value, known_dependencies, misc_args))
        for value in assign.default_result.values:
            used_variables.extend(find_used_variables_without_formatting_in_code(value, known_dependencies, misc_args))
        return used_variables

    def find_used_variables_without_formatting_in_loop_array_index(packaged_args, misc_args):
        (loop_array_index, is_constant, known_dependencies) = packaged_args
        if loop_array_index.array_index is not None:
            used_variables = find_used_variables_without_formatting_in_assign(loop_array_index.array_index.assign, known_dependencies, misc_args)
            if not is_constant:
                for index in loop_array_index.array_index.index_expr:
                    used_variables.extend(find_used_variables_without_formatting_in_code(index, known_dependencies, misc_args))
            return used_variables
        return execute_loop(loop_array_index, find_used_variables_without_formatting_in_loop_array_index, (loop_array_index.loop_array_index, is_constant, known_dependencies), misc_args)

    def find_used_variables_without_formatting_in_statement(statement, array_mode, node_name, known_dependencies):
        misc_args = create_misc_args(define_call = {}, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = '')
        if array_mode:
            used_variables = []
            is_constant = statement.constant_index == 'constant_index'
            for loop_array_index in statement.assigns:
                used_variables.extend(find_used_variables_without_formatting_in_loop_array_index((loop_array_index, is_constant, known_dependencies), misc_args))
            used_variables.extend(find_used_variables_without_formatting_in_assign(statement.default_value, known_dependencies, misc_args))
            return used_variables
        return find_used_variables_without_formatting_in_assign(statement.assign, known_dependencies, misc_args)

    def format_return_status(return_status):
        return return_status.capitalize()

    def create_parallel_one(current_node, node_name, inactive_condition, indent_level):
        original_inactive_condition = inactive_condition
        names = []
        for child in current_node.children:
            (child_name, indent_level) = walk_tree(child, inactive_condition, indent_level)
            names.append(child_name)
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = original_inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| elem ' + format_return_status('failure')  + ' = ' + format_return_status('failure') + os.linesep
            + indent(1) + '| elem ' + format_return_status('success')  + ' = ' + format_return_status('success') + os.linesep
            + indent(1) + '| otherwise' + ' = ' + format_return_status('running') + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_parallel_all(current_node, node_name, inactive_condition, indent_level):
        original_inactive_condition = inactive_condition
        names = []
        for child in current_node.children:
            (child_name, indent_level) = walk_tree(child, inactive_condition, indent_level)
            names.append(child_name)
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = original_inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| elem ' + format_return_status('failure')  + ' = ' + format_return_status('failure') + os.linesep
            + indent(1) + '| elem ' + format_return_status('running')  + ' = ' + format_return_status('running') + os.linesep
            + indent(1) + '| otherwise' + ' = ' + format_return_status('success') + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_parallel(current_node, node_name, _, inactive_condition, indent_level):
        return (create_parallel_all(current_node, node_name, inactive_condition, indent_level) if current_node.parallel_policy == 'success_on_all' else create_parallel_one(current_node, node_name, inactive_condition, indent_level))

    def create_sequence(current_node, node_name, _, inactive_condition, indent_level):
        original_inactive_condition = inactive_condition
        names = []
        for child in current_node.children:
            (child_name, indent_level) = walk_tree(child, inactive_condition, indent_level)
            names.append(child_name)
            inactive_condition = '((/=) ' + child_name + '___VAL' + format_return_status('success')
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = original_inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| elem ' + format_return_status('failure')  + ' = ' + format_return_status('failure') + os.linesep
            + indent(1) + '| elem ' + format_return_status('running')  + ' = ' + format_return_status('running') + os.linesep
            + indent(1) + '| otherwise' + ' = ' + format_return_status('success') + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_selector(current_node, node_name, _, inactive_condition, indent_level):
        original_inactive_condition = inactive_condition
        names = []
        for child in current_node.children:
            (child_name, indent_level) = walk_tree(child, inactive_condition, indent_level)
            names.append(child_name)
            inactive_condition = '((/=) ' + child_name + '___VAL' + format_return_status('failure')
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = original_inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| elem ' + format_return_status('success')  + ' = ' + format_return_status('success') + os.linesep
            + indent(1) + '| elem ' + format_return_status('running')  + ' = ' + format_return_status('running') + os.linesep
            + indent(1) + '| otherwise' + ' = ' + format_return_status('failure') + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_inverter(current_node, node_name, _, inactive_condition, indent_level):
        (child_name, indent_level) = walk_tree(current_node.child, inactive_condition, indent_level)
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| ' + child_name + 'VAL == ' + format_return_status('failure')  + ' = ' + format_return_status('success') + os.linesep
            + indent(1) + '| ' + child_name + 'VAL == ' + format_return_status('success')  + ' = ' + format_return_status('failure') + os.linesep
            + indent(1) + '| otherwise' + ' = ' + child_name + 'VAL' + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_X_is_Y(current_node, node_name, _, inactive_condition, indent_level):
        (child_name, indent_level) = walk_tree(current_node.child, inactive_condition, indent_level)
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| ' + child_name + 'VAL == ' + format_return_status(current_node.x)  + ' = ' + format_return_status(current_node.y) + os.linesep
            + indent(1) + '| otherwise' + ' = ' + child_name + 'VAL' + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        return node_name

    def create_check(current_node, node_name, argument_pairs, inactive_condition, indent_level):
        for argument_name in argument_pairs:
            constants[argument_name] = argument_pairs[argument_name]
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = inactive_condition)
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_return_status('invalid') + os.linesep
            + indent(1) + '| ' + format_code(current_node.condition, misc_args) + ' = Success' + os.linesep
            + indent(1) + '| otherwise' + ' = Failure' + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + 'VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        for argument_name in argument_pairs:
            constants.pop(argument_name)
        return node_name

    def create_action(current_node, node_name, argument_pairs, inactive_condition, indent_level):
        for argument_name in argument_pairs:
            constants[argument_name] = argument_pairs[argument_name]
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = inactive_condition)
        # local order: define without override, define with override, non-define without override, non-define with override.
        has_override = set(format_variable_name_only(initial_statement.variable, misc_args) for initial_statement  in current_node.init_statements)
        for variable in current_node.local_variables:
            if variable.model_as == 'DEFINE':
                variable_name = format_variable_name_only(variable, misc_args)
                if variable_name not in has_override:
                    (function_declaration, depends_on, specification_call, iteration_call) = handle_variable_statement_define(variable, variable, known_dependencies, misc_args) # this should use the most recent define calls
                    define_calls_iteration_mode[variable_name] = iteration_call
                    define_calls_specification_mode[variable_name] = specification_call
                    known_dependencies[variable_name] = depends_on
                    function_declarations.append(function_declaration)
        for initial_statement in current_node.initial_statements:
            if initial_statement.variable.model_as == 'DEFINE':
                variable_name = format_variable_name_only(initial_statement.variable, misc_args)
                (function_declaration, depends_on, specification_call, iteration_call) = handle_variable_statement_define(initial_statement.variable, initial_statement, known_dependencies, misc_args) # this should use the most recent define calls
                define_calls_iteration_mode[variable_name] = iteration_call
                define_calls_specification_mode[variable_name] = specification_call
                known_dependencies[variable_name] = depends_on
                function_declarations.append(function_declaration)
        for variable in current_node.local_variables:
            if variable.model_as != 'DEFINE':
                variable_name = format_variable_name_only(variable, misc_args)
                if variable_name not in has_override:
                    state_variables.append((variable_name, variable_type(variable, declared_enumerations, constants)))
                    initial_states_delayed_list.append(handle_variable_statement(variable, misc_args)[0])
        for initial_statement in current_node.initial_statements:
            if initial_statement.variable.model_as != 'DEFINE':
                variable_name = format_variable_name_only(variable, misc_args)
                if variable_name not in has_override:
                    state_variables.append((variable_name, variable_type(variable, declared_enumerations, constants)))
                    initial_states_delayed_list.append(handle_variable_statement(variable, misc_args)[0])
        misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = node_name, specification_mode = False, inactive_condition = inactive_condition)
        for statement in current_node.pre_update_statements:
            result = handle_statement(statement, misc_args)
            next_states_list.extend(result[0])
            next_states_delayed_list.extend(result[1])
        next_states_list.append((
            '-- for ' + node_name + os.linesep
            + 'value' + os.linesep
            + indent(1) + '| ' + misc_args['inactive_condition'] + ' ='  + format_return_status('invalid') + os.linesep
            + ''.join(
                [
                    (indent(1) + '| ' + format_code(case_result.condition, misc_args) + ' = ' + format_return_status(case_result.status) + os.linesep)
                    for case_result in current_node.return_statement.case_results
                ]
            )
            + indent(1) + '| otherwise = ' + format_return_status(current_node.return_statement.status_default_result.status) + os.linesep
            + 'result = next_func value' + os.linesep
            + indent(1) + 'where' + os.linesep
            + indent(2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(2) + 'next_func ' + node_name + '___VAL = result' + os.linesep
            + indent(3) + 'where' + os.linesep
            , 4))
        for statement in current_node.post_update_statements:
            result = handle_statement(statement, misc_args)
            next_states_list.extend(result[0])
            next_states_delayed_list.extend(result[1])
        for argument_name in argument_pairs:
            constants.pop(argument_name)
        return node_name

    def walk_tree(current_node, inactive_condition, indent_level):
        argument_pairs = {}
        while hasattr(current_node, 'sub_root'):
            current_node = current_node.sub_root
        node_name = ''
        if hasattr(current_node, 'leaf'):
            node_name = current_node.name if hasattr(current_node, 'name') else current_node.leaf.name
            all_arguments = []
            for argument in current_node.arguments:
                arg_func = build_meta_func(argument)
                all_arguments.extend(arg_func((constants, {})))
            argument_pairs = {
                current_node.leaf.arguments[index].argument_name: all_arguments[index]
                for index in range(len(current_node.arguments))
            }
            current_node = current_node.leaf
        else:
            node_name = current_node.name
        node_name = node_name + '___'
        return create_node[current_node.node_type](current_node, node_name, argument_pairs, inactive_condition, indent_level)

    function_format = {
        # (name, overwrite, inputs, output)
        'if' : ('ifThenElse', format_function_if),
        'loop' : ('loop', format_function_loop),
        'abs' : ('abs', format_function_default),
        'max' : ('max', format_function_default),
        'min' : ('min', format_function_default),
        'sin' : ('sin', format_function_default),
        'cos' : ('cos', format_function_default),
        'tan' : ('tan', format_function_default),
        'ln' : ('log', format_function_default),
        'not' : ('not', format_function_default),
        'and' : ('(&&)', format_function_default),
        'or' : ('(||)', format_function_default),
        'xor' : ('sereneXOR', format_function_default),
        'xnor' : ('sereneXNOR', format_function_default),
        'implies' : ('sereneIMPLIES', format_function_default),
        'equivalent' : ('(==)', format_function_default),
        'eq' : ('(==)', format_function_default),
        'neq' : ('(/=)', format_function_default),
        'lt' : ('(<)', format_function_default),
        'gt' : ('(>)', format_function_default),
        'lte' : ('(<=)', format_function_default),
        'gte' : ('(>=)', format_function_default),
        'neg' : ('negate', format_function_default),
        'add' : ('(+)', format_function_default),
        'sub' : ('(-)', format_function_default),
        'mult' : ('(*)', format_function_default),
        'idiv' : ('quot', format_function_default),  #quot does integer division and rounds to 0.
        'mod' : ('mod', format_function_default),
        'rdiv' : ('/', format_function_default),
        'floor' : ('floor', format_function_default),
        'count' : ('count', format_function_default),
        'index' : ('(!)', format_function_default),
        'active' : ('.active', format_function_default),
        'success' : ('.status = success', format_function_default),
        'running' : ('.status = running', format_function_default),
        'failure' : ('.status = failure', format_function_default),
        'exists_globally' : ('ctlEG', format_function_ctl),
        'exists_next' : ('ctlEX', format_function_ctl),
        'exists_finally' : ('ctlEF', format_function_ctl),
        'exists_until' : ('ctlEU', format_function_ctl),
        'always_globally' : ('ctlAG', format_function_ctl),
        'always_next' : ('ctlAX', format_function_ctl),
        'always_finally' : ('ctlAF', format_function_ctl),
        'always_until' : ('ctlAU', format_function_ctl)
    }
    create_node = {
        'sequence' : create_sequence,
        'selector' : create_selector,
        'parallel' : create_parallel,
        'X_is_Y' : create_X_is_Y,
        'inverter' : create_inverter,
        'check' : create_check,
        'environment_check' : create_check,
        'action' : create_action
    }
    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit)
    hyper_mode = model.hypersafety
    use_reals = model.use_reals
    if model.neural:
        import onnxruntime

    define_calls_specification_mode = {}
    define_calls_iteration_mode = {}
    known_dependencies = {}
    state_variables = []
    function_declarations = []
    base_misc_args = create_misc_args(define_call = define_calls_iteration_mode, loop_references = {}, node_name = None, specification_mode = False, inactive_condition = '')
    next_states_list = []
    next_states_delayed_list = []
    next_states_environment_list = []
    initial_states_list = []
    initial_states_delayed_list = []
    for variable in model.variables:
        if is_local(variable):
            continue
        variable_name = format_variable_name_only(variable, base_misc_args)
        if variable.model_as == 'DEFINE':
            (function_declaration, depends_on, specification_call, iteration_call) = handle_variable_statement_define(variable, variable, known_dependencies, base_misc_args) # this should use the most recent define_calls
            define_calls_iteration_mode[variable_name] = iteration_call
            define_calls_specification_mode[variable_name] = specification_call
            known_dependencies[variable_name] = depends_on
            function_declarations.append(function_declaration)
        else:
            state_variables.append((variable_name, variable_type(variable, declared_enumerations, constants)))

    (root_name, cur_indent_level) = walk_tree(model.root, 'False', 4)

    for variable in model.variables:
        if is_local(variable):
            continue
        if variable.model_as != 'DEFINE':
            initial_states_list.extend(handle_variable_statement(variable, base_misc_args)[0])
    for env_variable_statement in model.update:
        next_states_environment_list.extend(handle_variable_statement(env_variable_statement, base_misc_args))
    initial_states_list = initial_states_list + initial_states_delayed_list
    next_states_list = next_states_list + next_states_delayed_list + next_states_environment_list
    with open(output_file, 'w', encoding = 'utf-8') as out_file:
        write_string = 'module ' + output_file.rsplit('/', 1)[1].split('.', 1)[0] + ' where' + os.linesep
        with open('./haskell_checker_file/imports.hs', 'r', encoding = 'utf-8') as in_file:
            write_string += in_file.read()
        write_string += (
            'data State = State {' + os.linesep
            + (indent(1) if len(state_variables) > 0 else '')
            + (indent(1) + ', ').join(map(lambda x: x[0] + ' :: ' + x[1] + os.linesep, state_variables))
            + indent(1) + '}' + os.linesep
            + indent(1) + 'deriving (Eq, Ord, Show)'
        )
        for initial_state in initial_states_list:
            write_string
            
        out_file.write(write_string)
        
    # what do we need the tree to output?
    # APPEND: local define variables (function_declaration, depends_on, specification_call, iteration_call)
    # APPEND: local not define variables (variable_name, variable_type, initial_statement)
    # APPEND: the environment statements to be handled later.
    # APPEND: the formatted code for nextStates
    # UPDATE: node names
    # UPDATE: node names map
    # the previous node name (used so we can calibrate inactive_condition, see below)
    # the indent_level

    # we modify next_states to have a guard that checks the tick condition and returns a singleton with the current state if it fails.

    # so crucially, we need to write the function that determines when a node runs. I think we can handle that using the tree.
    # e.g. we call the tree and let it know under what conditions the node is inactive
    # for the root we pass False
    # if a node is a selector, it will pass w/e it received to its first child. For all remaining children, it will pass previous child != Failure
    # if a node is a sequence, it will pass w/e it received to its first child. For all remaining children, it will pass previous child != Success
    # if a node is a parallel, it will always pass w/e it received.
    # if a node is a decorator, it will always pass w/e it received.

    # output
    # module NAME where
    # import file and additional types and such
    # state declaration
    # initial states
    # next states
    # (move this into file?) reachable states
    # (move this into file?) state map
    # COPY A FILE HERE (specification checkers mostly).
    # speficiations
    # main method

    (_, _, _, nodes, local_variables, initial_statements, statements) = walk_tree(model.root)

    behaverify_variables = {} # here to make sure the variable is in the namespace.
    behaverify_variables = get_behaverify_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))[0]
    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    args = arg_parser.parse_args()
    dsl_to_nuxmv(args.metamodel_file, args.model_file, args.output_file, args.recursion_limit)
