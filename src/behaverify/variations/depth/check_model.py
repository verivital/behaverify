import itertools
import serene_functions
# import textx
from behaverify_common import create_node_name

# TODO : function category (TL/INVAR/reg) - DONE?
# TODO : node_types (idk what this means)
# TODO : instant declarations
# TODO : array updates
# TODO : read at/node_name in functions


class BTreeException(Exception):
    '''an exception that indicates something is wrong with the BTree'''
    def __init__(self, last_message = ''):
        self.message = ' -> '.join(trace) + ' ::-> ' + last_message
        super().__init__(self.message)


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


FUNCTION_TYPE_INFO = {
    'abs' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'max' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'min' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    # 'sin' : serene_functions.serene_sin,
    # 'cos' : serene_functions.serene_cos,
    # 'tan' : serene_functions.serene_tan,
    # 'ln' : serene_functions.serene_log,
    'equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'not_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'less_than' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'greater_than' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'less_than_or_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'greater_than_or_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'negative' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'addition' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'subtraction' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'multiplication' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'division' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'mod' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'count' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},
    'index' : {'return_type' : 'depends', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'INVAR', 'reg'}},

    'not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'and' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'or' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'xor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'xnor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'implies' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},
    'equivalent' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL', 'LTL', 'INVAR', 'reg'}, 'allows' : {'CTL', 'LTL', 'INVAR', 'reg'}},

    'active' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
    'success' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
    'running' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},
    'failure' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name', 'allowed_in' : {'CTL', 'LTL', 'INVAR'}, 'allows' : set()},

    'exists_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'exists_next' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'exists_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'exists_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'always_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'always_next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'always_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},
    'always_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'CTL'}, 'allows' : {'CTL', 'INVAR', 'reg'}},

    'next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'globally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'finally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'finally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'until' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'until_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'release' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'release_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'previous' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'not_previous_not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'historically' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'historically_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'once' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'once_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'since' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'since_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'triggered' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}},
    'triggered_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN', 'allowed_in' : {'LTL'}, 'allows' : {'LTL', 'INVAR', 'reg'}}
}


def constant_type(constant):
    global constants
    new_constant = (constants[constant] if constant in constants else constant)
    if isinstance(new_constant, str):
        return 'ENUM'
    elif isinstance(new_constant, bool):
        return 'BOOLEAN'
    elif isinstance(new_constant, int):
        return 'INT'
    else:
        raise BTreeException('Constant ' + constant + ' is of an unsupported type. Only ENUM, BOOLEAN, and INT are supported')


def variable_type(variable):
    global constants
    if variable.model_as == 'DEFINE':
        return variable.domain
    if variable.domain.boolean is not None:
        return 'BOOLEAN'
    elif variable.domain.min_val is not None:
        return 'INT'
    else:
        return constant_type(variable.domain.enums[0])


def is_local(variable):
    return variable.var_type == 'local'


def is_env(variable):
    return variable.var_type == 'env'


def is_blackboard(variable):
    return variable.var_type == 'bl'


def variable_scope(variable):
    if is_local(variable):
        return 'local'
    elif is_env(variable):
        return 'environment'
    elif is_blackboard(variable):
        return 'blackboard'
    else:
        raise BTreeException('Variable ' + variable.name + ' is not local, blackboard, or environment')


def is_array(variable):
    return variable.array_size is not None


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


def str_format(value):
    if isinstance(value, str):
        return "'" + value + "'"
    return str(value)


