'''
This module is part of BehaVerify and used to convert .tree files to .smv files for use with nuXmv. It indexes arrays manually.


Author: Serena Serafina Serbinowska
Last Edit: 2023-11-06
'''
import argparse
import pprint
import os
import itertools
import copy
from behaverify_to_smv import write_smv
from serene_functions import build_meta_func
from check_grammar import validate_model

from behaverify_common import create_node_name, create_node_template, create_variable_template, indent, is_local, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max

# a NEXT_VALUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE

def dsl_to_nuxmv(metamodel_file, model_file, output_file, keep_stage_0, keep_last_stage, do_not_trim, behave_only, recursion_limit, return_values):
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
        return ['(' + format_code(function_call.values[0], misc_args)[0] + ' ? ' + format_code(function_call.values[1], misc_args)[0] + ' : ' + format_code(function_call.values[2], misc_args)[0] + ')']

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, function_call.values[0], misc_args)

    def format_function_before(function_name, function_call, misc_args):
        '''function_name(vals)'''
        return [
            function_name + '('
            + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_recursive_before(function_name, function_call, misc_args):
        '''function_name(vals)'''
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return [
            ''.join([(function_name + '(' + formatted_value + ', ') for formatted_value in formatted_values[0:-2]])
            + function_name + '(' + formatted_values[-2] + ', ' + formatted_values[-1] + ')'
            + ')'*(len(formatted_values[0:-2]))
        ]

    def format_function_between(function_name, function_call, misc_args):
        '''(vals function_name vals)'''
        return [
            '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_integer_division(function_name, function_call, misc_args):
        '''(vals function_name vals)'''
        return [
            ('floor' if use_reals else '') + '('
            + (' ' + function_name + ' ').join([(' ' + function_name + ' ').join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_after(function_name, function_call, misc_args):
        '''(node_name.function_name)'''
        return [
            '('
            + (('system' + (('_' + str(misc_args['trace_num'])) if hyper_mode else '') + '.') if misc_args['specification_writing'] else '')
            + function_call.node_name
            + function_name
            + ')'
        ]

    def format_function_before_bounded(function_name, function_call, misc_args):
        '''function_name [min, max] (vals)'''
        (min_val, max_val) = get_min_max(function_call.bound.lower_bound, function_call.bound.upper_bound, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        return [
            function_name + ' [' + str(min_val) + ', ' + str(max_val) + '] '  '('
            + ', '.join([', '.join(format_code(value, misc_args)) for value in function_call.values])
            + ')'
        ]

    def format_function_between_bounded(function_name, function_call, misc_args):
        ''' honestly not sure '''
        (min_val, max_val) = get_min_max(function_call.bound.lower_bound, function_call.bound.upper_bound, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return ['(' + (' ' + function_name + ' [' + str(min_val) + ', ' + str(max_val) + '] ').join(formatted_values) + ')']

    def format_function_before_between(function_name, function_call, misc_args):
        '''probably some spec thing'''
        formatted_values = []
        for value in function_call.values:
            formatted_values.extend(format_code(value, misc_args))
        return (
            function_name[0] + '['
            + (' ' + function_name[1] + ' ').join(formatted_values)
            + ']'
            )

    def case_index(formatted_variable, array_size, index_expression):
        return (
            '(case '
            + ''.join(
                map(
                    lambda index:
                    str(index) + ' = ' + index_expression + ' : ' + formatted_variable + '_index_' + str(index) + '; '
                    ,
                    range(array_size)
                )
            )
            + 'esac)'
        )

    def format_function_index(_, function_call, misc_args):
        new_misc_args = adjust_args(function_call, misc_args)
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
        formatted_variable = format_variable(variable, new_misc_args)
        if function_call.constant_index == 'constant_index':
            index_func = build_meta_func(function_call.values[0])
            index = resolve_potential_reference_no_type(index_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
            return [formatted_variable + '_index_' + str(index)]
        index_expression = format_code(function_call.values[0], new_misc_args)[0]
        return [case_index(formatted_variable, variable_array_size(variable, declared_enumerations, nodes, variables, constants, misc_args['loop_references']), index_expression)]

    def format_function(code, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.'''
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code.function_call, misc_args)

    def create_misc_args(loop_references, node_name, use_stages, overwrite_stage, define_substitutions, specification_writing, specification_warning):
        '''
        -- ARGUMENTS
        @ node_name := the name of the node which caused this to be called. used for formatting local variables.
        @ use_stages := are we using stages for this? (note: does not affect variable renaming).
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        return {
            'loop_references' : loop_references,
            'node_name' : node_name,
            'use_stages' : use_stages,
            'overwrite_stage' : overwrite_stage,
            'define_substitutions' : define_substitutions,
            'trace_num' : 1,  # this can only be modified when dealing with specifications.
            'specification_writing' : specification_writing,
            'specification_warning' : specification_warning
        }

    def compute_stage(variable_key, misc_args):
        variable = behaverify_variables[variable_key]
        overwrite_stage = misc_args['overwrite_stage']
        last_stage = (len(variable['existing_definitions']) - 1) if variable['mode'] == 'DEFINE' else len(variable['next_value'])
        # if define:  minus one because stage 0 appears when we first create a definition
        # if not define: no minus one. Stage 0 always created.
        return (last_stage if overwrite_stage is None or overwrite_stage < 0 else min(overwrite_stage, last_stage))

    def find_used_variables(code, misc_args):
        '''Returns the list of used variables (will also format them)'''
        if code.atom is not None:
            (atom_class, atom) = handle_constant_or_reference_no_type(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
            return [format_variable(atom, adjust_args(code, misc_args))] if atom_class == 'VARIABLE' else []
        if code.code_statement is not None:
            return find_used_variables(code.code_statement, misc_args)
        function_call = code.function_call
        if function_call.function_name == 'loop':
            return execute_loop(function_call, find_used_variables, function_call.values[0], misc_args)
        used_variables = []
        for value in function_call.values:
            used_variables.extend(find_used_variables(value, misc_args))
        if function_call.function_name != 'index':
            return used_variables
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
        new_misc_args = adjust_args(function_call, misc_args)
        formatted_variable = format_variable(variable, new_misc_args)
        return used_variables + [(formatted_variable + '_index_' + str(index)) for index in range(variable_array_size(variable, declared_enumerations, nodes, variables, constants, new_misc_args['loop_references']))]

    def assemble_variable(name, stage, trace_num, specification_writing):
        '''This method should only be called by format variable.'''
        return (
            (('system' + (('_' + str(trace_num)) if hyper_mode else '') + '.') if specification_writing else '')
            + name
            + '_stage_' + str(stage)
        )

    def format_variable(variable_obj, misc_args):
        '''
        -- GLOBALS
        @ variables := a dict of all variables
        -- ARGUMENTS
        @ variable_obj := a textx object of a variable that we will be formatting.
        @ node_name := the name of the node which caused this to be called.
        @ use_stages := are we using stages for this?
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        variable_key = variable_reference(variable_obj.name, is_local(variable_obj), misc_args['node_name'])
        variable = behaverify_variables[variable_key]
        return format_variable_non_object(variable, variable_key, misc_args)

    def format_variable_non_object(variable, variable_key, misc_args):
        use_stages = misc_args['use_stages']
        overwrite_stage = misc_args['overwrite_stage']
        trace_num = misc_args['trace_num']
        specification_writing = misc_args['specification_writing']
        specification_warning = misc_args['specification_warning']
        if misc_args['define_substitutions'] is not None:
            return misc_args['define_substitutions'][variable_key]

        if variable['mode'] == 'DEFINE':
            if overwrite_stage is not None and len(variable['next_value']) > 0:
                return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), trace_num, specification_writing)
            used_vars = tuple(format_variable_non_object(behaverify_variables[dependant_variable_key], dependant_variable_key, misc_args) for dependant_variable_key in variable['depends_on'])
            if used_vars not in variable['existing_definitions']:
                variable['existing_definitions'][used_vars] = len(variable['existing_definitions'])
            stage = variable['existing_definitions'][used_vars]
            return assemble_variable(variable['name'], stage, trace_num, specification_writing)
        # the not define variables are formatted below.
        if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
            if specification_warning and not variable['keep_stage_0']:
                print('A specification is preventing the removal of stage 0 for: ' + variable['name'])
            variable['keep_stage_0'] = True
        if use_stages and (overwrite_stage is None or overwrite_stage < 0 or overwrite_stage == len(variable['next_value'])):
            # we don't need to subtract one from len of next_value because we have one stage not represented in next_value.
            if specification_warning and not variable['keep_last_stage']:
                print('A specification is preventing the removal of last stage for: ' + variable['name'])
            variable['keep_last_stage'] = True
        return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), trace_num, specification_writing)

    def adjust_args(code, misc_args):
        '''
        creates a new arg based on the old one, but modifies it. should only be used by format_code
        Declared not as nested function cuz that would tank performance.
        '''
        new_misc_args = copy_misc_args(misc_args)
        if code.node_name is not None:
            node_name_func = build_meta_func(code.node_name)
            new_misc_args['node_name'] = resolve_potential_reference_no_type(node_name_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
        if code.read_at is not None:
            read_at_func = build_meta_func(code.read_at)
            new_misc_args['overwrite_stage'] = resolve_potential_reference_no_type(read_at_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
        if code.trace_num is not None:
            trace_num_func = build_meta_func(code.trace_num)
            new_misc_args['trace_num'] = resolve_potential_reference_no_type(trace_num_func((constants, new_misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])[1]
        return new_misc_args

    def handle_atom(code, misc_args):
        (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        return (str(atom).upper() if atom_type == 'BOOLEAN' else str(atom)) if atom_class == 'CONSTANT' else (format_variable(atom, adjust_args(code, misc_args)))

    def format_code(code, misc_args):
        return (
            [handle_atom(code, misc_args)] if code.atom is not None else (
                ['(' + formatted_code + ')' for formatted_code in format_code(code.code_statement, misc_args)] if code.code_statement is not None else (
                    format_function(code, misc_args)
                )
            )
        )

    def handle_result(result, misc_args):
        '''should only be called by handle_assign'''
        vals = []
        for value in result.values:
            vals.extend(format_code(value, misc_args))
        non_determinism = len(vals) > 1
        return (non_determinism, ('{' + ', '.join(vals) + '}') if non_determinism else vals[0])

    def handle_assign(assign, misc_args):
        '''should only be called by handle_variable_statement'''
        condition_results = []
        case_results = assign.case_results
        default_result = assign.default_result
        non_determinism = False
        for case_result in case_results:
            (new_non_det, result) = handle_result(case_result, misc_args)
            non_determinism = non_determinism or new_non_det
            condition_results.append((format_code(case_result.condition, misc_args)[0], result))
        (new_non_det, result) = handle_result(default_result, misc_args)
        non_determinism = non_determinism or new_non_det
        condition_results.append(('TRUE', result))
        return (non_determinism, condition_results)

    def handle_array_constant_index_loop(packaged_args, misc_args):
        (loop_array_index, formatted_variable, condition) = packaged_args
        non_determinism = {}
        stage = []
        if loop_array_index.array_index is not None:
            (cur_non_determinism, cur_condition_results) = handle_assign(loop_array_index.array_index.assign, misc_args)
            for index_code in loop_array_index.array_index.index_expr:
                index_func = build_meta_func(index_code)
                for index in index_func((constants, misc_args['loop_references'])):
                    new_index = resolve_potential_reference_no_type(index, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
                    non_determinism[new_index] = cur_non_determinism
                    stage.append((new_index,
                                  ([] if condition is None else [(condition, formatted_variable + '_index_' + str(new_index))]) + cur_condition_results))
        else:
            for (new_stage, new_non_determinism) in execute_loop(loop_array_index, handle_array_constant_index_loop, (loop_array_index.loop_array_index, formatted_variable, condition), misc_args):
                stage.extend(new_stage)
                non_determinism.update(new_non_determinism)
        return [(stage, non_determinism)]

    def handle_array_constant_index(variable_statement, condition, misc_args):
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        non_determinism = {}
        stage = []
        formatted_variable = format_variable(assign_var, misc_args)
        for loop_array_index in variable_statement.assigns:
            (new_stage, new_non_determinism) = handle_array_constant_index_loop((loop_array_index, formatted_variable, condition), misc_args)[0]
            stage.extend(new_stage)
            non_determinism.update(new_non_determinism)
        return (misc_args['node_name'], True, non_determinism, stage)

    def handle_array_unknown_index_loop(packaged_args, misc_args):
        (loop_array_index, formatted_variable, array_size, condition) = packaged_args
        non_determinism = False
        stage = []
        if loop_array_index.array_index is not None:
            (cur_non_determinism, cur_condition_results) = handle_assign(loop_array_index.array_index.assign, misc_args)
            non_determinism = non_determinism or cur_non_determinism
            for index_code in loop_array_index.array_index.index_expr:
                for index in format_code(index_code, misc_args):
                    stage.append((index,
                                  ([] if condition is None else [(condition, case_index(formatted_variable, array_size, index))]) + cur_condition_results))
        else:
            for (cur_condition_results, new_non_determinism) in execute_loop(loop_array_index, handle_array_unknown_index_loop, (loop_array_index.loop_array_index, formatted_variable, array_size, condition), misc_args):
                stage.extend(cur_condition_results)
                non_determinism = non_determinism or new_non_determinism
        return [(stage, non_determinism)]

    def handle_array_unknown_index(variable_statement, condition, misc_args):
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        non_determinism = False
        stage = []
        formatted_variable = format_variable(assign_var, misc_args)
        array_size = -1 if condition is None else variable_array_size(assign_var, declared_enumerations, nodes, variables, constants, misc_args['loop_references']) # the point is we only want to do this calcultion if codition is not None
        for loop_array_index in variable_statement.assigns:
            (new_stage, new_non_determinism) = handle_array_unknown_index_loop((loop_array_index, formatted_variable, array_size, condition), misc_args)[0]
            stage.extend(new_stage)
            non_determinism = non_determinism or new_non_determinism
        return (misc_args['node_name'], False, non_determinism, stage)

    def handle_variable_statement(variable_statement, condition, misc_args):
        '''should only be called if init_mode is true or from variable_assignment'''
        assign_var = variable_statement.variable if hasattr(variable_statement, 'variable') else variable_statement
        if is_array(assign_var):
            return (
                handle_array_constant_index(variable_statement, condition, misc_args)
                if variable_statement.constant_index == 'constant_index' else
                handle_array_unknown_index(variable_statement, condition, misc_args)
            )
        (non_determinism, stage) = handle_assign(variable_statement.assign, misc_args)
        return (misc_args['node_name'], non_determinism, ([] if condition is None else [(condition, format_variable(assign_var, misc_args))]) + stage)

    def handle_variable_assignment(statement, condition, read_statement_assign_condition, misc_args):
        '''
        this handles variable assignment
        this should be called if you have a variable assignment and it is not initial
        if you have an initial variable value, call handle_variable_statement
        We keep this seperate so we can track stage removal.
        '''
        assign_var = statement.condition_variable if read_statement_assign_condition else (statement.variable if hasattr(statement, 'variable') else statement)

        variable_key = variable_reference(assign_var.name, is_local(assign_var), misc_args['node_name'])
        variable = behaverify_variables[variable_key]
        keep_stage_0 = variable['keep_stage_0']
        # keep_last_stage = variable['keep_last_stage']
        # we don't need to track keep_last_stage here, because we're going to reset the value after adding a new stage anyways. see below.
        if read_statement_assign_condition:
            non_determinism = statement.non_determinism == 'non_determinism'
            if is_array(assign_var):
                if statement.constant_index == 'constant_index':
                    index_func = build_meta_func(statement.index_of)
                    index = resolve_potential_reference_no_type(index_func((constants, misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
                    next_value = (misc_args['node_name'], True, {index : non_determinism},
                                  [(index, [(format_code(statement.condition, misc_args)[0], '{TRUE, FALSE}' if non_determinism else 'TRUE'), ('TRUE', 'FALSE')])])
                else:
                    index = format_code(statement.index_of, misc_args)[0]
                    next_value = (misc_args['node_name'], False, non_determinism,
                                  [(index, [(format_code(statement.condition, misc_args)[0], '{TRUE, FALSE}' if non_determinism else 'TRUE'), ('TRUE', 'FALSE')])])
        else:
            # this means it was a variable_statement
            next_value = handle_variable_statement(statement, condition, misc_args)
            non_determinism = next_value[-2]
        keep_stage_0 = keep_stage_0 or (not non_determinism)  # there is no point in deleting stage_0 if stage_1 was going to be deterministic.
        variable['next_value'].append(next_value)
        variable['keep_stage_0'] = keep_stage_0
        variable['keep_last_stage'] = variable['force_last_stage']  # and now we've reset it. if force_last_stage is true, this will ensure we use the last stage
        # if force_last_stage is false, then if this variable shows up in someone elses update after this point, we'll keep the last stage
        # if it never shows up after this point, then we can axe it.
        # note: keep_stage_0 takes precedence
        if read_statement_assign_condition:
            return index
        return None

    def handle_specifications(specifications):
        '''this handles specifications'''
        return [
            (
                specification.spec_type
                + ' '
                + format_code(specification.code_statement, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = True, specification_warning = True))[0]
                + ';'
            )
            for specification in specifications
        ]

    def variable_reference(base_name, _is_local_, node_name):
        return ((node_name + '_DOT_' + base_name) if _is_local_ else base_name)

    def resolve_statements(statements, nodes):
        def handle_read_statement(statement, misc_args):
            if statement.condition_variable is not None:
                index = handle_variable_assignment(statement, None, True, misc_args)
                condition = (
                    '!('
                    + (
                        (
                            format_variable(statement.condition_variable, misc_args) + '_index_' + str(index)
                            if statement.constant_index == 'constant_index' else
                            case_index(format_variable(statement.condition_variable, misc_args),
                                       variable_array_size(statement.condition_variable, declared_enumerations, nodes, variables, constants, misc_args['loop_references']),
                                       index
                                       )
                        )
                        if is_array(statement.condition_variable) else
                        format_variable(statement.condition_variable, misc_args)
                    )
                    + ')'
                )
            else:
                condition = '!(' + format_code(statement.condition, misc_args)[0] + ')'
            for variable_statement in statement.variable_statements:
                handle_variable_assignment(variable_statement, condition, False, misc_args)
            return

        def handle_write_statement(statement, misc_args):
            delayed = []
            for var_update in statement.update:
                if var_update.instant:
                    handle_variable_assignment(var_update, None, False, misc_args)
                else:
                    delayed.append((misc_args['node_name'], argument_pairs, var_update))
            return delayed

        def handle_return_statement(statement, nodes, misc_args):
            node_name = misc_args['node_name']
            node = nodes[node_name]
            statuses = {result.status for result in itertools.chain([statement.default_result], statement.case_results)}
            node['return_possibilities']['success'] = 'success' in statuses
            node['return_possibilities']['running'] = 'running' in statuses
            node['return_possibilities']['failure'] = 'failure' in statuses
            variable_list = []
            if not (len(statement.case_results) == 0 or len(statuses) == 1):
                for case_result in statement.case_results:
                    variable_list += find_used_variables(case_result.condition, misc_args)
            variable_list = sorted(list(set(variable_list)))
            node['additional_arguments'] = variable_list
            node['internal_status_module_name'] = (
                None
                if (len(statement.case_results) == 0 or len(statuses) == 1) else
                (
                    node_name + '_module'
                )
            )
            node['internal_status_module_code'] = (
                None
                if (len(statement.case_results) == 0 or len(statuses) == 1) else
                (
                    'MODULE ' + node_name + '_module(' + ', '.join(variable_list) + ')' + os.linesep
                    + indent(1) + 'CONSTANTS' + os.linesep
                    + indent(2) + 'success, failure, running, invalid;' + os.linesep
                    + indent(1) + 'DEFINE' + os.linesep
                    + indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                    + indent(2) + 'internal_status := ' + os.linesep
                    + indent(3) + 'case' + os.linesep
                    + ('').join([(indent(4) + ''
                                  + format_code(case_result.condition, misc_args)[0]
                                  + ' : '
                                  + case_result.status
                                  + ';' + os.linesep)
                                 for case_result in statement.case_results])
                    + indent(4) + 'TRUE : ' + statement.default_result.status + ';' + os.linesep
                    + indent(3) + 'esac;' + os.linesep
                )
            )
            return

        def handle_condition(condition, nodes, misc_args):
            node_name = misc_args['node_name']
            node = nodes[node_name]
            variable_list = find_used_variables(condition, misc_args)
            variable_list = sorted(list(set(variable_list)))
            node['additional_arguments'] = variable_list
            node['internal_status_module_name'] = node_name + '_module'
            node['internal_status_module_code'] = (
                'MODULE ' + node_name + '_module(' + ', '.join(variable_list) + ')' + os.linesep
                + indent(1) + 'CONSTANTS' + os.linesep
                + indent(2) + 'success, failure, running, invalid;' + os.linesep
                + indent(1) + 'DEFINE' + os.linesep
                + indent(2) + 'status := active ? internal_status : invalid;' + os.linesep
                + indent(2) + 'internal_status := ('
                + format_code(condition, misc_args)[0]
                + ') ? success : failure;' + os.linesep
            )
            return

        delayed_statements = []
        for (node_name, argument_pairs, statement_type, statement) in statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            if statement_type == 'check':
                handle_condition(statement, nodes, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
            elif statement_type == 'return':
                handle_return_statement(statement, nodes, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
            else:
                if statement.variable_statement is not None:
                    handle_variable_assignment(statement.variable_statement, None, False, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
                elif statement.read_statement is not None:
                    handle_read_statement(statement.read_statement, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
                else:
                    delayed_statements += handle_write_statement(statement.write_statement, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        for (node_name, argument_pairs, statement) in delayed_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            handle_variable_assignment(statement, None, False, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        return

    def complete_environment_variables(model, pre_tick):
        '''
        completes the environment variables.
        -- arguments
        @ model := a model.
        @ variables := a dictionary of variables
        @ local_variables := a dictionary of local variables that will be used to create new variable
        @ delayed_statements := a list of statements that need to be processed now
        -- return
        no return
        -- side effects
        changes variables.
        '''
        for statement in model.update:
            if statement.instant == pre_tick:
                # things marked as instant happen before the tick. pre_tick means before the tick. This is called twice, once before and once after.
                handle_variable_assignment(statement, None, False, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))

    def get_behaverify_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage):
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
                return [variable_reference(atom.name, is_local(atom), misc_args['node_name'])] if atom_class == 'VARIABLE' else []
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
            used_variables.append(variable_reference(variable.name, is_local(variable), new_misc_args['node_name']))
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
            if array_mode:
                used_variables = []
                is_constant = statement.constant_index == 'constant_index'
                for loop_array_index in statement.assigns:
                    used_variables.extend(find_used_variables_without_formatting_in_loop_array_index((loop_array_index, is_constant), create_misc_args(loop_references = {}, node_name = node_name, use_stages = False, overwrite_stage = False, define_substitutions = None, specification_writing = False, specification_warning = False)))
                used_variables.extend(find_used_variables_without_formatting_in_assign(statement.default_value, create_misc_args(loop_references = {}, node_name = node_name, use_stages = False, overwrite_stage = False, define_substitutions = None, specification_writing = False, specification_warning = False)))
                return used_variables
            return find_used_variables_without_formatting_in_assign(statement.assign, create_misc_args(loop_references = {}, node_name = node_name, use_stages = False, overwrite_stage = False, define_substitutions = None, specification_writing = False, specification_warning = False))

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

        # create each variable type using the template.
        nonlocal behaverify_variables  # this is necessary right now because we need to be able to access already created variables during other variable initializations.
        # specifically, if we make var A, and then var B depends on var A, it will assume var A is in behaverify_variables
        var_key_to_obj = {variable_reference(variable.name, False, None) : variable for variable in model.variables if not is_local(variable)} if model.neural else None
        behaverify_variables = {
            variable_reference(variable.name, False, '') :
            (
                create_variable_template(variable.name, 'DEFINE', variable_array_size(variable, {}, {}, {}, constants, {}), None, None, None, [], True, True)
                if variable.model_as == 'NEURAL' else
                (
                    create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None, None, None, None, [], True, True)
                    if variable.model_as == 'DEFINE' else
                    create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None,
                                             (
                                                 {True, False}
                                                 if variable.domain.boolean is not None else
                                                 (
                                                     'integer'
                                                     if variable.domain.true_int is not None else
                                                     (
                                                         'real'
                                                         if variable.domain.true_real is not None else
                                                         (
                                                             None
                                                             if variable.domain.min_val is not None else
                                                             {val for domain_code in variable.domain.domain_codes for val in build_meta_func(domain_code)((constants, {}))}
                                                         )
                                                     )
                                                 )
                                             ),
                                             get_min_max(variable.domain.min_val, variable.domain.max_val, {}, {}, {}, constants, {}),
                                             None, [], keep_stage_0, keep_last_stage
                                             )
                )
            ) for variable in model.variables if not is_local(variable)
        }
        local_variable_templates = {
            variable.name :
            (
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None, None, None, None, [], True, True)
                if variable.model_as == 'DEFINE' else
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None,
                                         (
                                             {True, False}
                                             if variable.domain.boolean is not None else
                                             (
                                                 'integer'
                                                 if variable.domain.true_int is not None else
                                                 (
                                                     'real'
                                                     if variable.domain.true_real is not None else
                                                     (
                                                         None
                                                         if variable.domain.min_val is not None else
                                                         {val for domain_code in variable.domain.domain_codes for val in build_meta_func(domain_code)((constants, {}))}
                                                     )
                                                 )
                                             )
                                         ),
                                         get_min_max(variable.domain.min_val, variable.domain.max_val, {}, {}, {}, constants, {}),
                                         None, [], keep_stage_0, keep_last_stage
                                         )
            )
            for variable in model.variables if is_local(variable)
        }
        for variable in model.variables:
            var_key = variable_reference(variable.name, is_local(variable), '')
            if is_local(variable):
                continue  # this is handled below
            if variable.model_as == 'NEURAL':
                behaverify_variables[variable.name]['existing_definitions'] = {}
                depends_on = set()
                domain_values = set()
                input_order = []
                for input_code in variable.inputs:
                    input_func = build_meta_func(input_code)
                    variable_inputs = input_func((constants, {}))
                    for variable_input in variable_inputs:
                        (atom_class, atom) = resolve_potential_reference_no_type(variable_input, declared_enumerations, {}, variables, constants, {})
                        if atom_class == 'VARIABLE':
                            depends_on.add(variable_reference(atom.name, False, None))
                        input_order.append((atom_class, atom))
                behaverify_variables[var_key]['depends_on'] = tuple(sorted(list(depends_on)))
                define_substitutions = {
                    sub_key : 'SUBSTITUTE_' + str(index) + '_ME'
                    for (index, sub_key) in enumerate(behaverify_variables[var_key]['depends_on'])
                }
                define_substitutions[var_key] = 'SUBSTITUTE_SELF'
                list_of_list_of_inputs = create_possible_values(behaverify_variables[var_key]['depends_on'])
                file_prefix = model_file.rsplit('/', 1)[0]
                source_func = build_meta_func(variable.source)
                source_vals = source_func((constants, {}))
                source = source_vals[0]
                source = resolve_potential_reference_no_type(source, declared_enumerations, {}, variables, constants, {})[1]
                source = file_prefix + '/' + source
                session = onnxruntime.InferenceSession(source)
                input_name = session.get_inputs()[0].name
                cur_stage = []
                for index in range(behaverify_variables[var_key]['array_size']):
                    cur_stage.append((index, []))
                for list_of_inputs in list_of_list_of_inputs:
                    cur_ref = dict(list_of_inputs)
                    current_input = []
                    for (atom_class, atom) in input_order:
                        if atom_class == 'VARIABLE':
                            current_input.append(cur_ref[atom.name])
                        else:
                            current_input.append(atom)
                    current_outputs = session.run(None, {input_name : [current_input]})
                    condition = ' & '.join(['(' + define_substitutions[variable_reference(var_name, False, None)] + ' = ' + str(var_val) + ')' for (var_name, var_val) in list_of_inputs])
                    for index in range(len(current_outputs[0][0])):
                        output = int(current_outputs[0][0][index])
                        cur_stage[index][1].append((condition, str(output)))
                        domain_values.add(output)
                for index in range(behaverify_variables[var_key]['array_size']):
                    cur_stage[index][1].append(('TRUE', '66'))
                behaverify_variables[var_key]['initial_value'] = (None, True, {index : False for index in range(behaverify_variables[var_key]['array_size'])}, cur_stage)
                behaverify_variables[var_key]['custom_value_range'] = domain_values
                behaverify_variables[var_key]['default_array_val'] = (False, [('TRUE', '66')])
                continue  # don't do the other stuff for neural networks
            define_substitutions = None
            if variable.model_as == 'DEFINE':
                behaverify_variables[variable.name]['existing_definitions'] = {}
                behaverify_variables[var_key]['depends_on'] = tuple(sorted(list(set(find_used_variables_without_formatting_in_statement(variable, is_array(variable), None)))))
                define_substitutions = {
                    sub_key : 'SUBSTITUTE_' + str(index) + '_ME'
                    for (index, sub_key) in enumerate(behaverify_variables[var_key]['depends_on'])
                }
                define_substitutions[var_key] = 'SUBSTITUTE_SELF'
            behaverify_variables[var_key]['initial_value'] = handle_variable_statement(variable, None, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
            if is_array(variable):
                behaverify_variables[var_key]['default_array_val'] = handle_assign(variable.default_value, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
        # at this point we've finished everything that isn't a local variable.
        # create local variables.
        for (node_name, variable) in local_variables:
            var_key = variable_reference(variable.name, True, node_name)
            new_var = copy.deepcopy(local_variable_templates[variable.name])
            behaverify_variables[var_key] = new_var
            behaverify_variables[var_key]['name'] = var_key
            define_substitutions = None
            if variable.model_as == 'DEFINE':
                behaverify_variables[var_key]['existing_definitions'] = {}
                behaverify_variables[var_key]['depends_on'] = tuple(sorted(list(set(find_used_variables_without_formatting_in_statement(variable, is_array(variable), None)))))
                define_substitutions = {
                    sub_key : 'SUBSTITUTE_' + str(index) + '_ME'
                    for (index, sub_key) in enumerate(behaverify_variables[var_key]['depends_on'])
                }
                define_substitutions[var_key] = 'SUBSTITUTE_SELF'
            behaverify_variables[var_key]['initial_value'] = handle_variable_statement(variable, None, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
            if is_array(variable):
                behaverify_variables[var_key]['default_array_val'] = handle_assign(variable.default_value, create_misc_args(loop_references = {}, node_name = None, use_stages = True, overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
        # handle initial statements FOR DEFINE ONLY.
        # we have to parse and update this first. only after that can we go through non-define macros.
        # this is so we populate the definitions and what not.
        for (node_name, argument_pairs, initial_statement) in initial_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            assign_var = initial_statement.variable
            if assign_var.model_as == 'DEFINE':
                var_key = variable_reference(assign_var.name, is_local(assign_var), node_name)
                behaverify_variables[var_key]['existing_definitions'] = {}
                behaverify_variables[var_key]['depends_on'] = tuple(sorted(list(set(find_used_variables_without_formatting_in_statement(initial_statement, is_array(assign_var), node_name)))))
                define_substitutions = {
                    sub_key : 'SUBSTITUTE_' + str(index) + '_ME'
                    for (index, sub_key) in enumerate(behaverify_variables[var_key]['depends_on'])
                }
                define_substitutions[var_key] = 'SUBSTITUTE_SELF'
                behaverify_variables[var_key]['initial_value'] = handle_variable_statement(initial_statement, None, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
                if is_array(assign_var):
                    behaverify_variables[var_key]['default_array_val'] = handle_assign(initial_statement.default_value, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True,  overwrite_stage = None, define_substitutions = define_substitutions, specification_writing = False, specification_warning = False))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        # now we go through all the not define.
        for (node_name, argument_pairs, initial_statement) in initial_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            assign_var = initial_statement.variable
            if assign_var.model_as != 'DEFINE':
                var_key = variable_reference(assign_var.name, is_local(assign_var), node_name)
                behaverify_variables[var_key]['initial_value'] = handle_variable_statement(initial_statement, None, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
                if is_array(assign_var):
                    behaverify_variables[var_key]['default_array_val'] = handle_assign(initial_statement.default_value, create_misc_args(loop_references = {}, node_name = node_name, use_stages = True, overwrite_stage = None, define_substitutions = None, specification_writing = False, specification_warning = False))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        return behaverify_variables

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
                                              True, False, True)
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
                                              True, True, True)
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
        while True:
            if hasattr(current_node, 'sub_root'):
                current_node = current_node.sub_root
                continue
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
            break
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
        'if' : ('', format_function_if),
        'loop' : ('', format_function_loop),
        'abs' : ('abs', format_function_before),
        'max' : ('max', format_function_recursive_before),
        'min' : ('min', format_function_recursive_before),
        'sin' : ('sin', format_function_before),
        'cos' : ('cos', format_function_before),
        'tan' : ('tan', format_function_before),
        'ln' : ('ln', format_function_before),
        'not' : ('!', format_function_before),
        'and' : ('&', format_function_between),
        'or' : ('|', format_function_between),
        'xor' : ('xor', format_function_between),
        'xnor' : ('xnor', format_function_between),
        'implies' : ('->', format_function_between),
        'equivalent' : ('<->', format_function_between),
        'eq' : ('=', format_function_between),
        'neq' : ('!=', format_function_between),
        'lt' : ('<', format_function_between),
        'gt' : ('>', format_function_between),
        'lte' : ('<=', format_function_between),
        'gte' : ('>=', format_function_between),
        'neg' : ('-', format_function_before),
        'add' : ('+', format_function_between),
        'sub' : ('-', format_function_between),
        'mult' : ('*', format_function_between),
        'idiv' : ('/', format_function_integer_division),
        'mod' : ('mod', format_function_between),
        'rdiv' : ('/', format_function_between),
        'floor' : ('floor', format_function_before),
        'count' : ('count', format_function_before),
        'index' : ('index', format_function_index),
        'active' : ('.active', format_function_after),
        'success' : ('.status = success', format_function_after),
        'running' : ('.status = running', format_function_after),
        'failure' : ('.status = failure', format_function_after),
        'next' : ('X', format_function_before),
        'globally' : ('G', format_function_before),
        'globally_bounded' : ('G', format_function_before_bounded),
        'finally' : ('F', format_function_before),
        'finally_bounded' : ('F', format_function_before_bounded),
        'until' : ('U', format_function_between),
        'until_bounded' : ('U', format_function_between_bounded),
        'release' : ('V', format_function_between),
        'release_bounded' : ('V', format_function_between_bounded),
        'previous' : ('Y', format_function_before),
        'not_previous_not' : ('Z', format_function_before),
        'historically' : ('H', format_function_before),
        'historically_bounded' : ('H', format_function_before_bounded),
        'once' : ('O', format_function_before),
        'once_bounded' : ('O', format_function_before_bounded),
        'since' : ('S', format_function_between),
        'since_bounded' : ('S', format_function_between_bounded),
        'triggered' : ('T', format_function_between),
        'triggered_bounded' : ('T', format_function_between_bounded),
        'exists_globally' : ('EG', format_function_before),
        'exists_next' : ('EX', format_function_before),
        'exists_finally' : ('EF', format_function_before),
        'exists_until' : (('E', 'U'), format_function_before_between),
        'always_globally' : ('AG', format_function_before),
        'always_next' : ('AX', format_function_before),
        'always_finally' : ('AF', format_function_before),
        'always_until' : (('A', 'U'), format_function_before_between)
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

    if return_values:
        return (nodes, behaverify_variables)
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
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--keep_last_stage', action = 'store_true')
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    arg_parser.add_argument('--behave_only', action = 'store_true')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0)
    args = arg_parser.parse_args()
    dsl_to_nuxmv(args.metamodel_file, args.model_file, args.output_file, args.keep_stage_0, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False)
