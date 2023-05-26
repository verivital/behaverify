import textx
import argparse
import pprint
import os
# import sys
import itertools
import copy
import serene_functions
from behaverify_to_smv import write_smv
from check_model import validate_model

from behaverify_common import create_node_name, create_node_template, create_variable_template

# a NEXT_VALLUE is defined as a triple (node_name, non_determinism, STAGE)
# node_name is a string representing the node where this update happens or none if it's environmental
# non_determinism indicates if this update is non-deterministic
# STAGE are are pairs (condition, result)
# if the condition is true, then the result is used.
# the last condition should always be TRUE


# -------------- FUNCTIONS


class serene_case_default():
    def __init__(self, case, default):
        self.case_results = case
        self.default_result = default


class serene_case():
    def __init__(self, condition, values):
        self.condition = condition
        self.values = values
        self.range_mode = False


class serene_code():
    def __init__(self, constant, mode, variable, function_call, code):
        self.constant = constant
        self.mode = mode
        self.variable = variable
        self.function_call = function_call
        self.code_statement = code


class serene_function_call():
    def __init__(self, function_name, values):
        self.function_name = function_name
        self.values = values


def format_function_before(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        function_name + '('
        + ', '.join([format_code(value, node_name, variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, node_name, variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_after(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        '('
        + code.function_call.node_name
        + function_name
        + ')'
        )


def format_function_before_bounded(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] '  '('
        + ', '.join([format_code(value, node_name, variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_between_bounded(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        '('
        + (' ' + function_name + ' [' + str(code.lower_bound) + ', ' + str(code.upper_bound) + '] ').join([format_code(value, node_name, variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ')'
        )


def format_function_before_between(function_name, code, node_name, variables, use_stages, use_next, not_next):
    return (
        function_name[0] + '['
        + (' ' + function_name[1] + ' ').join([format_code(value, node_name, variables, use_stages, use_next, not_next) for value in code.function_call.values])
        + ']'
        )


def format_function(code, node_name, variables, use_stages, use_next, not_next):
    (function_name, function_to_call) = FUNCTION_FORMAT[code.function_call.function_name]
    return function_to_call(function_name, code, node_name, variables, use_stages, use_next, not_next)


def compute_stage(variable_key, variables, use_stages, overwrite_stage = None):
    '''
    compute the stage for the variable now
    -- arguments
    @ variable_key := used to index into the variable.
    @ variables := a dictionary of variables
    @ use_stages := if true, use stages
    @ overwrite_stage := forces a specific stage
    -- return
    @ the string with appropriate state number
    -- side effects
    none.
    '''
    return (
        (('_stage_' + str(min(overwrite_stage, len(variables[variable_key]['next_value']))) if overwrite_stage > 0 else (
            '' if overwrite_stage == 0 else (
                '_stage_' + str(len(variables[variable_key]['next_value']))
            ))))
        if overwrite_stage is not None else
        (('_stage_' + str(len(variables[variable_key]['next_value']))) if (use_stages and len(variables[variable_key]['next_value']) > 0) else (''))
    )


def find_used_variables(code, node_name, variables, use_stages):
    return (
        [] if code.constant is not None else (
            [format_variable(code.variable, (code.mode == 'local'), node_name, (code.mode == 'env'), variables, use_stages, False, None)] if code.variable is not None else (
                find_used_variables(code.code_statement, node_name, variables, use_stages) if code.code_statement is not None else (
                    [variable for value in code.function_call.values for variable in find_used_variables(value, node_name, variables, use_stages)]
                    )
                )
            )
        )


def format_variable(variable_obj, is_local, node_name, is_env, variables, use_stages, use_next, not_next, overwrite_stage = None):
    '''
    -- ARGUMENTS
    @ variable_obj := a textx object of a variable that we will be formatting.
    @ is_local := is the variable local?
    @ node_name := the name of the node which caused this to be called.
    @ is_env := is this an environment variable?
    @ variables := a dict of all variables
    @ use_stages := are we using stages for this?
    @ use_next := are we making a 'next' call for this. (only used in optimization cases where we're optimizing out stage_0
    @ not_next := only matters if use_next is true. In that case, this variable is replaced with a macro link.
    @ overwrite_stage := overwrite which stage we're asking for.
    '''
    variable_key = variable_reference(variable_obj.name, is_local, node_name, is_env)
    variable = variables[variable_key]
    if variable['mode'] == 'DEFINE':
        if overwrite_stage is not None:
            return (
                ('' if not use_next else 'next(')
                + variable['prefix']
                + variable['name']
                + '_stage_' + str(overwrite_stage)
                + ('' if not use_next else ')'))
        used_vars = []
        for code_fragment in variable_obj.initial_value.default_result.values:
            used_vars += find_used_variables(code_fragment, node_name, variables, use_stages)
        for case_result in variable_obj.initial_value.case_results:
            for code_fragment in case_result.values:
                used_vars += find_used_variables(code_fragment, node_name, variables, use_stages)
            used_vars += find_used_variables(case_result.condition, node_name, variables, use_stages)
        used_vars = tuple(sorted(list(set(used_vars))))
        if used_vars not in variable['existing_definitions']:
            variable['existing_definitions'][used_vars] = len(variable['next_value'])
            variable['next_value'].append(make_new_stage(variable_obj.initial_value, node_name, variables, use_stages, use_next, not_next))
        stage = variable['existing_definitions'][used_vars]
        return (
            ('' if not use_next else 'next(')
            + variable['prefix']
            + variable['name']
            + '_stage_' + str(stage)
            + ('' if not use_next else ')'))

    if use_stages and (len(variable['next_value']) == 0 or overwrite_stage == 0):
        variable['keep_stage_0'] = True
    if use_next and variable_key == not_next:
        return 'LINK_TO_PREVIOUS_FINAL_' + variable['prefix'] + variable['name']
    return (('' if not use_next else 'next(')
            + variable['prefix']
            + variable['name']
            + compute_stage(variable_key, variables, use_stages, overwrite_stage)
            + ('' if not use_next else ')'))


def format_code(code, node_name, variables, use_stages, use_next, not_next):
    return (
        (str(code.constant).upper() if isinstance(code.constant, bool) else str(handle_constant(code.constant))) if code.constant is not None else (
            (format_variable(code.variable, code.mode == 'local', code.node_name if hasattr(code, 'node_name') else node_name, code.mode == 'env', variables, use_stages, use_next, not_next, (code.read_at if hasattr(code, 'read_at') else None))) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name, variables, use_stages, use_next, not_next) + ')') if code.code_statement is not None else (
                    format_function(code, node_name, variables, use_stages, use_next, not_next)
                )
            )
        )
    )


def build_range_func(code):
    return (
        (lambda x : handle_constant(code.constant)) if code.constant is not None else (
            (lambda x : x) if code.value else (
                build_range_func(code.code_statement) if code.code_statement is not None else (
                    (lambda x : RANGE_FUNCTION[code.function_call.function_name]([build_range_func(value) for value in code.function_call.values], x))
                )
            )
        )
    )


def make_new_stage(statement, node_name, variables, use_stages, use_next, not_next):
    '''
    this creates a new_stage and returns it.
    the stage consists of (conditions, results) pairs in order.
    if a condition is met, that value is used.
    the last condition is always TRUE, ensuring at least one condition will be met.
    -- arguments
    @ statement := a code statement (see grammar defined in behaverify.tx)
     -> the statement contains the information we need.
    @ node_name := the name of the node to use string usually, can be None.
     -> this is used by methods called by make_new_stage.
    @ variables := a dictionary of variables_names to variable_info
    @ local_variables := a dictionary of variable_names to variable_info
    @ use_stages := a boolean.
     -> if true, variables will be formattted to use their current stage.
     -> if false, variables will just use their name
    @ use_next := a boolean
     -> usually false. This is only True in the case where we've decided we will
     -> be deleting stage_0, and therefore stage_1 must use next statements.
    @ not_next := a string or None.
     -> Only relevant if use_next is true. in that case, this is the name of the
     -> variable which is having stage_0 deleted, which requires some mapping.
     -> Should only be None if use_next is False.
    -- return
    @ UNNAMED := a new stage is returned.
    -- side effects
    none directly. however, this method calls format_code which calls format_variable
    format_variable has side effects. can modify variables.
    '''

    return (
        [
            (
                format_code(case_result.condition, node_name, variables, use_stages, use_next, not_next)
                ,
                (
                    (
                        '{'
                        + ', '.join([str(value) for value in range(handle_constant(case_result.values[0]), handle_constant(case_result.values[1]) + 1)
                                     if cond_func(value)])
                        + '}'
                    )
                    if (case_result.range_mode and ((cond_func := build_range_func(case_result.values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
                    (
                        ('{' if len(case_result.values) > 1 else '')
                        + ', '.join([format_code(value, node_name, variables, use_stages, use_next, not_next)
                                     for value in case_result.values])
                        + ('}' if len(case_result.values) > 1 else '')
                    )
                )
            )
            for case_result in statement.case_results
        ]
        # the above portion is the optional cases
        +
        # the below portion is the required final case.
        [
            (
                'TRUE'
                ,
                (
                    (
                        '{'
                        + ', '.join([str(value) for value in range(handle_constant(statement.default_result.values[0]), handle_constant(statement.default_result.values[1]) + 1)
                                     if cond_func(value)])
                        + '}'
                    )
                    if (statement.default_result.range_mode and ((cond_func := build_range_func(statement.default_result.values[2])) or True)) else  # this is not a mistake. we are doing this to build the cond func once, instead of having to repeatedly build it
                    (
                        ('{' if len(statement.default_result.values) > 1 else '')
                        + ', '.join([format_code(value, node_name, variables, use_stages, use_next, not_next)
                                     for value in statement.default_result.values])
                        + ('}' if len(statement.default_result.values) > 1 else '')
                    )
                )
            )
        ]
    )


def handle_variable_assignment(variables, variable_obj, node_name, case_default):
    global metamodel
    variable_key = variable_reference(variable_obj.name, textx.textx_isinstance(variable_obj, metamodel['local_variable']), node_name, textx.textx_isinstance(variable_obj, metamodel['environment_variable']))
    variable = variables[variable_key]
    keep_stage_0 = variable['keep_stage_0']
    non_determinism = any([(len(result.values) > 1) for result in itertools.chain([case_default.default_result], case_default.case_results)])
    keep_stage_0 = keep_stage_0 or (not non_determinism)
    variable['next_value'].append((node_name,
                                   non_determinism,
                                   make_new_stage(case_default, node_name, variables, True,
                                                  (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
                                                  (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key))))
    variable['keep_stage_0'] = keep_stage_0
    return


def handle_specifications(specifications, variables):
    return [
        (
            specification.spec_type
            + ' '
            + format_code(specification.code_statement, '', variables, True, False, None)
            + ';'
        )
        for specification in specifications
        ]


def handle_constant(constant):
    return (constants[constant] if constant in constants else constant)


def variable_reference(base_name, is_local, node_name, is_env):
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
    return (
        ('env_' if is_env else ((node_name + '_DOT_') if is_local else ('')))
        + base_name)


def handle_variable_statement(statement, node_name, variables, is_initial, define_only):
    if is_initial:
        variable_key = variable_reference(statement.variable.name, statement.mode == 'local', node_name, statement.mode == 'env')
        variable = variables[variable_key]
        if variable['model_as'] == 'DEFINE':
            variable.initial_value = statement
            pass
        elif define_only:
            # intentional. do nothing in this case.
            pass
        else:
            variables[variable_key]['initial_value'] = make_new_stage(statement, node_name, variables, False, False, None)
    else:
        variable_key = variable_reference(statement.variable.name, statement.mode == 'local', node_name, statement.mode == 'env')
        keep_stage_0 = variables[variable_key]['keep_stage_0']
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        keep_stage_0 = keep_stage_0 or (not non_determinism)
        if keep_stage_0 or len(variables[variable_key]['next_value']) > 0:
            variables[variable_key]['next_value'].append((node_name,
                                                          non_determinism,
                                                          make_new_stage(statement, node_name, variables, True, False, None)))
        else:
            variables[variable_key]['next_value'].append((node_name,
                                                          non_determinism,
                                                          make_new_stage(statement, node_name, variables, True, True, variable_key)))
        variables[variable_key]['keep_stage_0'] = keep_stage_0
    return


def handle_read_statement(statement, node_name, variables, is_initial, define_only):
    if is_initial:
        # if statement.condition is None:
        #     condition_variable_key = variable_reference(statement.condition_variable.name, True, node_name, False)
        #     # if condition_variable_key not in variables:
        #     #     format_variable(statement.condition_variable, True, node_name, False, variables, False, False, None)
        #     new_stage = [('TRUE', '{TRUE, FALSE}')]
        #     variables[condition_variable_key]['initial_value'] = new_stage
        # condition = (
        #     format_code(statement.condition, node_name, variables, False, False, None) if statement.condition is not None else (
        #         format_variable(statement.condition_variable, True, node_name, False, variables, False, False, None)
        #         )
        #     )
        # for variable_statement in statement.variable_statements:
        #     variable_key = variable_reference(variable_statement.variable.name, variable_statement.mode == 'local', node_name, variable_statement.mode == 'env')
        #     # if variable_key not in variables:
        #     #     format_variable(variable_statement.variable, True,
        #     #                     node_name, False, variables, False, False, None)
        #     variable = variables[variable_key]
        #     variable['intial_value'] = ([('!(' + condition + ')',
        #                                   variable['custom_value_range'] if variable['custom_value_range'] is not None else (
        #                                       str(variable['min_val']) + '..' + str(variable['max_val'])
        #                                   )
        #                                   )]
        #                                 +
        #                                 make_new_stage(variable_statement, node_name, variables, False, False, None)
        #                                 )
        raise Exception('a read statement was marked as initial. This should not be possible')
    # else:
    #     if statement.condition is None:
    #         condition_variable_key = variable_reference(statement.condition_variable.name, True, node_name, False)
    #         # if condition_variable_key not in variables:
    #         #     format_variable(statement.condition_variable, True, node_name, False, variables, False, False, None)
    #         new_stage = [('TRUE', '{TRUE, FALSE}')]
    #         variables[condition_variable_key]['next_value'].append((node_name, True, new_stage))
    #     condition = (
    #         format_code(statement.condition, node_name, variables, True, False, None) if statement.condition is not None else (
    #             format_variable(statement.condition_variable, True, node_name, False, variables, True, False, None)
    #             )
    #         )
    #     for variable_statement in statement.variable_statements:
    #         variable_key = variable_reference(variable_statement.variable.name, variable_statement.mode == 'local', node_name, variable_statement.mode == 'env')
    #         # if variable_key not in variables:
    #         #     format_variable(variable_statement.variable, variable_statement.mode == 'local',
    #         #                     node_name, False, variables, False, False, None)
    #         variable = variables[variable_key]
    #         keep_stage_0 = variable['keep_stage_0']
    #         non_determinism = any([(len(result.values) > 1) for result in itertools.chain([variable_statement.default_result], variable_statement.case_results)])
    #         keep_stage_0 = keep_stage_0 or (not non_determinism)
    #         variable['next_value'].append((node_name,
    #                                        non_determinism,
    #                                        (
    #                                            [('!(' + condition + ')',
    #                                              format_variable(variable_statement.variable, variable_statement.mode == 'local',
    #                                                              node_name, False, variables, True,
    #                                                              (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
    #                                                              (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key))
    #                                              )]
    #                                            +
    #                                            make_new_stage(variable_statement, node_name, variables, True,
    #                                                           (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
    #                                                           (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key)))))
    #         variable['keep_stage_0'] = keep_stage_0
    if statement.condition_variable is not None:
        handle_variable_assignment(
            variables, statement.condition_variable, node_name,
            serene_case_default(
                [serene_case(statement.condition,
                             [serene_code(True, None, None, None, None), serene_code(False, None, None, None, None)]
                             if statement.non_determinism
                             else
                             [serene_code(True, None, None, None, None)]
                             )],
                serene_case(None,
                            [serene_code(False, None, None, None, None)]
                            )
            )
        )
    for variable_statement in statement.variable_statements:
        handle_variable_assignment(
            variables, variable_statement.variable, node_name,
            serene_case_default(
                [serene_case(
                    serene_code(None, None, None, serene_function_call('not', [statement.condition]), None)
                    if statement.condition_variable is None
                    else
                    serene_code(None, None, None, serene_function_call('not', [statement.condition_variable]), None)
                    ,
                    [serene_code(None, variable_statement.mode, variable_statement.variable, None, None)]
                )]
                +
                variable_statement.case_results
                ,
                variable_statement.default_result
                )
            )
    return


def handle_write_statement(statement, node_name, variables):
    delayed = []
    for var_update in statement.update:
        if var_update.instant:
            variable_key = variable_reference(var_update.variable.name, False, '', True)
            variable = variables[variable_key]
            keep_stage_0 = variable['keep_stage_0']
            non_determinism = any([(len(result.values) > 1) for result in itertools.chain([var_update.default_result], var_update.case_results)])
            keep_stage_0 = keep_stage_0 or (not non_determinism)
            variable['next_value'].append((node_name,
                                           non_determinism,
                                           make_new_stage(var_update, node_name, variables, True,
                                                          (False if keep_stage_0 or len(variable['next_value']) > 0 else True),
                                                          (None if keep_stage_0 or len(variable['next_value']) > 0 else variable_key))))
            variable['keep_stage_0'] = keep_stage_0
        else:
            delayed.append((node_name, var_update))
    return delayed


def resolve_statements(statements, nodes, variables):

    def handle_return_statement(statement, nodes, node_name, variables):
        node = nodes[node_name]
        statuses = {result.status for result in itertools.chain([statement.default_result], statement.case_results)}
        node['return_possibilities']['success'] = 'success' in statuses
        node['return_possibilities']['running'] = 'running' in statuses
        node['return_possibilities']['failure'] = 'failure' in statuses

        variable_list = []
        if not (len(statement.case_results) == 0 or len(statuses) == 1):
            for case_result in statement.case_results:
                variable_list += find_used_variables(case_result.condition,
                                                     node_name, variables,
                                                     True)
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
                + '\tCONSTANTS' + os.linesep
                + '\t\tsuccess, failure, running, invalid;' + os.linesep
                + '\tDEFINE' + os.linesep
                + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
                + '\t\tinternal_status := ' + os.linesep
                + '\t\t\tcase' + os.linesep
                + ('').join([('\t\t\t\t'
                              + format_code(case_result.condition, node_name, variables, True, False, None)
                              + ' : '
                              + case_result.status
                              + ';' + os.linesep)
                             for case_result in statement.case_results])
                + '\t\t\t\tTRUE : ' + statement.default_result.status + ';' + os.linesep
                + '\t\t\tesac;' + os.linesep
            )
        )
        return

    def handle_condition(condition, nodes, node_name, variables):
        node = nodes[node_name]
        variable_list = (
            find_used_variables(condition,
                                node_name, variables,
                                True)
            if condition is not None else [])
        variable_list = sorted(list(set(variable_list)))
        node['additional_arguments'] = variable_list
        node['internal_status_module_name'] = node_name + '_module'
        node['internal_status_module_code'] = (
            'MODULE ' + node_name + '_module(' + ', '.join(variable_list) + ')' + os.linesep
            + '\tCONSTANTS' + os.linesep
            + '\t\tsuccess, failure, running, invalid;' + os.linesep
            + '\tDEFINE' + os.linesep
            + '\t\tstatus := active ? internal_status : invalid;' + os.linesep
            + '\t\tinternal_status := ('
            + format_code(condition, node_name, variables, True, False, None)
            + ') ? success : failure;' + os.linesep
        )
        return

    delayed_statements = []

    for statement_tuple in statements:
        if statement_tuple[1] == 'check':
            handle_condition(statement_tuple[2], nodes, statement_tuple[0], variables)
        elif statement_tuple[1] == 'return':
            handle_return_statement(statement_tuple[2], nodes, statement_tuple[0], variables)
        else:
            if statement_tuple[2].variable_statement is not None:
                handle_variable_statement(statement_tuple[2].variable_statement, statement_tuple[0], variables, False, False)
            elif statement_tuple[2].read_statement is not None:
                handle_read_statement(statement_tuple[2].read_statement, statement_tuple[0], variables, False, False)
            else:
                delayed_statements += handle_write_statement(statement_tuple[2].write_statement, statement_tuple[0], variables)
    for delayed in delayed_statements:
        handle_variable_statement(delayed[1], delayed[0], variables, False, False)
    return


def complete_environment_variables(model, variables):
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
        new_stage = make_new_stage(statement, None, variables, True, False, False)
        variable_name = variable_reference(statement.variable.name, False, '', True)
        non_determinism = any([(len(result.values) > 1) for result in itertools.chain([statement.default_result], statement.case_results)])
        variables[variable_name]['next_value'].append((None, non_determinism, new_stage))

    return


def get_variables(model, local_variables, initial_statements, keep_stage_0):
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
    variables = {variable_reference(variable.name, False, '', False) :
                 (
                     create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], 'var_', False)
                     if variable.model_as == 'DEFINE' else
                     create_variable_template(variable.name, variable.model_as,
                                              (None if (variable.domain.min_val is not None or variable.model_as == 'DEFINE') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                              0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                              1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                              None, [], 'var_', keep_stage_0
                                              )
                  )
                 for variable in model.blackboard_variables}
    env_variables = {variable_reference(variable.name, False, '', True) :
                     (
                         create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], 'env_', False)
                         if variable.model_as == 'DEFINE' else
                         create_variable_template(variable.name, variable.model_as,
                                                  (None if (variable.domain.min_val is not None or variable.model_as == 'DEFINE') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                                  0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                                  1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                                  None, [], 'env_', keep_stage_0
                                                  )
                     )
                     for variable in model.environment_variables}
    variables.update(env_variables)

    local_variable_templates = {variable.name :
                                (
                                    create_variable_template(variable.name, variable.model_as, None, 0, 0, None, [], '', False)
                                    if variable.model_as == 'DEFINE' else
                                    create_variable_template(variable.name, variable.model_as,
                                                             (None if (variable.domain.min_val is not None or variable.model_as == 'DEFINE') else ('{TRUE, FALSE}' if variable.domain.boolean is not None else ('{' + ', '.join(map(str, map(handle_constant, variable.domain.enums))) + '}'))),
                                                             0 if variable.domain.min_val is None else int(handle_constant(variable.domain.min_val)),
                                                             1 if variable.domain.min_val is None else int(handle_constant(variable.domain.max_val)),
                                                             None, [], '', keep_stage_0
                                                             )
                                )
                                for variable in model.local_variables}

    # add existing_definitions field for local variables.

    for variable in model.blackboard_variables:
        if variable.model_as == 'DEFINE':
            variables[variable_reference(variable.name, False, '', False)]['existing_definitions'] = {}
        else:
            variables[variable_reference(variable.name, False, '', False)]['initial_value'] = make_new_stage(variable.initial_value, None, variables, False, False, None)
    for variable in model.environment_variables:
        if variable.model_as == 'DEFINE':
            variables[variable_reference(variable.name, False, '', True)]['existing_definitions'] = {}
        else:
            variables[variable_reference(variable.name, False, '', True)]['initial_value'] = make_new_stage(variable.initial_value, None, variables, False, False, None)
    for variable in model.local_variables:
        if variable.model_as == 'DEFINE':
            local_variable_templates[variable.name]['existing_definitions'] = {}
        else:
            local_variable_templates[variable.name]['initial_value'] = make_new_stage(variable.initial_value, None, variables, False, False, None)

    # create local variables.

    for local_variable_pair in local_variables:
        new_name = variable_reference(local_variable_pair[1].name, True, local_variable_pair[0], False)
        new_var = copy.deepcopy(local_variable_templates[local_variable_pair[1].name])
        new_var['name'] = new_name
        variables[new_name] = new_var

    # handle initial statements FOR DEFINE ONLY.
    # we have to parse and update this first. only after that can we go through non-define macros.

    for statement_tuple in initial_statements:
        if statement_tuple[1].variable_statement is not None:
            handle_variable_statement(statement_tuple[1], statement_tuple[0], variables, True, True)
        elif statement_tuple[1].read_statement is not None:
            handle_read_statement(statement_tuple[1], statement_tuple[0], variables, True, True)
        else:
            print('warning: DO NOT USE WRITE STATEMENTS IN INITIAL DECLARATIONS')

    for statement_tuple in initial_statements:
        if statement_tuple[1].variable_statement is not None:
            handle_variable_statement(statement_tuple[1], statement_tuple[0], variables, True, False)
        elif statement_tuple[1].read_statement is not None:
            handle_read_statement(statement_tuple[1], statement_tuple[0], variables, True, False)
        else:
            print('warning: DO NOT USE WRITE STATEMENTS IN INITIAL DECLARATIONS')

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


def create_check(current_node, node_name, modifier, node_names, node_names_map, parent_name):
    cur_node_names = {node_name}.union(node_names)
    cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
    return (
        node_name, cur_node_names, cur_node_names_map,
        {node_name : create_node_template(node_name, parent_name, [],
                                          'leaf', current_node.node_type, '', '',
                                          True, False, True)
         },
        [], [], [(node_name, 'check', current_node.condition)]
    )


def create_action(current_node, node_name, modifier, node_names, node_names_map, parent_name):
    cur_node_names = {node_name}.union(node_names)
    cur_node_names_map = {name : (modifier if name == node_name else node_names_map[name]) for name in node_names_map}
    return (
        node_name, cur_node_names, cur_node_names_map,
        {node_name : create_node_template(node_name, parent_name, [],
                                          'leaf', current_node.node_type, '', '',
                                          True, True, True)
         },
        list(map(lambda x : (node_name, x), current_node.local_variables)),
        list(map(lambda x : (node_name, x), current_node.init_statements)),
        (
            list(map(lambda x : (node_name, 'statement', x), current_node.pre_update_statements))
            +
            [(node_name, 'return', current_node.return_statement)]
            +
            list(map(lambda x : (node_name, 'statement', x), current_node.post_update_statements))
        )
    )


def walk_tree(current_node, parent_name = None, node_names = set(), node_names_map = {}):
    while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
        if hasattr(current_node, 'leaf'):
            current_node = current_node.leaf
        else:
            # print(dir(current_node))
            current_node = current_node.sub_root
    # the above deals with sub_trees and leaf nodes, ensuring that the current_node variable has the next actual node at this point
    # next, we get the name of this node, and correct for duplication

    new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
    node_name = new_name[0]
    modifier = new_name[1]
    # print(node_name + ' : ' + str(parent_name))
    return CREATE_NODE[current_node.node_type](current_node, node_name, modifier, node_names, node_names_map, parent_name)


# --------------- CONSTANTS


FUNCTION_FORMAT = {
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


RANGE_FUNCTION = {
    'abs' : serene_functions.serene_abs,
    'max' : serene_functions.serene_max,
    'min' : serene_functions.serene_min,
    'sin' : serene_functions.serene_sin,
    'cos' : serene_functions.serene_cos,
    'tan' : serene_functions.serene_tan,
    'ln' : serene_functions.serene_log,
    'not' : serene_functions.serene_not,
    'and' : serene_functions.serene_and,
    'or' : serene_functions.serene_or,
    'xor' : serene_functions.serene_xor,
    'xnor' : serene_functions.serene_xnor,
    'implies' : serene_functions.serene_implies,
    'equivalent' : serene_functions.serene_eq,
    'equal' : serene_functions.serene_eq,
    'not_equal' : serene_functions.serene_ne,
    'less_than' : serene_functions.serene_lt,
    'greater_than' : serene_functions.serene_gt,
    'less_than_or_equal' : serene_functions.serene_lte,
    'greater_than_or_equal' : serene_functions.serene_gte,
    'negative' : serene_functions.serene_neg,
    'addition' : serene_functions.serene_sum,
    'subtraction' : serene_functions.serene_sub,
    'multiplication' : serene_functions.serene_mult,
    'division' : serene_functions.serene_truediv,
    'mod' : serene_functions.serene_mod,
    'count' : serene_functions.serene_count
}


COMPOSITES = {
    'parallel',
    'sequence',
    'selector',
}


CREATE_NODE = {
    'sequence' : create_composite,
    'selector' : create_composite,
    'parallel' : create_composite,
    'X_is_Y' : create_X_is_Y,
    'inverter' : create_decorator,
    'check' : create_check,
    'check_environment' : create_check,
    'action' : create_action
}


# --------------- Main


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('--keep_stage_0', action = 'store_true')
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--do_not_trim', action = 'store_true')
    arg_parser.add_argument('--behave_only', action = 'store_true')
    args = arg_parser.parse_args()

    metamodel_ = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel_.model_from_file(args.model_file)

    global constants
    constants = {
        constant.name : constant.val
        for constant in model.constants
    }
    validate_model(model, constants, metamodel_)
    global metamodel
    metamodel = metamodel_

    (_, _, _, nodes, local_variables, initial_statements, statements) = walk_tree(model.root)

    variables = get_variables(model, local_variables, initial_statements, args.keep_stage_0)
    tick_condition = 'TRUE' if model.tick_condition is None else format_code(model.tick_condition, None, variables, True, False, None)
    specifications = handle_specifications(model.specifications, variables)  # this included here to ensure we don't erase stage 0 used by specifications.
    resolve_statements(statements, nodes, variables)
    complete_environment_variables(model, variables)
    specifications = handle_specifications(model.specifications, variables)

    if args.behave_only:
        if args.output_file is None:
            printer = pprint.PrettyPrinter(indent = 4)
            printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
        else:
            with open(args.output_file, 'w') as f:
                printer = pprint.PrettyPrinter(indent = 4, stream = f)
                printer.pprint({'tick_condition' : tick_condition, 'nodes' : nodes, 'variables' : variables, 'specifications' : specifications})
    else:
        write_smv(nodes, variables, tick_condition, specifications, args.output_file, args.do_not_trim)
    return


if __name__ == '__main__':
    main()