def validate_code(code, scopes, variable_names, allowed_functions):
    global all_node_names

    def var_checks(code):
        var_scope = variable_scope(code.variable)
        if var_scope not in scopes:
            raise BTreeException('Expected a variable in one of the following scopes: [' + ', '.join(scopes) + '] but got ' + code.variable.name + ' in scope ' + var_scope)
        if var_scope != 'environment':
            if variable_names is not None:
                if code.variable.name not in variable_names:
                    raise BTreeException('Expected only the following variables: [' + ', '.join(variable_names) + '] but got ' + code.variable.name)
        if var_scope == 'local':
            if hasattr(code, 'node_name'):
                if code.node_name not in all_node_names:
                    raise BTreeException('Reference to a node that does not exist ' + code.node_name)
                # TODO: add a check here which confirms that the node actually uses the local variable.
                # this will prevent the user from specificying a specification using a node that doesn't have this variable.
        return

    if code.constant is not None:
        return (constant_type(code.constant), 'constant', str_format(code.constant))
    elif code.variable is not None:
        var_checks(code)
        if is_array(code.variable):
            raise BTreeException('Variable ' + code.variable.name + ' is an array but appears without being indexed')
        return (variable_type(code.variable), 'variable', code.variable.name)
    elif code.code_statement is not None:
        return validate_code(code.code_statement, scopes, variable_names, allowed_functions)
    else:
        if code.function_call.function_name not in FUNCTION_TYPE_INFO:
            raise BTreeException('Function ' + code.function_call.function_name + ' is not yet supported')
        func_info = FUNCTION_TYPE_INFO[code.function_call.function_name]
        if len(func_info['allowed_in'].intersection(allowed_functions)) == 0:
            raise BTreeException('Function ' + code.function_call.function_name + ' is only allowed in ' + str(func_info['allowed_in']) + ' but we are in ' + str(allowed_functions))
        new_allowed_functions = func_info['allows'].intersection(allowed_functions)
        # handle index specially, and return.
        if code.function_call.function_name == 'index':
            var_checks(code.function_call)
            if len(code.function_call.values) != 1:
                raise BTreeException('Index into variable ' + code.function_call.variable.name + ' should have exactly 1 argument')
            (cur_arg_type, cur_code_type, cur_code) = validate_code(code.function_call.values[0], scopes, variable_names, new_allowed_functions)
            if cur_arg_type != 'INT':
                raise BTreeException('Index into variable ' + code.function_call.variable.name + ' should be an integer')
            return (variable_type(code.function_call.variable), 'indexed variable', code.function_call.variable.name)
        # handle bounded specially
        if 'bounded' in func_info:
            if code.function_call.bound.upper_bound != '+oo':
                lower = handle_constant(code.function_call.bound.lower_bound)
                upper = handle_constant(code.function_call.bound.upper_bound)
                if upper < lower:
                    raise BTreeException('A specification bound has a lower bound of ' + str(lower) + ' which is more than the upper bound of ' + str(upper))
        if func_info['max_arg'] != -1:
            if len(code.function_call.values) > func_info['max_arg']:
                raise BTreeException('Function ' + code.function_call.function_name + ' expected at most ' + str(func_info['max_arg']) + ' but got ' + len(code.function_call.values))
        if len(code.function_call.values) < func_info['min_arg']:
            raise BTreeException('Function ' + code.function_call.function_name + ' expected at least ' + str(func_info['min_arg']) + ' but got ' + len(code.function_call.values))
        return_type = func_info['return_type']
        arg_type = func_info['arg_type']
        if arg_type == 'node_name':
            if code.function_call.node_name not in all_node_names:
                raise BTreeException('Reference to a node that does not exist ' + code.function_call.node_name)
        if arg_type == 'depends':
            (arg_type, _, _) = validate_code(code.function_call.values[0], scopes, variable_names, new_allowed_functions)
        for index, value in enumerate(code.function_call.values):
            (cur_arg_type, cur_code_type, cur_code) = validate_code(value, scopes, variable_names, new_allowed_functions)
            if cur_arg_type != arg_type:
                raise BTreeException('Function ' + code.function_call.function_name + ' expected ' + arg_type + ' but got ' + cur_arg_type + ' from argument number ' + str(index) + ' which is ' + cur_code_type + ' ' + cur_code)
        return (return_type, 'function', code.function_call.function_name)


def validate_condition(code, scopes, variable_names, allowed_functions):
    (cur_arg_type, cur_code_type, cur_code) = validate_code(code, scopes, variable_names, allowed_functions)
    if cur_arg_type != 'BOOLEAN':
        raise BTreeException('Conditition expected BOOLEAN but got ' + cur_arg_type + ' from ' + cur_code_type + ' ' + cur_code)
    return


def handle_constant(constant):
    global constants
    return (constants[constant] if constant in constants else constant)


