'''
This module is part of BehaVerify and used to convert .tree files to .smv files for use with nuXmv.


Author: Serena Serafina Serbinowska
Created: 2022-01-01 (Date not correct)
Last Edit: 2023-08-11
'''
import argparse
import pprint
import os
import itertools
import copy
import textx
from behaverify_to_smv import write_smv
from check_model import (validate_model,
                         variable_type,
                         is_local,
                         is_array,
                         build_range_func)

from behaverify_common import create_node_name, create_node_template, create_variable_template, indent

# a NEXT_VALLUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE

def dsl_to_behaverify(metamodel_file, model_file, keep_stage_0, keep_last_stage, output_file, do_not_trim, behave_only):
    '''
    This method is used to convert the dsl to behaverify.
    '''

    def format_function_before(function_name, code, misc_args):
        '''function_name(vals)'''
        return (
            function_name + '('
            + ', '.join([format_code(value, misc_args) for value in code.function_call.values])
            + ')'
            )

    def format_function_between(function_name, code, misc_args):
        '''(vals function_name vals)'''
        return (
            '('
            + (' ' + function_name + ' ').join([format_code(value, misc_args) for value in code.function_call.values])
            + ')'
            )

    def format_function_after(function_name, code, _):
        '''(node_name.function_name)'''
        return (
            '('
            + code.function_call.node_name
            + function_name
            + ')'
            )

    def format_function_before_bounded(function_name, code, misc_args):
        '''function_name [min, max] (vals)'''
        return (
            function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] '  '('
            + ', '.join([format_code(value, misc_args) for value in code.function_call.values])
            + ')'
            )

    def format_function_between_bounded(function_name, code, misc_args):
        ''' honestly not sure '''
        return (
            '('
            + (' ' + function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] ').join([format_code(value, misc_args) for value in code.function_call.values])
            + ')'
            )

    def format_function_before_between(function_name, code, misc_args):
        '''probably some spec thing'''
        return (
            function_name[0] + '['
            + (' ' + function_name[1] + ' ').join([format_code(value, misc_args) for value in code.function_call.values])
            + ']'
            )

    def format_function_index(_, code, misc_args):
        '''variable[val]'''
        return (
            format_variable(code.function_call.variable, misc_args) + '[' + format_code(code.function_call.values[0], misc_args) + ']'
        )

    def format_function(code, misc_args):
        '''this just calls the other format functions. moved here to make format_code less cluttered.'''
        (function_name, function_to_call) = function_format[code.function_call.function_name]
        return function_to_call(function_name, code, misc_args)

    def create_misc_args(node_name, use_stages, use_next, not_next, overwrite_stage):
        '''
        -- ARGUMENTS
        @ node_name := the name of the node which caused this to be called. used for formatting local variables.
        @ use_stages := are we using stages for this? (note: does not affect variable renaming).
        @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
        @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
        @ overwrite_stage := overwrite which stage we're asking for.
        '''
        return {
            'node_name' : node_name,
            'use_stages' : use_stages,
            'use_next' : use_next,
            'not_next' : not_next,
            'overwrite_stage' : overwrite_stage,
            'trace_num' : '1'
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
        variable = variables[variable_key]
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
        # return (
        #     '_stage_'
        #     + str(
        #         len(variable['next_value'])
        #         if overwrite_stage is None or overwrite_stage < 0
        #         else
        #         min(overwrite_stage, len(variable['next_value']))
        #     )
        # )

    def find_used_variables(code, misc_args):
        '''Returns the list of used variables (will also format them)'''
        return (
            [] if code.constant is not None else (
                [format_variable(code.variable, misc_args)] if code.variable is not None else (
                    find_used_variables(code.code_statement, misc_args) if code.code_statement is not None else (
                        [variable for value in code.function_call.values for variable in find_used_variables(value, misc_args)]
                        +
                        ([format_variable(code.function_call.variable, misc_args)] if code.function_call.function_name == 'index' else [])
                    )
                )
            )
        )

    def assemble_variable(name, stage, use_next, trace_num):
        '''
        This method should only be called by format variable.
        '''
        return (
            ('' if not use_next else 'next(')
            + (('system' + (('_' + trace_num) if hyper_mode else '') + '.') if specification_writing else '')
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

        node_name = misc_args['node_name']
        use_stages = misc_args['use_stages']
        use_next = misc_args['use_next']
        not_next = misc_args['not_next']
        overwrite_stage = misc_args['overwrite_stage']
        trace_num = misc_args['trace_num']

        variable_key = variable_reference(variable_obj.name, is_local(variable_obj), node_name)
        variable = variables[variable_key]

        if variable['mode'] == 'DEFINE':
            nonlocal specification_writing
            if overwrite_stage is not None and len(variable['next_value']) > 0:
                return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), use_next, trace_num)
            restore_specification_writing = specification_writing
            specification_writing = False
            used_vars = []
            var_statement = variable['initial_value']
            var_assigns = var_statement.assigns
            var_assign = var_statement.assign
            var_array_mode = var_statement.array_mode
            if is_array(variable_obj) and var_array_mode != 'range':
                for assign in var_assigns:
                    if assign.default_result.range_mode != 'range':
                        for code_fragment in assign.default_result.values:
                            used_vars += find_used_variables(code_fragment, misc_args)
                    for case_result in assign.case_results:
                        if case_result.range_mode != 'range':
                            for code_fragment in case_result.values:
                                used_vars += find_used_variables(code_fragment, misc_args)
                        used_vars += find_used_variables(case_result.condition, misc_args)
            else:
                if var_assign.default_result.range_mode != 'range':
                    for code_fragment in var_assign.default_result.values:
                        used_vars += find_used_variables(code_fragment, misc_args)
                for case_result in var_assign.case_results:
                    if case_result.range_mode != 'range':
                        for code_fragment in case_result.values:
                            used_vars += find_used_variables(code_fragment, misc_args)
                    used_vars += find_used_variables(case_result.condition, misc_args)
            used_vars = tuple(sorted(list(set(used_vars))))
            if used_vars not in variable['existing_definitions']:
                variable['existing_definitions'][used_vars] = len(variable['next_value'])
                variable['next_value'].append(handle_variable_statement(var_statement, variable_obj, None, misc_args))
            stage = variable['existing_definitions'][used_vars]
            specification_writing = restore_specification_writing
            return assemble_variable(variable['name'], stage, use_next, trace_num)

        if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
            if spec_warn and not variable['keep_stage_0']:
                print('A specification is preventing the removal of stage 0 for: ' + variable['name'])
            variable['keep_stage_0'] = True
        if use_stages and (overwrite_stage is None or overwrite_stage < 0 or overwrite_stage == len(variable['next_value'])):
            # we don't need to subtract one from len of next_value because we have one stage not represented in next_value.
            if spec_warn and not variable['keep_last_stage']:
                print('A specification is preventing the removal of last stage for: ' + variable['name'])
            variable['keep_last_stage'] = True
        if use_next and variable_key == not_next:
            return (('system' + (('_' + trace_num) if hyper_mode else '') + '.') if specification_writing else '') + 'LINK_TO_PREVIOUS_FINAL_' + variable['name']
        return assemble_variable(variable['name'], compute_stage(variable_key, misc_args), use_next, trace_num)

    def adjust_args(code, misc_args):
        '''
        creates a new arg based on the old one, but modifies it. should only be used by format_code
        Declared not as nested function cuz that would tank performance.
        '''
        new_misc_args = copy.deepcopy(misc_args)
        new_misc_args['node_name'] = new_misc_args['node_name'] if code.node_name is None else code.node_name
        new_misc_args['overwrite_stage'] = new_misc_args['overwrite_stage'] if code.read_at is None else code.read_at
        new_misc_args['trace_num'] = new_misc_args['trace_num'] if code.trace_num is None else str(handle_constant(code.trace_num))
        return new_misc_args

    def format_code(code, misc_args):
        '''
        format a code fragment
        '''
        return (
            (str(code.constant).upper() if isinstance(code.constant, bool) else str(handle_constant(code.constant))) if code.constant is not None else (
                format_variable(code.variable, adjust_args(code, misc_args)) if code.variable is not None else (
                    ('(' + format_code(code.code_statement, misc_args) + ')') if code.code_statement is not None else (
                        format_function(code, misc_args)
                    )
                )
            )
        )

    def handle_result(result, misc_args):
        '''
        should only be called by handle_assign
        '''
        if result.range_mode == 'range':
            cond_func = build_range_func(result.values[2], constants)
            min_val = handle_constant(result.values[0])
            max_val = handle_constant(result.values[1])
            vals = list(map(str, filter(cond_func, range(min_val, max_val + 1))))
        else:
            vals = [
                format_code(value, misc_args)
                for value in result.values
            ]
        non_determinism = len(vals) > 1
        return (non_determinism, ('{' + ', '.join(vals) + '}') if non_determinism else vals[0])

    def handle_assign(assign, misc_args):
        '''
        should only be called by handle_variable_statement
        '''
        case_results = assign.case_results
        default_result = assign.default_result
        stage = []
        non_determinism = False
        for case_result in case_results:
            (new_non_det, stage_part) = handle_result(case_result, misc_args)
            non_determinism = non_determinism or new_non_det
            stage.append((format_code(case_result.condition, misc_args), stage_part))
        (new_non_det, stage_part) = handle_result(default_result, misc_args)
        non_determinism = non_determinism or new_non_det
        stage.append(('TRUE', stage_part))
        return (non_determinism, stage)

    def handle_variable_statement(statement, assign_var, condition, misc_args):
        '''
        should only be called if init_mode is true or from variable_assignment
        '''

        node_name = misc_args['node_name']
        init_mode = not textx.textx_isinstance(statement, metamodel['variable_statement'])
        constant_index = init_mode or statement.constant_index == 'constant_index'

        if is_array(assign_var):
            stage = []

            if constant_index:
                non_determinism = {}
            else:
                non_determinism = False

            if statement.array_mode == 'range':
                serene_indices = []
                if init_mode or len(statement.values) == 0:
                    serene_indices = list(range(handle_constant(assign_var.array_size)))
                else:
                    cond_func = build_range_func(statement.values[2], constants)
                    min_val = handle_constant(statement.values[0])
                    max_val = handle_constant(statement.values[1])
                    serene_indices = list(filter(cond_func, range(min_val, max_val + 1)))
                for index in serene_indices:
                    # constants['serene_index'] = index
                    serene_index.append(index)
                    cur_index = (
                        index
                        if init_mode
                        else
                        (
                            handle_constant(statement.assign.index_expr)
                            if constant_index
                            else
                            format_code(statement.assign.index_expr, misc_args)
                        )
                    )
                    (cur_non_determinism, cur_stage) = handle_assign(statement.assign if init_mode else statement.assign.assign, misc_args)
                    if condition is not None:
                        cur_stage = [(condition, format_variable(assign_var, misc_args) + '[' + str(cur_index) + ']')] + cur_stage
                    stage.append((cur_index, cur_stage))
                    if constant_index:
                        non_determinism[cur_index] = cur_non_determinism
                    else:
                        non_determinism = non_determinism or cur_non_determinism
                    serene_index.pop()
                # constants.pop('serene_index')
            else:
                for index, assign in enumerate(statement.assigns):
                    cur_index = (
                        index
                        if init_mode
                        else
                        (
                            handle_constant(assign.index_expr)
                            if constant_index
                            else
                            format_code(assign.index_expr, misc_args)
                        )
                    )
                    (cur_non_determinism, cur_stage) = handle_assign(assign if init_mode else assign.assign, misc_args)
                    if condition is not None:
                        cur_stage = [(condition, format_variable(assign_var, misc_args) + '[' + str(cur_index) + ']')] + cur_stage
                    stage.append((cur_index, cur_stage))
                    if constant_index:
                        non_determinism[cur_index] = cur_non_determinism
                    else:
                        non_determinism = non_determinism or cur_non_determinism
            return (node_name, True if init_mode else constant_index, non_determinism, stage)
        else:
            (non_determinism, stage) = handle_assign(statement.assign, misc_args)
            if condition is not None:
                stage = [(condition, format_variable(assign_var, misc_args))] + stage
            return (node_name, non_determinism, stage)
        return

    def handle_variable_assignment(statement, assign_var, condition, misc_args):
        '''
        this handles variable assignment
        this should be called if you have a variable assignment and it is not initial
        if you have an initial variable value, call handle_variable_statement
        '''

        node_name = misc_args['node_name']

        variable_key = variable_reference(assign_var.name, is_local(assign_var), node_name)
        variable = variables[variable_key]
        keep_stage_0 = variable['keep_stage_0']
        # keep_last_stage = variable['keep_last_stage']
        # we don't need to track keep_last_stage here, because we're going to reset the value after adding a new stage anyways. see below.
        if textx.textx_isinstance(statement, metamodel['read_statement']):
            non_determinism = statement.non_determinism
            if is_array(assign_var):
                the_index = handle_constant(statement.index_of) if statement.is_const == 'constant_index_of' else format_code(statement.index_of, misc_args)
                next_value = (
                    node_name, True, {the_index : non_determinism} if statement.is_const == 'constant_index_of' else non_determinism,
                    [
                        (
                            the_index
                            ,
                            (
                                [(format_code(statement.condition, misc_args), '{TRUE, FALSE}'), ('TRUE', 'FALSE')]
                                if non_determinism
                                else
                                [(format_code(statement.condition, misc_args), 'TRUE'), ('TRUE', 'FALSE')]
                            )
                        )
                    ]
                )
            else:
                next_value = (
                    node_name, non_determinism,
                    (
                        [(format_code(statement.condition, misc_args), '{TRUE, FALSE}'), ('TRUE', 'FALSE')]
                        if non_determinism
                        else
                        [(format_code(statement.condition, misc_args), 'TRUE'), ('TRUE', 'FALSE')]
                    )
                )
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
        return

    def handle_specifications(specifications):
        '''this handles specifications'''
        return [
            (
                specification.spec_type
                + ' '
                + format_code(specification.code_statement, create_misc_args(None, True, False, None, None))
                + ';'
            )
            for specification in specifications
        ]

    def handle_constant(constant):
        '''this handles a constant by checking if it is in constants and replacing if appropriate'''
        if constant == 'serene_index':
            return serene_index[-1]
        return (constants[constant] if constant in constants else constant)

    def variable_reference(base_name, _is_local_, node_name):
        '''
        creates the name used to store the variable in variables.
        -- arguments
        @ base_name := what is normally stored in 'variable_name'
        @ is_local := is the variable local
        @ node_name := the name of the node (only relevant if local)
        @ is_env := is the variable an environment_variable
        -- return
        @ UNNAMED := returns the variable name
        -- side effects
        none
        '''
        return ((node_name + '_DOT_' + base_name) if _is_local_ else base_name)

    def resolve_statements(statements, nodes):
        def handle_read_statement(statement, misc_args):
            if statement.condition_variable is not None:
                handle_variable_assignment(statement, statement.condition_variable, None, misc_args)
                condition = (
                    '!('
                    + format_variable(statement.condition_variable, misc_args)
                    + (
                        (
                            '['
                            + (format_code(statement.index_of, misc_args) if statement.is_const == 'index_of' else str(handle_constant(statement.index_of)))
                            + ']'
                        )
                        if is_array(statement.condition_variable)
                        else
                        ''
                    )
                    + ')'
                )
            else:
                condition = '!(' + format_code(statement.condition, misc_args) + ')'
            for variable_statement in statement.variable_statements:
                handle_variable_assignment(variable_statement, variable_statement.variable, condition, misc_args)
            return

        def handle_write_statement(statement, misc_args):
            delayed = []
            for var_update in statement.update:
                if var_update.instant:
                    handle_variable_assignment(var_update, var_update.variable, None, misc_args)
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
                handle_condition(statement, nodes, create_misc_args(node_name, True, False, None, None))
            elif statement_type == 'return':
                handle_return_statement(statement, nodes, create_misc_args(node_name, True, False, None, None))
            else:
                if statement.variable_statement is not None:
                    handle_variable_assignment(statement.variable_statement, statement.variable_statement.variable, None, create_misc_args(node_name, True, False, None, None))
                elif statement.read_statement is not None:
                    handle_read_statement(statement.read_statement, create_misc_args(node_name, True, False, None, None))
                else:
                    delayed_statements += handle_write_statement(statement.write_statement, create_misc_args(node_name, True, False, None, None))
            for argument_name in argument_pairs:
                constants.pop(argument_name)
        for (node_name, argument_pairs, statement) in delayed_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            handle_variable_assignment(statement, statement.variable, None, create_misc_args(node_name, True, False, None, None))
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
                handle_variable_assignment(statement, statement.variable, None, create_misc_args(None, True, False, None, None))

    def get_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage):
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
        # create each variable type using the template.
        variables = {
            variable_reference(variable.name, False, '') :
            (
                create_variable_template(variable.name, variable.model_as, handle_constant(variable.array_size), None, 0, 0, None, [], True, True)
                if variable.model_as == 'DEFINE' else
                create_variable_template(variable.name, variable.model_as, handle_constant(variable.array_size),
                                         ('integer' if variable.domain.true_int is not None else (None if (variable.domain.min_val is not None or variable.model_as == 'DEFINE') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}')))),
                                         0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                         1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                         None, [], keep_stage_0, keep_last_stage
                                         )
            )
            for variable in model.variables if not is_local(variable)
        }
        local_variable_templates = {
            variable.name :
            (
                create_variable_template(variable.name, variable.model_as, handle_constant(variable.array_size), None, 0, 0, None, [], True, True)
                if variable.model_as == 'DEFINE' else
                create_variable_template(variable.name, variable.model_as, handle_constant(variable.array_size),
                                         ('integer' if variable.domain.true_int is not None else (None if (variable.domain.min_val is not None or variable.model_as == 'DEFINE') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}')))),
                                         0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                         1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                         None, [], keep_stage_0, keep_last_stage
                                         )
            )
            for variable in model.variables if is_local(variable)
        }
        for variable in model.variables:
            if variable.model_as == 'DEFINE':
                if is_local(variable):
                    local_variable_templates[variable.name]['existing_definitions'] = {}
                    local_variable_templates[variable.name]['initial_value'] = None
                else:
                    variables[variable_reference(variable.name, False, '')]['existing_definitions'] = {}
                    variables[variable_reference(variable.name, False, '')]['initial_value'] = variable
            else:
                if is_local(variable):
                    local_variable_templates[variable.name]['initial_value'] = handle_variable_statement(variable, variable, None, create_misc_args(None, False, False, None, None))
                else:
                    variables[variable_reference(variable.name, False, '')]['initial_value'] = handle_variable_statement(variable, variable, None, create_misc_args(None, False, False, None, None))

        # create local variables.
        for local_variable_pair in local_variables:
            new_name = variable_reference(local_variable_pair[1].name, True, local_variable_pair[0])
            new_var = copy.deepcopy(local_variable_templates[local_variable_pair[1].name])
            new_var['name'] = new_name
            if local_variable_pair[1].model_as == 'DEFINE':
                new_var['initial_value'] = local_variable_pair[1]
            variables[new_name] = new_var

        # handle initial statements FOR DEFINE ONLY.
        # we have to parse and update this first. only after that can we go through non-define macros.
        # this is so we populate the definitions and what not.
        for (node_name, argument_pairs, initial_statement) in initial_statements:
            for argument_name in argument_pairs:
                constants[argument_name] = argument_pairs[argument_name]
            assign_var = initial_statement.variable
            if assign_var.model_as == 'DEFINE':
                # variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = handle_variable_statement(initial_statement, assign_var, None, create_misc_args(node_name, False, False, None, None))
                variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = initial_statement
            for argument_name in argument_pairs:
                constants.pop(argument_name)

        for (node_name, initial_statement) in initial_statements:
            assign_var = initial_statement.variable
            if assign_var.model_as != 'DEFINE':
                variables[variable_reference(assign_var.name, is_local(assign_var), node_name)]['initial_value'] = handle_variable_statement(initial_statement, assign_var, None, create_misc_args(node_name, False, False, None, None))

        return variables

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
                argument_pairs = {
                    current_node.leaf.argument_names[index]: handle_constant(current_node.arguments[index])
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
        # print(node_name + ' : ' + str(parent_name))
        return (
            create_node[current_node.node_type](current_node, node_name, modifier, node_names, node_names_map, parent_name)
            if argument_pairs is None
            else
            create_node[current_node.node_type](current_node, argument_pairs, node_name, modifier, node_names, node_names_map, parent_name)
        )

    function_format = {
        'abs' : ('abs', format_function_before),
        'max' : ('max', format_function_before),
        'min' : ('min', format_function_before),
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
        'equal' : ('=', format_function_between),
        'not_equal' : ('!=', format_function_between),
        'less_than' : ('<', format_function_between),
        'greater_than' : ('>', format_function_between),
        'less_than_or_equal' : ('<=', format_function_between),
        'greater_than_or_equal' : ('>=', format_function_between),
        'negative' : ('-', format_function_before),
        'addition' : ('+', format_function_between),
        'subtraction' : ('-', format_function_between),
        'multiplication' : ('*', format_function_between),
        'division' : ('/', format_function_between),
        'mod' : ('mod', format_function_between),
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
        'check_environment' : create_check,
        'action' : create_action
    }

    metamodel = textx.metamodel_from_file(metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(model_file)
    hyper_mode = model.hypersafety
    specification_writing = False  # this is used to track whether or not code should make references to the trace and system or not.
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }
    serene_index = []
    variables = {}
    spec_warn = False
    validate_model(model, constants)

    (_, _, _, nodes, local_variables, initial_statements, statements) = walk_tree(model.root)

    variables = get_variables(model, local_variables, initial_statements, keep_stage_0, keep_last_stage)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, create_misc_args(None, True, False, None, None))
    complete_environment_variables(model, True)
    resolve_statements(statements, nodes)
    complete_environment_variables(model, False)
    specification_writing = True
    spec_warn = True
    specifications = handle_specifications(model.specifications)
    spec_warn = False
    enum_constants = set()
    for variable in model.variables:
        if variable_type(variable, constants) == 'ENUM' and variable.model_as != 'DEFINE':
            enum_constants.update(variable.domain.enums)

    if behave_only:
        if output_file is None:
            printer = pprint.PrettyPrinter(indent = 4)
            printer.pprint({'nodes' : nodes
                            , 'variables' : variables
                            , 'enum_constants' : enum_constants
                            , 'tick_condition' : tick_condition
                            , 'specifications' : specifications})
        else:
            with open(output_file, 'w', encoding = 'utf-8') as write_file:
                printer = pprint.PrettyPrinter(indent = 4, stream = write_file)
                printer.pprint({'nodes' : nodes
                                , 'variables' : variables
                                , 'enum_constants' : enum_constants
                                , 'tick_condition' : tick_condition
                                , 'specifications' : specifications})
    else:
        write_smv(nodes, variables, enum_constants, tick_condition, specifications, hyper_mode, output_file, do_not_trim)
    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--keep_last_stage', action = 'store_true')
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    arg_parser.add_argument('--behave_only', action = 'store_true')
    args = arg_parser.parse_args()
    dsl_to_behaverify(args.metamodel_file, args.model_file, args.keep_stage_0, args.keep_last_stage, args.output_file, args.do_not_trim, args.behave_only)
