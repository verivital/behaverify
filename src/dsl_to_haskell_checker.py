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
        return create_misc_args(copy_loop_references(misc_args['loop_references']), misc_args['node_name'], misc_args['use_stages'], misc_args['overwrite_stage'], misc_args['define_substitutions'], misc_args['specification_writing'], misc_args['specification_warning'])

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

    def create_misc_args(define_call, loop_references, node_name, specification_mode):
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
            'specification_mode' : specification_mode
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
        guard_string = indent(misc_args['indent_level']) + 'guard_' + str(case_number) + ' = ' + (
            format_code(case_result.condition, misc_args)
            if hasattr(case_result, 'condition') else
            'True'
        ) + os.linesep
        vals = []
        for value in case_result.values:
            vals.extend(format_code(value, misc_args))
        value_string = ''.join([
            (indent(misc_args['indent_level']) + 'value_' + str(case_number) + '_' + str(value_number) + ' = ' + value + os.linesep)
            for (value_number, value) in enumerate(vals)
        ])
        return (
            guard_string + value_string,
            indent(misc_args['indent_level'] + 1) + '| guard_' + str(case_number) + ' = ' + (
                ('Set.singleton value_' + str(case_number) + '_0')
                if len(vals) > 1 else
                ('Set.fromList [' + ', '.join(map(lambda x: 'value_' + str(case_number) + '_' + str(x), range(len(vals)))) + ']')
            ) + os.linesep
        )

    def handle_assign_value(variable, assign_value, misc_args):
        case_result_strings = [handle_case_result(case_result, case_number, misc_args) for (case_number, case_result) in enumerate(assign_value.case_results)] + [handle_case_result(assign_value.default_result, len(assign_value.case_results), misc_args)]
        return (
            indent(misc_args['indent_level']) + '-- for ' + format_variable_name_only(variable, misc_args) + os.linesep
            + ''.join(map(lambda x: x[0], case_result_strings))
            + indent(misc_args['indent_level']) + 'values' + os.linesep
            + ((indent(misc_args['indent_level'] + 1) + '| ' + misc_args['inactive_condition'] + ' = ' + format_variable_name_only(variable, misc_args) + os.linesep) if misc_args['inactive_condition'] is not None else '')
            + ''.join(map(lambda x: x[1], case_result_strings))
            + indent(misc_args['indent_level']) + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'where' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func :: ' + variable_type(variable) + ' -> Set.Set State' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func ' + format_variable_name_only(variable, misc_args) + ' = result' + os.linesep
            + indent(misc_args['indent_level'] + 3) + 'where' + os.linesep
        )

    def handle_return_statement(node_name, return_statement, misc_args):
        return (
            indent(misc_args['indent_level']) + '-- for ' + node_name + os.linesep
            + indent(misc_args['indent_level']) + 'values' + os.linesep
            + ((indent(misc_args['indent_level'] + 1) + '| ' + misc_args['inactive_condition'] + ' = Invalid' + os.linesep) if misc_args['inactive_condition'] is not None else '')
            + ''.join(
                [
                    (indent(misc_args['indent_level'] + 1) + '| ' + format_code(case_result.condition, misc_args) + ' = ' + format_return_status(case_result.status))
                    for case_result in return_statement.case_results
                ]
            )
            + (indent(misc_args['indent_level'] + 1) + '| otherwise = ' + format_return_status(return_statement.status_default_result.status))
            + indent(misc_args['indent_level']) + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'where' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func :: NodeStatus -> Set.Set State' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func ' + node_name + '___val = result' + os.linesep
            + indent(misc_args['indent_level'] + 3) + 'where' + os.linesep
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
        return (handle_assign_value(assign_var, variable_statement.assign, misc_args), misc_args['indent_level'] + 4)

    def handle_write_statement(write_statement, misc_args):
        new_misc_args = copy_misc_args(misc_args)
        result = ''
        for variable_statement in write_statement.update:
            (new_string, new_indent) = handle_variable_statement(variable_statement, new_misc_args)
            result += new_string
            new_misc_args['indent_level'] = new_indent
        return (result, new_misc_args['indent_level'])

    def handle_read_statement(read_statement, misc_args):
        new_misc_args = copy_misc_args(misc_args)
        result = (
            indent(new_misc_args['indent_level']) + '-- for READ STATEMENT: ' + str(read_statement.name) + os.linesep
            + indent(new_misc_args['indent_level']) + 'values' + os.linesep
            + ((indent(new_misc_args['indent_level'] + 1) + '| ' + new_misc_args['inactive_condition'] + ' = Set.singleton False' + os.linesep) if new_misc_args['inactive_condition'] is not None else '')
            + indent(new_misc_args['indent_level'] + 1) + '| ' + format_code(read_statement.condition, new_misc_args) + ' = ' + ('Set.fromList [True, False]' if read_statement.non_determinism else 'Set.singleton True') + os.linesep
            + indent(new_misc_args['indent_level'] + 1) + '| otherwise = Set.singleton False' + os.linesep
            + indent(misc_args['indent_level']) + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
            + indent(misc_args['indent_level'] + 1) + 'where' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func :: Bool -> Set.Set State' + os.linesep
            + indent(misc_args['indent_level'] + 2) + 'next_func read_condition = result' + os.linesep
            + indent(misc_args['indent_level'] + 3) + 'where' + os.linesep
        )
        new_misc_args['indent_level'] += 4
        if read_statement.condition_variable is not None:
            if is_array(read_statement.condition_variable):
                raise ValueError
            result += (
                indent(new_misc_args['indent_level']) + 'values' + os.linesep
                + ((indent(misc_args['indent_level'] + 1) + '| ' + new_misc_args['inactive_condition'] + ' = ' + format_variable_name_only(read_statement.condition_variable, misc_args) + os.linesep) if new_misc_args['inactive_condition'] is not None else '')
                + indent(misc_args['indent_level'] + 1) + '| read_condition = ' + (('Set.fromList [True, False]') if read_statement.non_determinism == 'non_determinism' else 'Set.singleton True') + os.linesep
                + indent(misc_args['indent_level'] + 1) + '| otherwise = Set.singleton False' + os.linesep
                + indent(misc_args['indent_level']) + 'result = Set.foldr (Set.union . next_func) Set.empty values' + os.linesep
                + indent(misc_args['indent_level'] + 1) + 'where' + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'next_func :: Bool -> Set.Set State' + os.linesep
                + indent(misc_args['indent_level'] + 2) + 'next_func ' + format_variable_name_only(read_statement.condition_variable, new_misc_args) + ' = result' + os.linesep
                + indent(misc_args['indent_level'] + 3) + 'where' + os.linesep
            )
            new_misc_args['indent_level'] += 4
        new_misc_args['inactive_condition'] = '(||) ' + new_misc_args['inactive_condition'] + '(not read_condition)'
        for variable_statement in read_statement.variable_statements:
            (new_string, new_indent) = handle_variable_statement(variable_statement, new_misc_args)
            result += new_string
            new_misc_args['indent_level'] = new_indent
        return (result, new_misc_args['indent_level'])

    def handle_statement(statement, misc_args):
        return (
            handle_variable_statement(statement.variable_statement, misc_args)
            if statement.variable_statement is not None else
            (
                handle_read_statement(statement.read_statement, misc_args)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, misc_args)
            )
        )

    def create_define_statements(model, local_variables, initial_statements):
        '''
        this constructs and returns variables and local variables.
        variables are constructed based on variables and environment_variables
        -- arguments
        @ model := a model. one created using behaverify.tx as the metamodel (probably)
        @ keep_stage_0 := a boolean. indicates if we should be default keep_stage_0.
        -- return
        @ variables := a dictionary from variable_name (string) to variable informaion
        @ local_variables := a dictionary from variable_name (string) to variable informaion
        -- side effects
        none. purely functional.
        '''

        def find_used_variables_without_formatting_in_code(code, misc_args):
            if code.atom is not None:
                (atom_class, atom) = handle_constant_or_reference_no_type(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
                return (
                    (
                        known_dependencies[format_variable_name_only(atom, misc_args)]
                        if atom.model_as == 'DEFINE' else
                        [(
                            format_variable_name_only(atom, create_misc_args(define_call = None, loop_references = None, node_name = misc_args['node_name'], specification_mode = False)),
                            format_variable_name_only(atom, create_misc_args(define_call = None, loop_references = None, node_name = misc_args['node_name'], specification_mode = True)),
                            variable_type(atom, declared_enumerations, constants)
                        )]
                    )
                    if atom_class == 'VARIABLE' else []
                )
            if code.code_statement is not None:
                return find_used_variables_without_formatting_in_code(code.code_statement, misc_args)
            function_call = code.function_call
            if function_call.function_name == 'loop':
                return execute_loop(function_call, find_used_variables_without_formatting_in_code, function_call.values[0], misc_args)
            used_variables = []
            for value in function_call.values:
                used_variables.extend(find_used_variables_without_formatting_in_code(value, misc_args))
            if function_call.function_name != 'index':
                return used_variables
            var_func = build_meta_func(function_call.to_index)
            variable = resolve_potential_reference_no_type(var_func((constants, misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
            new_misc_args = adjust_args(function_call, misc_args)
            used_variables.append((
                format_variable_name_only(variable, create_misc_args(define_call = None, loop_references = None, node_name = new_misc_args['node_name'], specification_mode = False)),
                format_variable_name_only(variable, create_misc_args(define_call = None, loop_references = None, node_name = new_misc_args['node_name'], specification_mode = True)),
                variable_type(atom, declared_enumerations, constants)
            ))
            return used_variables

        def find_used_variables_without_formatting_in_assign(assign, misc_args):
            used_variables = []
            for case_result in assign.case_results:
                used_variables.extend(find_used_variables_without_formatting_in_code(case_result.condition, misc_args))
                for value in case_result.values:
                    used_variables.extend(find_used_variables_without_formatting_in_code(value, misc_args))
            for value in assign.default_result.values:
                used_variables.extend(find_used_variables_without_formatting_in_code(value, misc_args))
            return used_variables

        def find_used_variables_without_formatting_in_loop_array_index(packaged_args, misc_args):
            (loop_array_index, is_constant) = packaged_args
            if loop_array_index.array_index is not None:
                used_variables = find_used_variables_without_formatting_in_assign(loop_array_index.array_index.assign, misc_args)
                if not is_constant:
                    for index in loop_array_index.array_index.index_expr:
                        used_variables.extend(find_used_variables_without_formatting_in_code(index, misc_args))
                return used_variables
            return execute_loop(loop_array_index, find_used_variables_without_formatting_in_loop_array_index, (loop_array_index.loop_array_index, is_constant), misc_args)

        def find_used_variables_without_formatting_in_statement(statement, array_mode, node_name):
            misc_args = create_misc_args(define_call = {}, loop_references = {}, node_name = node_name, specification_mode = False)
            if array_mode:
                used_variables = []
                is_constant = statement.constant_index == 'constant_index'
                for loop_array_index in statement.assigns:
                    used_variables.extend(find_used_variables_without_formatting_in_loop_array_index((loop_array_index, is_constant), misc_args))
                used_variables.extend(find_used_variables_without_formatting_in_assign(statement.default_value, misc_args))
                return used_variables
            return find_used_variables_without_formatting_in_assign(statement.assign, misc_args)

        def create_possible_values(var_keys):
            # does not work with local variables. Doesn't need to; neural networks cannot be local, and therefore cannot depends on local variables.
            possible_values = []
            for var_key in var_keys:
                fix_domain_of_variable(var_key)
                variable = behaverify_variables[var_key]
                domain =  variable['custom_value_range'] if variable['custom_value_range'] is not None else set(range(variable['min_value'], variable['max_value'] + 1))
                var_name = (var_key_to_obj[var_key]).name
                if len(possible_values) == 0:
                    possible_values = [[(var_name, val)] for val in domain]
                else:
                    possible_values = [[*old_val, (var_name, val)] for val in domain for old_val in possible_values]
            return possible_values
        def possible_values_from_loop_array_index(loop_array_index, packaged_args, misc_args):
            loop_references = misc_args['loop_references']
            (list_of_list_of_inputs, ) = packaged_args
            if loop_array_index.array_index is not None:
                return possible_values_from_assign(loop_array_index.array_index.assign, list_of_list_of_inputs, loop_references)
            return set(execute_loop(loop_array_index, possible_values_from_loop_array_index, packaged_args, misc_args))
        def possible_values_from_assign(assign, list_of_list_of_inputs, loop_references):
            domain_values = set()
            value_funcs = []
            for case_result in assign.case_results:
                value_funcs.append(build_meta_func(case_result.values[0]))
            value_funcs.append(build_meta_func(assign.default_result.values[0]))
            if len(list_of_list_of_inputs) == 0:
                # the value would appear to be a constant
                # we can compute this directly then.
                for value_func in value_funcs:
                    domain_values.add(resolve_potential_reference_no_type(value_func((constants, loop_references))[0], declared_enumerations, {}, {}, constants, loop_references)[1])
            for list_of_inputs in list_of_list_of_inputs:
                new_loop_references = dict(list_of_inputs)
                new_loop_references.update(loop_references)
                for value_func in value_funcs:
                    domain_values.add(resolve_potential_reference_no_type(value_func((constants, loop_references))[0], declared_enumerations, {}, {}, constants, new_loop_references)[1])
            return domain_values
        def fix_domain_of_variable(var_key):
            # does not work with local variables. Doesn't need to; neural networks cannot be local, and therefore cannot depends on local variables.
            variable = behaverify_variables[var_key]
            if variable['mode'] != 'DEFINE' or variable['custom_value_range'] is not None or variable['min_value'] is not None:
                return
            var_obj = var_key_to_obj[var_key]
            list_of_list_of_inputs = create_possible_values(variable['depends_on'])
            if variable['array_size'] is not None:
                domain_values = possible_values_from_assign(var_obj.default_value, list_of_list_of_inputs, {})
                for loop_array_index in var_obj.assigns:
                    domain_values.update(possible_values_from_loop_array_index(loop_array_index, (list_of_list_of_inputs, ), create_misc_args(loop_references = {}, node_name = None, use_stages = False, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False)))
            else:
                domain_values = possible_values_from_assign(var_obj.assign, list_of_list_of_inputs, {})
            variable['custom_value_range'] = domain_values
            return

        known_dependencies = {}
        definition_functions = {}
        definition_function_calls_spec = {}
        definition_function_calls_iter = {}
        misc_args_fake = create_misc_args(define_call = {}, loop_references = {}, node_name = None, specification_mode = True)
        for variable in model.variables:
            if variable.model_as == 'DEFINE':
                depends_on = sorted(list(set(find_used_variables_without_formatting_in_statement(variable, is_array(variable), None))))
                variable_name = format_variable_name_only(variable, misc_args_fake)
                known_dependencies[variable_name] = depends_on
                definition_functions[variable_name] = (
                    variable_name + ' :: ' + ' -> '.join(map(lambda x : x[2], depends_on)) + (' -> ' if len(depends_on) > 0 else '') + variable_type(variable, declared_enumerations, constants) + os.linesep
                    + variable_name + ' ' + ' '.join(map(lambda x : x[0], depends_on)) + ' = result' + os.linesep
                )
                definition_function_calls_spec[variable_name] = '(' + variable_name + ' ' + ' '.join(map(lambda x : '(' + x[1] + ' stage)')) + ')'
                definition_function_calls_iter[variable_name] = '(' + variable_name + ' ' + ' '.join(map(lambda x : x[1])) + ')'
        for variable in model.variables:
            if variable.model_as == "DEFINE":
                if is_array(variable):
                    definition_functions[variable_name] += (
                        indent(1) + 'where' + os.linesep
                        + indent(2) + 'default_value = '
                        )

    def create_composite(current_node, node_name, modifier, node_names, node_names_map, parent_name):
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        children = []
        nodes = {}
        local_variables = []
        initial_statements = []
        statements = []
        for child in current_node.children:
            # (child_name, node_names, nodes, local_variables, initial_statements, statements)
            new_vals = walk_tree(child, node_name, cur_node_names, cur_node_names_map)
            children.append(new_vals[0])
            cur_node_names = new_vals[1]
            cur_node_names_map = new_vals[2]
            nodes.update(new_vals[3])
            local_variables = local_variables + new_vals[4]
            initial_statements = initial_statements + new_vals[5]
            statements = statements + new_vals[6]
        nodes[node_name] = create_node_template(node_name, parent_name, children,
                                                'composite', current_node.node_type, (('_' + current_node.parallel_policy) if current_node.node_type == 'parallel' else ''), current_node.memory,
                                                True, True, True)
        return (node_name, cur_node_names, cur_node_names_map, nodes, local_variables, initial_statements, statements)

    def create_decorator(current_node, node_name, modifier, node_names, node_names_map, parent_name, additional_arguments = None):
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        children = []
        nodes = {}
        local_variables = []
        initial_statements = []
        statements = []
        new_vals = walk_tree(current_node.child, node_name, cur_node_names, cur_node_names_map)
        children.append(new_vals[0])
        cur_node_names = new_vals[1]
        cur_node_names_map = new_vals[2]
        nodes.update(new_vals[3])
        local_variables = local_variables + new_vals[4]
        initial_statements = initial_statements + new_vals[5]
        statements = statements + new_vals[6]
        nodes[node_name] = create_node_template(node_name, parent_name, children,
                                                'decorator', current_node.node_type, '', '',
                                                True, True, True, additional_arguments)
        return (node_name, cur_node_names, cur_node_names_map, nodes, local_variables, initial_statements, statements)

    def create_X_is_Y(current_node, node_name, modifier, node_names, node_names_map, parent_name):
        return create_decorator(current_node, node_name, modifier, node_names, node_names_map, parent_name, [current_node.x, current_node.y])

    def create_check(current_node, argument_pairs, node_name, modifier, node_names, node_names_map, parent_name):
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        return (
            node_name, cur_node_names, cur_node_names_map,
            {node_name : create_node_template(node_name, parent_name, [],
                                              'leaf', current_node.node_type, '', '',
                                              True, False, True, custom_type = current_node.name)
             },
            [], [], [(node_name, argument_pairs, 'check', current_node.condition)]
        )

    def create_action(current_node, argument_pairs, node_name, modifier, node_names, node_names_map, parent_name):
        cur_node_names = {node_name}.union(node_names)
        cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
        return (
            node_name, cur_node_names, cur_node_names_map,
            {node_name : create_node_template(node_name, parent_name, [],
                                              'leaf', current_node.node_type, '', '',
                                              True, True, True, custom_type = current_node.name)
             },
            list(map(lambda x : (node_name, x), current_node.local_variables)),
            list(map(lambda x : (node_name, argument_pairs, x), current_node.init_statements)),
            (
                list(map(lambda x : (node_name, argument_pairs, 'statement', x), current_node.pre_update_statements))
                +
                [(node_name, argument_pairs, 'return', current_node.return_statement)]
                +
                list(map(lambda x : (node_name, argument_pairs, 'statement', x), current_node.post_update_statements))
            )
        )

    def walk_tree(current_node, parent_name = None, node_names = None, node_names_map = None):
        if node_names is None:
            node_names = set()
        if node_names_map is None:
            node_names_map = {}
        argument_pairs = None
        while hasattr(current_node, 'sub_root'):
            current_node = current_node.sub_root
        current_name = current_node.leaf.name if current_node.name is None else current_node.name
        if hasattr(current_node, 'leaf'):
            all_arguments = []
            for argument in current_node.arguments:
                arg_func = build_meta_func(argument)
                all_arguments.extend(arg_func((constants, {})))
            argument_pairs = {
                current_node.leaf.arguments[index].argument_name: all_arguments[index]
                for index in range(len(current_node.arguments))
            }
            current_node = current_node.leaf
        # the above deals with sub_trees and leaf nodes, ensuring that the current_node variable has the next actual node at this point
        # next, we get the name of this node, and correct for duplication

        new_name = create_node_name(current_name, node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        return (
            create_node[current_node.node_type](current_node, node_name, modifier, node_names, node_names_map, parent_name)
            if argument_pairs is None else
            create_node[current_node.node_type](current_node, argument_pairs, node_name, modifier, node_names, node_names_map, parent_name)
        )

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
        'sequence' : create_composite,
        'selector' : create_composite,
        'parallel' : create_composite,
        'X_is_Y' : create_X_is_Y,
        'inverter' : create_decorator,
        'check' : create_check,
        'environment_check' : create_check,
        'action' : create_action
    }
    (model, variables, constants, declared_enumerations) = validate_model(metamodel_file, model_file, recursion_limit)
    hyper_mode = model.hypersafety
    use_reals = model.use_reals
    if model.neural:
        import onnxruntime
    behaverify_variables = {}

    (_, _, _, nodes, local_variables, initial_statements, statements) = walk_tree(model.root)

    behaverify_variables = {} # here to make sure the variable is in the namespace.
    behaverify_variables = get_behaverify_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))[0]
    complete_environment_variables(model, True)
    resolve_statements(statements, nodes)
    complete_environment_variables(model, False)
    specifications = handle_specifications(model.specifications)

    for var_key in behaverify_variables:
        if behaverify_variables[var_key]['custom_value_range'] in ('integer', 'real'):
            continue
        if behaverify_variables[var_key]['min_value'] is not None:
            behaverify_variables[var_key]['custom_value_range'] = str(behaverify_variables[var_key]['min_value']) + '..' + str(behaverify_variables[var_key]['max_value'])
        elif behaverify_variables[var_key]['custom_value_range'] is not None:
            behaverify_variables[var_key]['custom_value_range'] = '{' + ', '.join(map(str, behaverify_variables[var_key]['custom_value_range'])) + '}'
            behaverify_variables[var_key]['custom_value_range'] = behaverify_variables[var_key]['custom_value_range'].replace('{True, False}', 'boolean')
            behaverify_variables[var_key]['custom_value_range'] = behaverify_variables[var_key]['custom_value_range'].replace('{False, True}', 'boolean')
    if behave_only:
        if output_file is None:
            printer = pprint.PrettyPrinter(indent = 4)
            printer.pprint({'nodes' : nodes
                            , 'variables' : behaverify_variables
                            , 'declared_enumerations' : declared_enumerations
                            , 'tick_condition' : tick_condition
                            , 'specifications' : specifications})
        else:
            with open(output_file, 'w', encoding = 'utf-8') as write_file:
                printer = pprint.PrettyPrinter(indent = 4, stream = write_file)
                printer.pprint({'nodes' : nodes
                                , 'variables' : behaverify_variables
                                , 'declared_enumerations' : declared_enumerations
                                , 'tick_condition' : tick_condition
                                , 'specifications' : specifications})
    else:
        write_smv(nodes, behaverify_variables, declared_enumerations, tick_condition, specifications, hyper_mode, output_file, do_not_trim)
    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    args = arg_parser.parse_args()
    dsl_to_nuxmv(args.metamodel_file, args.model_file, args.output_file, args.recursion_limit)