def validate_variable_assignment(variable, assign, scopes, variable_names, deterministic = False, init_mode = None):
    trace.append('In variable assignment for: ' + variable.name)
    if sum([is_local(variable), is_env(variable), is_blackboard(variable)]) != 1:
        raise BTreeException('marked as not exactly one type (this should be unreachable)')
    if init_mode is None and (variable.model_as in {'DEFINE', 'FROZENVAR'}):
        raise BTreeException('updating variable modeled as ' + variable.model_as)
    if init_mode == 'node' and (not is_local(variable)):
        raise BTreeException('initializes non_local variable')

    var_type = variable_type(variable)

    def handle_case_result(case_result, is_default):
        if not is_default:
            validate_condition(case_result.condition, scopes, variable_names, {'reg'})
        if case_result.range_mode:
            if deterministic:
                raise BTreeException('needs to be updated deterministicly here but is being updated non-deterministicly')
            if var_type != 'INT':
                raise BTreeException('type ' + var_type + ' is being updated using range_mode')
            cond_func = build_range_func(case_result.values[2])
            if not any(map(cond_func, range(handle_constant(case_result.values[0]), handle_constant(case_result.values[1]) + 1))):
                raise BTreeException('assigned a value using range_mode but the range is empty')
        else:
            if deterministic and len(case_result.values) > 1:
                raise BTreeException('needs to be updated deterministicly here but is being updated non-deterministicly')
            for value in case_result.values:
                (cur_arg_type, cur_code_type, cur_code) = validate_code(value, scopes, variable_names, {'reg'})
                if cur_arg_type != var_type:
                    raise BTreeException('type ' + var_type + ' is being updated with ' + cur_code_type + ' ' + cur_code + ' which is of type ' + cur_arg_type)
    for case_result in assign.case_results:
        handle_case_result(case_result, False)
    handle_case_result(assign.default_result, True)
    trace.pop()
    return


def validate_array_assign(statement, constant_index, scopes, variable_names, node, deterministic = True, init_mode = None):
    trace.append('In Array Assignment for: ' + statement.variable.name)
    assign_var = statement.variable
    if not is_array(assign_var):
        raise BTreeException('updated as array but is not an array')
    if statement.array_mode == 'range':
        if statement.assign is None:
            raise BTreeException('updated with incorrect syntax')
        if not hasattr(statement, 'values') or len(statement.values) == 0:
            serene_indices = list(range(assign_var.array_size))
        else:
            cond_func = build_range_func(statement.values[2])
            min_val = handle_constant(statement.values[0])
            max_val = handle_constant(statement.values[1])
            if max_val < min_val:
                raise BTreeException('max_val is less than min_val')
            serene_indices = list(filter(cond_func, range(min_val, max_val + 1)))
        if len(serene_indices) == 0:
            raise BTreeException('is being updated using a range with no values')
        global constants
        constants['serene_index'] = 0  # this just used to confirm the types, not an actual value
        if init_mode == 'node':
            validate_variable_assignment(assign_var, statement.assign, scopes, variable_names, deterministic, init_mode)
        else:
            if constant_index:
                cur_type = constant_type(statement.assign.index_expr)
            else:
                (cur_type, _, _) = validate_code(statement.assign.index_expr, scopes, variable_names, {'reg'})
            if cur_type != 'INT':
                raise BTreeException('indexed using type of ' + cur_type + ' instead of INT')
            validate_variable_assignment(assign_var, statement.assign.assign, scopes, variable_names, deterministic, init_mode)
        constants.pop('serene_index')
        trace.pop()
        return
    else:
        if init_mode == 'node' and len(statement.assigns) != assign_var.array_size:
            raise BTreeException('array of size ' + str(assign_var.array_size) + ' was initialized with ' + str(len(statement.assigns)) + ' values')
        if len(statement.assigns) == 0:
            raise BTreeException('array variable updated with wrong syntax')
        seen_constants = set()
        for assign in statement.assigns:
            if init_mode == 'node':
                validate_variable_assignment(assign_var, assign, scopes, variable_names, deterministic, init_mode)
            else:
                if constant_index:
                    cur_type = constant_type(assign.index_expr)
                    if handle_constant(assign.index_expr) in seen_constants:
                        raise BTreeException('array is being indexed with constants and a constant appears twice')
                    seen_constants.add(handle_constant(assign.index_expr))
                else:
                    (cur_type, _, _) = validate_code(assign.index_expr, scopes, variable_names, {'reg'})
                if cur_type != 'INT':
                    raise BTreeException('indexed using type of ' + cur_type + ' instead of INT')
                validate_variable_assignment(assign_var, assign.assign, scopes, variable_names, deterministic, init_mode)
        trace.pop()
        return
    raise BTreeException('unreachable state')


def validate_check(node):
    trace.append('In Check: ' + node.name)
    read_variables = set(map(lambda x : x.name, node.read_variables))
    if len(read_variables) != len(node.read_variables):
        raise BTreeException('duplicate read variables')
    validate_condition(node.condition, {'blackboard'}, read_variables, {'reg'})
    trace.pop()
    return


