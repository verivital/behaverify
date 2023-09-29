'''
This module is part of BehaVerify and used to convert .tree files to .smv files for use with nuXmv. It indexes arrays manually.


Author: Serena Serafina Serbinowska
Last Edit: 2023-09-29
'''
import argparse
import pprint
import os
import itertools
import copy
import textx
from behaverify_to_smv import write_smv
from serene_functions import build_meta_func
from check_model import validate_model

from behaverify_common import create_node_name, create_node_template, create_variable_template, indent, is_local, is_array, handle_constant_or_reference, handle_constant_or_reference_no_type, resolve_potential_reference_no_type, variable_array_size, get_min_max

# a NEXT_VALLUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE

def dsl_to_behaverify(metamodel_file, model_file, output_file, keep_stage_0, keep_last_stage, do_not_trim, behave_only):
    '''
    This method is used to convert the dsl to behaverify.
    '''

    def execute_loop(function_call, to_call, misc_args):
        new_misc_args = copy.deepcopy(misc_args)
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
                return_vals.extend(to_call(function_call.values[0], misc_args))
            loop_references.pop(function_call.loop_variable)
        return return_vals

    def format_function_if(_, function_call, misc_args):
        return [format_code(function_call.values[0], misc_args) + ' ? ' + format_code(function_call.values[1], misc_args) + ' : ' + format_code(function_call.values[2], misc_args)]

    def format_function_loop(_, function_call, misc_args):
        return execute_loop(function_call, format_code, misc_args)

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
        return [
            '('
            + (' ' + function_name + ' [' + str(min_val) + ', ' + str(max_val) + '] ').join(formatted_values)
            + ')'
        ]

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
            # + 'TRUE : ' + formatted_variable + '_index_0; '
            + 'esac)'
        )

    def format_function_index(_, function_call, misc_args):
        '''variable[val]'''
        # return (
        #     format_variable(function_call.variable, misc_args) + '[' + format_code(function_call.values[0], misc_args) + ']'
        # )
        var_func = build_meta_func(function_call.to_index)
        variable = resolve_potential_reference_no_type(var_func((constants, misc_args['loop_references']))[0], declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
        new_misc_args = adjust_args(function_call, misc_args)
        formatted_variable = format_variable(variable, new_misc_args)
        index_expression = format_code(function_call.values[0], new_misc_args)
        return [case_index(formatted_variable, variable_array_size(variable, declared_enumerations, nodes, variables, constants, misc_args['loop_references']), index_expression)]

    def format_function(function_call, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.'''
        (function_name, function_to_call) = function_format[function_call.function_name]
        return function_to_call(function_name, function_call, misc_args)

    def create_misc_args(loop_references, node_name, use_stages, use_next, not_next, overwrite_stage, specification_writing, specification_warning):
        '''
        -- ARGUMENTS
        @ node_name := the name of the node which caused this to be called. used for formatting local variables.
        @ use_stages := are we using stages for this? (note: does not affect variable renaming).
        @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
        @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        return {
            'loop_references' : loop_references,
            'node_name' : node_name,
            'use_stages' : use_stages,
            'use_next' : use_next,
            'not_next' : not_next,
            'overwrite_stage' : overwrite_stage,
            'trace_num' : 1,
            'specification_writing' : specification_writing,
            'specification_warning' : specification_warning
        }

    def compute_stage(variable_key, misc_args):
        '''
        compute the stage for the variable now
        -- GLOBALS
        @ variables := a dictionary of variables
        -- arguments
        @ variable_key := used to index into the variable.
        @ use_stages := if true, use stages
        @ overwrite_stage := forces a specific stage
        -- return
        @ the string with appropriate stage number
        -- side effects
        none.
        '''
        variable = behaverify_variables[variable_key]
        overwrite_stage = misc_args['overwrite_stage']
        return (
            (
                (len(variable['next_value']) - 1)
                if variable['mode'] == 'DEFINE'
                else
                len(variable['next_value'])
            )
            if overwrite_stage is None or overwrite_stage < 0
            else
            min(overwrite_stage, len(variable['next_value']))
        )

    def find_used_variables(code, misc_args):
        '''Returns the list of used variables (will also format them)'''
        if code.atom is not None:
            (atom_class, atom) = handle_constant_or_reference_no_type(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
            return [format_variable(atom, adjust_args(code, misc_args))] if atom_class == 'VARIABLE' else []
        if code.code_statement is not None:
            return find_used_variables(code.code_statement, misc_args)
        function_call = code.function_call
        if function_call.function_name == 'loop':
            return execute_loop(function_call, find_used_variables, misc_args)
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

    def assemble_variable(name, stage, use_next, trace_num, specification_writing):
        '''
        This method should only be called by format variable.
        '''
        return (
            ('' if not use_next else 'next(')
            + (('system' + (('_' + str(trace_num)) if hyper_mode else '') + '.') if specification_writing else '')
            + name
            + '_stage_' + str(stage)
            + ('' if not use_next else ')'))

    def format_variable(variable_obj, misc_args):
        '''
        -- GLOBALS
        @ variables := a dict of all variables
        -- ARGUMENTS
        @ variable_obj := a textx object of a variable that we will be formatting.
        @ node_name := the name of the node which caused this to be called.
        @ use_stages := are we using stages for this?
        @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
        @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        variable_key = variable_reference(variable_obj.name, is_local(variable_obj), misc_args['node_name'])
        variable = behaverify_variables[variable_key]
        return format_variable_non_object(variable, variable_key, misc_args)

    def format_variable_non_object(variable, variable_key, misc_args):
        loop_references = misc_args['loop_references']
        node_name = misc_args['node_name']
        use_stages = misc_args['use_stages']
        use_next = misc_args['use_next']
        not_next = misc_args['not_next']
        overwrite_stage = misc_args['overwrite_stage']
        trace_num = misc_args['trace_num']
        specification_writing = misc_args['specification_writing']
        specification_warning = misc_args['specification_warning']

        if variable['mode'] == 'DEFINE':
            if overwrite_stage is not None and len(variable['next_value']) > 0:
                return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), use_next, trace_num, specification_writing)
            used_vars = tuple(map(lambda dependent_variable_key: format_variable_non_object(behaverify_variables[dependent_variable_key], dependent_variable_key, misc_args), variable['depends_on']))
            if used_vars not in variable['existing_definitions']:
                variable['existing_definitions'][used_vars] = len(variable['next_value'])
                variable['next_value'].append(handle_variable_statement(variable['initial_value'], variable['initial_value'], None, create_misc_args(copy.deepcopy(loop_references), node_name, use_stages, use_next, not_next, overwrite_stage, False, specification_warning)))
            stage = variable['existing_definitions'][used_vars]
            return assemble_variable(variable['name'], stage, use_next, trace_num, specification_writing)

        if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
            if specification_warning and not variable['keep_stage_0']:
                print('A specification is preventing the removal of stage 0 for: ' + variable['name'])
            variable['keep_stage_0'] = True
        if use_stages and (overwrite_stage is None or overwrite_stage < 0 or overwrite_stage == len(variable['next_value'])):
            # we don't need to subtract one from len of next_value because we have one stage not represented in next_value.
            if specification_warning and not variable['keep_last_stage']:
                print('A specification is preventing the removal of last stage for: ' + variable['name'])
            variable['keep_last_stage'] = True
        if use_next and variable_key == not_next:
            return (('system' + (('_' + str(trace_num)) if hyper_mode else '') + '.') if specification_writing else '') + 'LINK_TO_PREVIOUS_FINAL_' + variable['name']
        return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), use_next, trace_num, specification_writing)

    def adjust_args(code, misc_args):
        '''
        creates a new arg based on the old one, but modifies it. should only be used by format_code
        Declared not as nested function cuz that would tank performance.
        '''
        new_misc_args = copy.deepcopy(misc_args)
        if code.node_name is not None:
            node_name_func = build_meta_func(code.node_name)
            new_misc_args['node_name'] = resolve_potential_reference_no_type(node_name_func((constants, new_misc_args['loop_references'])), declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])
        if code.read_at is not None:
            read_at_func = build_meta_func(code.read_at)
            new_misc_args['overwrite_stage'] = resolve_potential_reference_no_type(read_at_func((constants, new_misc_args['loop_references'])), declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])
        if code.trace_num is not None:
            trace_num_func = build_meta_func(code.trace_num)
            new_misc_args['trace_num'] = resolve_potential_reference_no_type(trace_num_func((constants, new_misc_args['loop_references'])), declared_enumerations, nodes, variables, constants, new_misc_args['loop_references'])
        return new_misc_args

    def handle_atom(code, misc_args):
        (atom_class, atom_type, atom) = handle_constant_or_reference(code.atom, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        return (str(atom).upper() if atom_type == 'BOOLEAN' else str(atom)) if atom_class == 'CONSTANT' else (format_variable(atom, adjust_args(code, misc_args)))

    def format_code(code, misc_args):
        '''
        format a code fragment
        '''
        return (
            [handle_atom(code, misc_args)] if code.atom is not None else (
                ['(' + format_code(code.code_statement, misc_args) + ')'] if code.code_statement is not None else (
                    format_function(code, misc_args)
                )
            )
        )

    def handle_result(result, misc_args):
        '''
        should only be called by handle_assign
        '''
        vals = []
        for value in result.values:
            vals.extend(format_code(value, misc_args))
        non_determinism = len(vals) > 1
        return (non_determinism, ('{' + ', '.join(vals) + '}') if non_determinism else vals[0])

    def handle_assign(assign, stage, misc_args):
        '''
        should only be called by handle_variable_statement
        '''
        case_results = assign.case_results
        default_result = assign.default_result
        non_determinism = False
        for case_result in case_results:
            (new_non_det, stage_part) = handle_result(case_result, misc_args)
            non_determinism = non_determinism or new_non_det
            stage.append((format_code(case_result.condition, misc_args), stage_part))
        (new_non_det, stage_part) = handle_result(default_result, misc_args)
        non_determinism = non_determinism or new_non_det
        stage.append(('TRUE', stage_part))
        return (non_determinism, stage)

    def handle_array_default(statement):
        default_func = build_meta_func(statement.default_value)
        return str(resolve_potential_reference_no_type(default_func((constants, {}))[0], declared_enumerations, nodes, variables, constants, {})[1])

    def handle_array_constant_index(statement, assign_var, condition, misc_args):
        non_determinism = {}
        stage = []
        formatted_variable = format_variable(assign_var, misc_args) + '_index_'
        for index_assign in statement.assigns:
            index_func = build_meta_func(index_assign.index_expr)
            (cur_non_determinism, cur_stage) = handle_assign(index_assign.assign, [] if condition is None else ['replace'], misc_args)
            for index in index_func((constants, misc_args['loop_references'])):
                new_index = resolve_potential_reference_no_type(index, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
                non_determinism[new_index] = cur_non_determinism
                if condition is not None:
                    cur_stage[0] = [(condition, formatted_variable + str(new_index))]
                stage.append((new_index, cur_stage))
        return (misc_args['node_name'], True, non_determinism, stage)

    def handle_array_unknown_index(statement, assign_var, condition, misc_args):
        non_determinism = False
        stage = []
        formatted_variable = format_variable(assign_var, misc_args)
        array_size = -1 if condition is None else variable_array_size(assign_var, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])
        for index_assign in statement.assigns:
            index_func = build_meta_func(index_assign.index_expr)
            (cur_non_determinism, cur_stage) = handle_assign(index_assign.assign, [] if condition is None else ['replace'], misc_args)
            for index in index_func((constants, misc_args['loop_references'])):
                new_index = resolve_potential_reference_no_type(index, declared_enumerations, nodes, variables, constants, misc_args['loop_references'])[1]
                non_determinism = non_determinism or cur_non_determinism
                if condition is not None:
                    cur_stage[0] = [(condition, case_index(formatted_variable + str(new_index), array_size, str(new_index)))]
                stage.append((str(new_index), cur_stage))
        return(misc_args['node_name'], False, non_determinism, stage)

    def handle_variable_statement(statement, assign_var, condition, misc_args):
        '''
        should only be called if init_mode is true or from variable_assignment
        '''
        if is_array(assign_var):
            return (
                handle_array_constant_index(statement, assign_var, condition, misc_args)
                if statement.constant_index == 'constant_index' else
                handle_array_unknown_index(statement, assign_var, condition, misc_args)
            )
        (non_determinism, stage) = handle_assign(statement.assign, [] if condition is None else [(condition, format_variable(assign_var, misc_args))], misc_args)
        return (misc_args['node_name'], non_determinism, stage)

    def handle_variable_assignment(statement, assign_var, condition, read_statement_assign_condition, misc_args):
        '''
        this handles variable assignment
        this should be called if you have a variable assignment and it is not initial
        if you have an initial variable value, call handle_variable_statement
        We keep this seperate so we can track stage removal.
        '''

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
                                  [(index, [(format_code(statement.condition, misc_args), '{TRUE, FALSE}' if non_determinism else 'TRUE'), ('TRUE', 'FALSE')])])
                else:
                    index = format_code(statement.index_of, misc_args)
                    next_value = (misc_args['node_name'], False, non_determinism,
                                  [(index, [(format_code(statement.condition, misc_args), '{TRUE, FALSE}' if non_determinism else 'TRUE'), ('TRUE', 'FALSE')])])
        else:
            next_value = handle_variable_statement(statement, assign_var, condition, misc_args)
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
        return

    def handle_specifications(specifications):
        '''this handles specifications'''
        return [
            (
                specification.spec_type
                + ' '
                + format_code(specification.code_statement, create_misc_args({}, None, True, False, None, None, True, True))
                + ';'
            )
            for specification in specifications
        ]

    def variable_reference(base_name, _is_local_, node_name):
        return ((node_name + '_DOT_' + base_name) if _is_local_ else base_name)

    def resolve_statements(statements, nodes):
        def handle_read_statement(statement, misc_args):
            if statement.condition_variable is not None:
                index = handle_variable_assignment(statement, statement.condition_variable, None, True, misc_args)
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
                condition = '!(' + format_code(statement.condition, misc_args) + ')'
            for variable_statement in statement.variable_statements:
                handle_variable_assignment(variable_statement, variable_statement.variable, condition, False, misc_args)
            return

        def handle_write_statement(statement, misc_args):
            delayed = []
            for var_update in statement.update:
                if var_update.instant:
                    handle_variable_assignment(var_update, var_update.variable, None, False, misc_args)
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
                                  + format_code(case_result.condition, misc_args)
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
                + format_code(condition, misc_args)
                + ') ? success : failure;' + os.linesep
            )
            return

        delayed_statements = []
        for (node_name, argument_pairs, statement_type, statement) in statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            if statement_type == 'check':
                handle_condition(statement, nodes, create_misc_args({}, node_name, True, False, None, None, False, False))
            elif statement_type == 'return':
                handle_return_statement(statement, nodes, create_misc_args({}, node_name, True, False, None, None, False, False))
            else:
                if statement.variable_statement is not None:
                    handle_variable_assignment(statement.variable_statement, statement.variable_statement.variable, None, False, create_misc_args({}, node_name, True, False, None, None, False, False))
                elif statement.read_statement is not None:
                    handle_read_statement(statement.read_statement, create_misc_args({}, node_name, True, False, None, None, False, False))
                else:
                    delayed_statements += handle_write_statement(statement.write_statement, create_misc_args({}, node_name, True, False, None, None, False, False))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        for (node_name, argument_pairs, statement) in delayed_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            handle_variable_assignment(statement, statement.variable, None, False, create_misc_args({}, node_name, True, False, None, None, False, False))
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
                # things marked as instant happen before the tick.
                # pre_tick means before the tick.
                handle_variable_assignment(statement, statement.variable, None, False, create_misc_args({}, None, True, False, None, None, False, False))

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
                return execute_loop(function_call, find_used_variables_without_formatting_in_code, misc_args)
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

        def find_used_variables_without_formatting_in_assign(assign, node_name):
            used_variables = []
            for case_result in assign.case_results:
                used_variables.extend(find_used_variables_without_formatting_in_code(case_result.condition, create_misc_args({}, node_name, False, False, False, False, False, False)))
                for value in case_result.values:
                    used_variables.extend(find_used_variables_without_formatting_in_code(value, create_misc_args({}, node_name, False, False, False, False, False, False)))
            return used_variables

        def find_used_variables_without_formatting_in_statement(statement, array_mode, node_name):
            if array_mode:
                used_variables = []
                if statement.constant_index == 'constant_index':
                    for index_assign in statement.assigns:
                        used_variables.extend(find_used_variables_without_formatting_in_assign(index_assign.assign, node_name))
                else:
                    for index_assign in statement.assigns:
                        for index in index_assign.index_expr:
                            used_variables.extend(find_used_variables_without_formatting_in_code(index, create_misc_args({}, node_name, False, False, False, False, False, False)))
                        used_variables.extend(find_used_variables_without_formatting_in_assign(index_assign.assign, node_name))
                return used_variables
            return find_used_variables_without_formatting_in_assign(statement.assign, node_name)

        # create each variable type using the template.
        nonlocal behaverify_variables  # this is necessary right now because we need to be able to access already created variables during other variable initializations.
        # specifically, if we make var A, and then var B depends on var A, it will assume var A is in behaverify_variables
        behaverify_variables = {
            variable_reference(variable.name, False, '') :
            (
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None, None, (0, 0), None, [], True, True)
                if variable.model_as == 'DEFINE' else
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None,
                                         (
                                             '{TRUE, FALSE}'
                                             if variable.domain.boolean is not None else
                                             (
                                                 'integer'
                                                 if variable.domain.true_int is not None else
                                                 (
                                                     'real'
                                                     if variable.domain.true_real is not None else
                                                     (
                                                         None
                                                         if variable.domain.min_val is None else
                                                         (
                                                             '{'
                                                             + ', '.join([''.join(map(str, build_meta_func(domain_code)((constants, {})))) for domain_code in variable.domain.domain_codes])
                                                             + '}'
                                                         )
                                                     )
                                                 )
                                             )
                                         ),
                                         get_min_max(variable.domain.min_val, variable.domain.max_val, {}, {}, {}, constants, {}),
                                         None, [], keep_stage_0, keep_last_stage
                                         )
            ) for variable in model.variables if not is_local(variable)
        }
        local_variable_templates = {
            variable.name :
            (
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None, None, (0, 0), None, [], True, True)
                if variable.model_as == 'DEFINE' else
                create_variable_template(variable.name, variable.model_as, variable_array_size(variable, {}, {}, {}, constants, {}) if is_array(variable) else None,
                                         (
                                             '{TRUE, FALSE}'
                                             if variable.domain.boolean is not None else
                                             (
                                                 'integer'
                                                 if variable.domain.true_int is not None else
                                                 (
                                                     'real'
                                                     if variable.domain.true_real is not None else
                                                     (
                                                         None
                                                         if variable.domain.min_val is None else
                                                         (
                                                             '{'
                                                             + ', '.join([''.join(map(str, build_meta_func(domain_code)((constants, {})))) for domain_code in variable.domain.domain_codes])
                                                             + '}'
                                                         )
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
            if is_array(variable):
                if is_local(variable):
                    local_variable_templates[variable.name]['default_array_val'] = handle_array_default(variable)
                else:
                    behaverify_variables[var_key]['default_array_val'] = handle_array_default(variable)
            if variable.model_as == 'DEFINE':
                local_variable_templates[variable.name]['existing_definitions'] = {}
                local_variable_templates[variable.name]['initial_value'] = variable
                if is_local(variable):
                    local_variable_templates[variable.name]['depends_on'] = None
                else:
                    behaverify_variables[var_key]['depends_on'] = tuple(sorted(list(set(find_used_variables_without_formatting_in_statement(variable, is_array(variable), None)))))
            else:
                if is_local(variable):
                    local_variable_templates[variable.name]['initial_value'] = handle_variable_statement(variable, variable, None, create_misc_args({}, None, False, False, None, None, False, False))
                else:
                    behaverify_variables[var_key]['initial_value'] = handle_variable_statement(variable, variable, None, create_misc_args({}, None, False, False, None, None, False, False))

        # create local variables.
        for (node_name, variable) in local_variables:
            new_name = variable_reference(variable.name, True, node_name)
            new_var = copy.deepcopy(local_variable_templates[variable.name])
            new_var['name'] = new_name
            if variable.model_as == 'DEFINE':
                new_var['depends_on'] = tuple(sorted(list(set(find_used_variables_without_formatting_in_statement(variable, is_array(variable), None)))))
            behaverify_variables[new_name] = new_var

        # handle initial statements FOR DEFINE ONLY.
        # we have to parse and update this first. only after that can we go through non-define macros.
        # this is so we populate the definitions and what not.
        for (node_name, argument_pairs, initial_statement) in initial_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            assign_var = initial_statement.variable
            if assign_var.model_as == 'DEFINE':
                # variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = handle_variable_statement(initial_statement, assign_var, None, create_misc_args(node_name, False, False, None, None))
                behaverify_variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = initial_statement
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        for (node_name, argument_pairs, initial_statement) in initial_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            assign_var = initial_statement.variable
            if assign_var.model_as != 'DEFINE':
                behaverify_variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = handle_variable_statement(initial_statement, assign_var, None, create_misc_args({}, node_name, False, False, None, None, False, False))
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
        while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
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
            else:
                current_node = current_node.sub_root
        # the above deals with sub_trees and leaf nodes, ensuring that the current_node variable has the next actual node at this point
        # next, we get the name of this node, and correct for duplication

        new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
        node_name = new_name[0]
        modifier = new_name[1]
        return (
            create_node[current_node.node_type](current_node, node_name, modifier, node_names, node_names_map, parent_name)
            if argument_pairs is None
            else
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
        'imply' : ('->', format_function_between),
        'equiv' : ('<->', format_function_between),
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

    metamodel = textx.metamodel_from_file(metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(model_file)
    hyper_mode = model.hypersafety
    use_reals = model.use_reals
    # specification_writing = False  # this is used to track whether or not code should make references to the trace and system or not.
    # serene_index = []
    behaverify_variables = {}
    # spec_warn = False
    (variables, constants, declared_enumerations) = validate_model(model)

    (_, _, _, nodes, local_variables, initial_statements, statements) = walk_tree(model.root)
    print('finished tree walk')

    behaverify_variables = {} # here to make sure the variable is in the namespace.
    behaverify_variables = get_behaverify_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage)
    print('finished variables')
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, create_misc_args({}, None, True, False, None, None, False, False))
    complete_environment_variables(model, True)
    print('completed environment variables, part 1')
    resolve_statements(statements, nodes)
    print('resolved_statements')
    complete_environment_variables(model, False)
    print('completed environment variables, part 2')
    # specification_writing = True
    # spec_warn = True
    specifications = handle_specifications(model.specifications)
    # spec_warn = False

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
    arg_parser.add_argument('output_file', default = None)
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--keep_last_stage', action = 'store_true')
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    arg_parser.add_argument('--behave_only', action = 'store_true')
    args = arg_parser.parse_args()
    dsl_to_behaverify(args.metamodel_file, args.model_file, args.output_file, args.keep_stage_0, args.keep_last_stage, args.do_not_trim, args.behave_only)