def validate_check_env(node):
    trace.append('In Environment Check: ' + node.name)
    read_variables = set(map(lambda x : x.name, node.read_variables))
    if len(read_variables) != len(node.read_variables):
        raise BTreeException('duplicate read variables')
    validate_condition(node.condition, {'blackboard', 'environment'}, read_variables, {'reg'})
    trace.pop()
    return


def validate_action(node):

    trace.append('In Action: ' + node.name)

    all_vars = set(map(lambda x : x.name, itertools.chain(node.local_variables, node.read_variables, node.write_variables)))
    read_variables = set(map(lambda x : x.name, node.read_variables))
    write_variables = set(map(lambda x : x.name, node.write_variables))
    local_variables = set(map(lambda x : x.name, node.local_variables))
    if len(read_variables) != len(node.read_variables):
        raise BTreeException('duplicate read variables')
    if len(write_variables) != len(node.write_variables):
        raise BTreeException('has duplicate write variables')
    if len(local_variables) != len(node.local_variables):
        raise BTreeException('duplicate local variables')

    if len(node.init_statements) != len(set(map(lambda x: x.variable.name, node.init_statements))):
        raise BTreeException('initializes at least one variable at least twice')

    for var_statement in node.init_statements:
        # if var_statement.instant:
        #     raise BTreeException('Action ' + node.name + ' marked a non-environment statement as instant')
        assign_var = var_statement.variable
        if assign_var.name not in local_variables:
            raise BTreeException('initializing local variable ' + assign_var.name + ' but it it does not appear in the local variable list for the node: [' + ', '.join(local_variables) + ']')
        if is_array(assign_var):
            validate_array_assign(var_statement, True, {'blackboard', 'local'}, all_vars, node, deterministic = True, init_mode = 'node')
        else:
            if var_statement.assign is None or var_statement.array_mode == 'range':
                raise BTreeException('invalid assignment for variable ' + assign_var.name)
            validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = 'node')

    for statement in itertools.chain(node.pre_update_statements, node.post_update_statements):
        if statement.variable_statement is not None:
            trace.append('Variable Statement for: ' + statement.variable_statement.variable.name)
            var_statement = statement.variable_statement
            if var_statement.instant:
                raise BTreeException('non-environment marked as instant')
            assign_var = var_statement.variable
            if assign_var.name not in local_variables and assign_var.name not in write_variables:
                raise BTreeException('updating variable ' + assign_var.name + ' but it is not listed in the local or write variables')
            if is_array(assign_var):
                validate_array_assign(var_statement, var_statement.constant_index == 'constant_index', {'blackboard', 'local'}, all_vars, node, deterministic = True, init_mode = None)
            else:
                if var_statement.assign is None or var_statement.array_mode == 'range':
                    raise BTreeException('has an invalid assignment for variable ' + assign_var.name)
                validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = None)
            trace.pop()
            #
            # END OF VARIABLE_STATEMENT
            #
        elif statement.read_statement is not None:
            trace.append('Read Statement: ' + statement.read_statement.name)
            read_statement = statement.read_statement
            cond_var = None
            if read_statement.condition_variable is not None:
                cond_var = read_statement.condition_variable
                if is_array(cond_var):
                    if read_statement.index_of is None:
                        raise BTreeException('Action ' + node.name + ' is using array ' + cond_var.name + ' without an index as a condition variable')
                    if read_statement.is_const == 'index_of':
                        (cur_type, _, _) = validate_code(read_statement.index_of, {'local', 'blackboard'}, all_vars, {'reg'})
                    else:
                        cur_type = constant_type(read_statement.index_of)
                    if cur_type != 'INT':
                        raise BTreeException('indexing into ' + cond_var.name + ' with something other than an int')
                if not is_array(cond_var) and read_statement.index_of is not None:
                    raise BTreeException(cond_var.name + ' used with an index as a condition variable but it is not an array')
                if is_env(cond_var):
                    raise BTreeException(cond_var.name + ' used as a condition variable but it is an Environment Variable')
                if cond_var.name not in local_variables and cond_var.name not in write_variables:
                    raise BTreeException('updating condition variable ' + cond_var.name + ' but it is not listed in the local or write variables')
                if variable_type(cond_var) != 'BOOLEAN':
                    raise BTreeException('Condition variable for read statement is ' + cond_var.name + ' but ' + cond_var.name + ' is of type ' + variable_type(cond_var) + ' and not BOOLEAN')
                if cond_var.model_as != 'VAR':
                    raise BTreeException('Condition variable for read statement is ' + cond_var.name + ' but ' + cond_var.name + ' is modeled as ' + cond_var.model_as)
            (cur_arg_type, _, _) = validate_code(read_statement.condition, {'blackboard', 'local', 'environment'}, all_vars, {'reg'})
            if cur_arg_type != 'BOOLEAN':
                raise BTreeException('read statement with a condition of type ' + cur_arg_type + ' instead of BOOLEAN')
            if read_statement.non_determinism and cond_var is None:
                raise BTreeException('non-deterministic read statement but no condition variable')
            for var_statement in read_statement.variable_statements:
                trace.append('Variable Statement for: ' + var_statement.variable.name)
                if var_statement.instant:
                    raise BTreeException('non-environment statement as instant')
                assign_var = var_statement.variable
                if cond_var is not None:
                    if cond_var.name == assign_var.name:
                        raise BTreeException(cond_var.name + ' used as a condition variable and update variable in the same read statement')
                if is_env(assign_var):
                    raise BTreeException('updating ' + assign_var.name + ' as part of a read statement but it is an Environment Variable')
                if assign_var.name not in write_variables and assign_var.name not in local_variables:
                    raise BTreeException('updating ' + assign_var.name + ' but ' + assign_var.name + ' is not declared in write_variables: [' + ', '.join(write_variables) + '] or in local_variables: [' + ', '.join(local_variables) + ']')
                if is_array(assign_var):
                    validate_array_assign(var_statement, var_statement.constant_index == 'constant_index', {'blackboard', 'local', 'environment'}, all_vars, node, deterministic = False, init_mode = None)
                else:
                    if var_statement.assign is None or var_statement.array_mode == 'range':
                        raise BTreeException('invalid assignment for variable ' + assign_var.name)
                    validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                trace.pop()
            trace.pop()
            #
            # END OF READ_STATEMENT
            #
        elif statement.write_statement is not None:
            trace.append('Write Statement: ' + statement.write_statement.name)
            write_statement = statement.write_statement
            for var_statement in write_statement.update:
                trace.append('Variable Statement for: ' + var_statement.variable.name)
                assign_var = var_statement.variable
                if not is_env(assign_var):
                    raise BTreeException('updating ' + assign_var.name + ' as part of a write statement but it is not an Environment Variable')
                if is_array(assign_var):
                    validate_array_assign(var_statement, var_statement.constant_index == 'constant_index', {'blackboard', 'local', 'environment'}, all_vars, node, deterministic = False, init_mode = None)
                else:
                    if var_statement.assign is None or var_statement.array_mode == 'range':
                        raise BTreeException('invalid assignment for variable ' + assign_var.name)
                    validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
                trace.pop()
            trace.pop()
            #
            # END OF WRITE_STATEMENT
            #
        else:
            raise BTreeException('Action ' + node.name + ' has a statement of an unrecognized type (should be impossible)')

    for case_result in node.return_statement.case_results:
        validate_condition(case_result.condition, {'blackboard', 'local'}, all_vars, {'reg'})
    trace.pop()
    return


def validate_variable(variable, scopes, variable_names):
    global constants
    trace.append('In Variable: ' + variable.name)
    if variable.model_as != 'DEFINE':
        if variable.domain.min_val is not None:
            min_val = handle_constant(variable.domain.min_val)
            max_val = handle_constant(variable.domain.max_val)
            if max_val < min_val:
                raise BTreeException('Variable ' + variable.name + ' domain has a minimum value of ' + str(min_val) + ' which is greater than its maximum value of ' + str(max_val))
            if variable.domain.condition is not None:
                cond_func = build_range_func(variable.domain.condition)
                if not any(map(cond_func, range(min_val, max_val + 1))):
                    raise BTreeException('Variable ' + variable.name + ' has an empty range domain when condition is applied')
        elif variable.domain.boolean is not None:
            pass
        else:
            var_type = variable_type(variable)
            for enum in variable.domain.enums:
                if constant_type(enum) != var_type:
                    raise BTreeException('Variable ' + variable.name + ' mixes enumeration types')
    if is_array(variable):
        if variable.array_mode == 'range':
            for index in range(handle_constant(variable.array_size)):
                constants['serene_index'] = index
                validate_variable_assignment(variable, variable.assign, scopes, variable_names, deterministic = not is_env(variable), init_mode = 'default')
            constants.pop('serene_index')
        else:
            if len(variable.assigns) != variable.array_size:
                raise BTreeException('Variable ' + variable.name + ' is an array of size ' + str(variable.array_size) + ' but was initialized with ' + str(len(variable.assigns)) + ' values')
            for assign in variable.assigns:
                validate_variable_assignment(variable, assign, scopes, variable_names, deterministic = not is_env(variable), init_mode = 'default')
    else:
        validate_variable_assignment(variable, variable.assign, scopes, variable_names, deterministic = not is_env(variable), init_mode = 'default')
    trace.pop()
    return


def walk_tree(current_node, node_names, node_names_map):
    while (not hasattr(current_node, 'name') or hasattr(current_node, 'sub_root')):
        if hasattr(current_node, 'leaf'):
            current_node = current_node.leaf
        else:
            current_node = current_node.sub_root
    # next, we get the name of this node, and correct for duplication

    new_name = create_node_name(current_node.name.replace(' ', ''), node_names, node_names_map)
    node_name = new_name[0]
    modifier = new_name[1]

    node_names.add(node_name)
    node_names_map[node_name] = modifier

    if hasattr(current_node, 'memory'):
        if current_node.memory == 'with_true_memory':
            raise BTreeException('True memory not yet implemented')
        if current_node.node_type == 'parallel':
            if current_node.parallel_policy == 'success_on_one' and current_node.memory != '':
                raise BTreeException('Node ' + current_node.name + ' is success_on_one and has memory. This combination does not make sense.')
    if current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            raise BTreeException('Node ' + current_node.name + ' is of type X_is_Y where X==Y')

    if hasattr(current_node, 'child'):
        (node_names, node_names_map) = walk_tree(current_node.child, node_names, node_names_map)
    if hasattr(current_node, 'children'):
        if len(current_node.children) < 2:
            raise BTreeException('Node ' + current_node.name + ' has less than 2 children.')
        for child in current_node.children:
            (node_names, node_names_map) = walk_tree(child, node_names, node_names_map)
    return (node_names, node_names_map)


def validate_model(model, constants_, metamodel_):
    global metamodel, constants, trace
    metamodel = metamodel_
    constants = constants_
    trace = []

    if 'serene_index' in constants:
        raise BTreeException('serene_index was declared as a constant, but is resevered')

    global all_node_names
    (all_node_names, _) = walk_tree(model.root, set(), {})

    variables_so_far = set()
    for variable in model.variables:
        validate_variable(variable, {'blackboard', 'environment'} if is_env(variable) else {'blackboard'}, variables_so_far)
        variables_so_far.add(variable.name)
    # for variable in model.blackboard_variables:
    #     validate_variable(variable, {'blackboard'}, variables_so_far)
    #     variables_so_far.add(variable.name)
    # for variable in model.local_variables:
    #     validate_variable(variable, {'blackboard'}, variables_so_far)
    # for variable in model.environment_variables:
    #     validate_variable(variable, {'blackboard', 'environment'}, variables_so_far)
    #     variables_so_far.add(variable.name)

    for var_statement in model.update:
        assign_var = var_statement.variable
        if is_array(assign_var):
            validate_array_assign(var_statement, var_statement.constant_index == 'constant_index', {'blackboard', 'local', 'environment'}, None, None, deterministic = False, init_mode = None)
        else:
            if var_statement.assign is None or var_statement.array_mode == 'range':
                raise BTreeException('Environment update has an invalid assignment for variable ' + assign_var.name)
            validate_variable_assignment(assign_var, var_statement.assign, {'blackboard', 'environment'}, None, deterministic = False, init_mode = None)
    for check in model.check_nodes:
        validate_check(check)
    for check_env in model.environment_checks:
        validate_check_env(check_env)
    for action in model.action_nodes:
        validate_action(action)

    if model.tick_condition is not None:
        validate_condition(model.tick_condition, {'blackboard', 'local', 'environment'}, None, {'reg'})
    for specification in model.specifications:
        if specification.spec_type == 'LTLSPEC':
            allowed = {'LTL', 'INVAR', 'reg'}
        elif specification.spec_type == 'CTLSPEC':
            allowed = {'CTL', 'INVAR', 'reg'}
        elif specification.spec_type == 'INVARSPEC':
            allowed = {'INVAR', 'reg'}
        else:
            raise BTreeException('unknown specification type: ' + specification.spec_type)
        validate_condition(specification.code_statement, {'blackboard', 'local', 'environment'}, None, allowed)
    print('model check complete')
    return
