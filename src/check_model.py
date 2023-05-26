import serene_functions
import textx
import itertools
from behaverify_common import create_node_name

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
    'abs' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT'},
    'max' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT'},
    'min' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT'},
    # 'sin' : serene_functions.serene_sin,
    # 'cos' : serene_functions.serene_cos,
    # 'tan' : serene_functions.serene_tan,
    # 'ln' : serene_functions.serene_log,
    'not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'and' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN'},
    'or' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'BOOLEAN'},
    'xor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'xnor' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'implies' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'equivalent' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends'},
    'not_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'depends'},
    'less_than' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'greater_than' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'less_than_or_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'greater_than_or_equal' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'negative' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'INT'},
    'addition' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT'},
    'subtraction' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'multiplication' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : -1, 'arg_type' : 'INT'},
    'division' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'mod' : {'return_type' : 'INT', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'INT'},
    'count' : {'return_type' : 'INT', 'min_arg' : 1, 'max_arg' : -1, 'arg_type' : 'BOOLEAN'},
    'active' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name'},
    'success' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name'},
    'running' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name'},
    'failure' : {'return_type' : 'BOOLEAN', 'min_arg' : 0, 'max_arg' : 0, 'arg_type' : 'node_name'},
    'exists_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'exists_next' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'exists_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'exists_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'always_globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'always_next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'always_finally' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'always_until' :  {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'next' :  {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'globally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'globally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'finally' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'finally_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'until' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'until_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'release' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'release_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'previous' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'not_previous_not' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'historically' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'historically_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'once' : {'return_type' : 'BOOLEAN', 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'once_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 1, 'max_arg' : 1, 'arg_type' : 'BOOLEAN'},
    'since' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'since_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'triggered' : {'return_type' : 'BOOLEAN', 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'},
    'triggered_bounded' : {'return_type' : 'BOOLEAN', 'bounded' : True, 'min_arg' : 2, 'max_arg' : 2, 'arg_type' : 'BOOLEAN'}
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
        raise Exception('Constant ' + constant + ' is of an unsupported type. Only ENUM, BOOLEAN, and INT are supported')


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
    global metamodel
    return textx.textx_isinstance(variable, metamodel['local_variable'])


def is_env(variable):
    global metamodel
    return textx.textx_isinstance(variable, metamodel['environment_variable'])


def variable_scope(variable):
    global metamodel
    if is_local(variable):
        return 'local'
    elif is_env(variable):
        return 'environment'
    elif textx.textx_isinstance(variable, metamodel['blackboard_variable']):
        return 'blackboard'
    else:
        raise Exception('Variable ' + variable.name + ' is not local, blackboard, or environment')


def str_format(value):
    if isinstance(value, str):
        return "'" + value + "'"
    return str(value)


def validate_code(code, scopes, variable_names):
    global all_node_names
    if code.constant is not None:
        return (constant_type(code.constant), 'constant', str_format(code.constant))
    elif code.variable is not None:
        var_scope = variable_scope(code.variable)
        if var_scope not in scopes:
            raise Exception('Expected a variable in one of the following scopes: [' + ', '.join(scopes) + '] but got ' + code.variable.name + ' in scope ' + var_scope)
        if var_scope != 'environment':
            if variable_names is not None:
                if code.variable.name not in variable_names:
                    raise Exception('Expected only the following variables: [' + ', '.join(variable_names) + '] but got ' + code.variable.name)
        if var_scope == 'local':
            if hasattr(code, 'node_name'):
                if code.node_name not in all_node_names:
                    raise Exception('Reference to a node that does not exist ' + code.node_name)
        return (variable_type(code.variable), 'variable', code.variable.name)
    elif code.code_statement is not None:
        return validate_code(code.code_statement, scopes, variable_names)
    else:
        if code.function_call.function_name not in FUNCTION_TYPE_INFO:
            raise Exception('Function ' + code.function_call.function_name + ' is not yet supported')
        func_info = FUNCTION_TYPE_INFO[code.function_call.function_name]
        if 'bounded' in func_info:
            if code.function_call.bound.upper_bound != '+oo':
                lower = handle_constant(code.function_call.bound.lower_bound)
                upper = handle_constant(code.function_call.bound.upper_bound)
                if upper < lower:
                    raise Exception('A specification bound has a lower bound of ' + str(lower) + ' which is more than the upper bound of ' + str(upper))
        if func_info['max_arg'] != -1:
            if len(code.function_call.values) > func_info['max_arg']:
                raise Exception('Function ' + code.function_call.function_name + ' expected at most ' + str(func_info['max_arg']) + ' but got ' + len(code.function_call.values))
        if len(code.function_call.values) < func_info['min_arg']:
            raise Exception('Function ' + code.function_call.function_name + ' expected at least ' + str(func_info['min_arg']) + ' but got ' + len(code.function_call.values))
        return_type = func_info['return_type']
        arg_type = func_info['arg_type']
        if arg_type == 'node_name':
            if code.function_call.node_name not in all_node_names:
                raise Exception('Reference to a node that does not exist ' + code.function_call.node_name)
        if arg_type == 'depends':
            (arg_type, _, _) = validate_code(code.function_call.values[0], scopes, variable_names)
        for index, value in enumerate(code.function_call.values):
            (cur_arg_type, cur_code_type, cur_code) = validate_code(value, scopes, variable_names)
            if cur_arg_type != arg_type:
                raise Exception('Function ' + code.function_call.function_name + ' expected ' + arg_type + ' but got ' + cur_arg_type + ' from argument number ' + str(index) + ' which is ' + cur_code_type + ' ' + cur_code)
        return (return_type, 'function', code.function_call.function_name)


def validate_condition(code, scopes, variable_names):
    (cur_arg_type, cur_code_type, cur_code) = validate_code(code, scopes, variable_names)
    if cur_arg_type != 'BOOLEAN':
        raise Exception('Conditition expected BOOLEAN but got ' + cur_arg_type + ' from ' + cur_code_type + ' ' + cur_code)
    return


def handle_constant(constant):
    global constants
    return (constants[constant] if constant in constants else constant)


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


def validate_variable_assignment(variable, case_default, scopes, variable_names, deterministic = False, init_mode = None):
    if is_local(variable) and is_env(variable):
        raise Exception('Variable ' + variable.name + ' was internally marked as both local and env')
    if init_mode is None and (variable.model_as == 'DEFINE' or variable.model_as == 'FROZENVAR'):
        raise Exception('Variable ' + variable.name + ' is being updated but is modeled as ' + variable.model_as)
    if init_mode == 'node' and (not is_local(variable)):
        raise Exception('Variable ' + variable.name + ' is being updated but is modeled as ' + variable.model_as)

    var_type = variable_type(variable)

    def handle_case_result(case_result, is_default):
        if not is_default:
            validate_condition(case_result.condition, scopes, variable_names)
        if case_result.range_mode:
            if deterministic:
                raise Exception('Variable ' + variable.name + ' needs to be updated deterministicly here but is being updated non-deterministicly')
            if var_type != 'INT':
                raise Exception('Variable ' + variable.name + ' is of type ' + var_type + ' but is being updated using range_mode')
            cond_func = build_range_func(case_result.values[2])
            if not any(map(cond_func, range(handle_constant(case_result.values[0]), handle_constant(case_result.values[1]) + 1))):
                raise Exception('Variable ' + variable.name + ' is being assigned a value using range_mode but the range is empty')
        else:
            if deterministic and len(case_result.values) > 1:
                raise Exception('Variable ' + variable.name + ' needs to be updated deterministicly here but is being updated non-deterministicly')
            for index, value in enumerate(case_result.values):
                (cur_arg_type, cur_code_type, cur_code) = validate_code(value, scopes, variable_names)
                if cur_arg_type != var_type:
                    raise Exception('Variable ' + variable.name + ' is of type ' + var_type + ' but is being updated with ' + cur_code_type + ' ' + cur_code + ' which is of type ' + cur_arg_type)
    for case_result in case_default.case_results:
        handle_case_result(case_result, False)
    handle_case_result(case_default.default_result, True)
    return


def validate_check(node):
    read_variables = set(map(lambda x : x.name, node.read_variables))
    if len(read_variables) != len(node.read_variables):
        raise Exception('Check ' + node.name + ' has duplicate read variables')
    validate_condition(node.condition, {'blackboard'}, set(map(lambda x : x.name, node.read_variables)))
    return


def validate_check_env(node):
    read_variables = set(map(lambda x : x.name, node.read_variables))
    if len(read_variables) != len(node.read_variables):
        raise Exception('Environment Check ' + node.name + ' has duplicate read variables')
    validate_condition(node.condition, {'blackboard', 'environment'}, set(map(lambda x : x.name, node.read_variables)))
    return


def validate_action(node):
    global metamodel
    all_vars = set(map(lambda x : x.name, itertools.chain(node.local_variables, node.read_variables, node.write_variables)))
    read_variables = set(map(lambda x : x.name, node.read_variables))
    write_variables = set(map(lambda x : x.name, node.write_variables))
    local_variables = set(map(lambda x : x.name, node.local_variables))
    if len(read_variables) != len(node.read_variables):
        raise Exception('Action ' + node.name + ' has duplicate read variables')
    if len(write_variables) != len(node.write_variables):
        raise Exception('Action ' + node.name + ' has duplicate write variables')
    if len(local_variables) != len(node.local_variables):
        raise Exception('Action ' + node.name + ' has duplicate local variables')
    for init_statement in node.init_statements:
        if init_statement.variable.name not in local_variables:
            raise Exception('Action ' + node.name + ' is initializing local variable ' + init_statement.variable.name + ' but it it does not appear in the local variable list for the node: [' + ', '.join(local_variables) + ']')
        validate_variable_assignment(init_statement.variable, init_statement, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = 'node')
    for statement in itertools.chain(node.pre_update_statements, node.post_update_statements):
        if statement.variable_statement is not None:
            assign_var = statement.variable_statement.variable
            if assign_var.name not in local_variables and assign_var.name not in write_variables:
                raise Exception('Node ' + node.name + ' is updating variable ' + assign_var.name + ' but it is not listed in the local or write variables')
            validate_variable_assignment(statement.variable_statement.variable, statement.variable_statement, {'blackboard', 'local'}, all_vars, deterministic = True, init_mode = None)
        elif statement.read_statement is not None:
            read_statement = statement.read_statement
            if read_statement.condition_variable is not None:
                cond_var = read_statement.condition_variable
                if textx.textx_isinstance(cond_var, metamodel['environment_variable']):
                    raise Exception('Action ' + node.name + ' is using ' + assign_var.name + ' as a condition variable but it is an Environment Variable')
                if cond_var.name not in local_variables and cond_var.name not in write_variables:
                    raise Exception('Node ' + node.name + ' is updating variable ' + cond_var.name + ' but it is not listed in the local or write variables')
                if variable_type(cond_var) != 'BOOLEAN':
                    raise Exception('Condition variable for read statement in Action ' + node.name + ' is ' + cond_var.name + ' but ' + cond_var.name + ' is of type ' + variable_type(cond_var) + ' and not BOOLEAN')
                if cond_var.model_as != 'VAR':
                    raise Exception('Condition variable for read statement in Action ' + node.name + ' is ' + cond_var.name + ' but ' + cond_var.name + ' is modeled as ' + cond_var.model_as)
            (cur_arg_type, cur_code_type, cur_code) = validate_code(read_statement.condition, {'blackboard', 'local', 'environment'}, all_vars)
            if cur_arg_type != 'BOOLEAN':
                raise Exception('Action ' + node.name + ' has a read statement with a condition of type ' + cur_arg_type + ' instead of BOOLEAN')
            if read_statement.non_determinism and read_statement.condition_variable is None:
                raise Exception('Action ' + node.name + ' has a non-deterministic read statement but no condition variable')
            for assign_statement in read_statement.variable_statements:
                assign_var = assign_statement.variable
                if textx.textx_isinstance(assign_var, metamodel['environment_variable']):
                    raise Exception('Action ' + node.name + ' is updating ' + assign_var.name + ' as part of a read statement but it is an Environment Variable')
                if assign_var.name not in write_variables and assign_var.name not in local_variables:
                    raise Exception('Action ' + node.name + ' is updating ' + assign_var.name + ' but ' + assign_var.name + ' is not declared in write_variables: [' + ', '.join(write_variables) + '] or in local_variables: [' + ', '.join(local_variables) + ']')
                validate_variable_assignment(assign_var, assign_statement, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
        elif statement.write_statement is not None:
            write_statement = statement.write_statement
            for env_statement in write_statement.update:
                assign_var = env_statement.variable
                if not textx.textx_isinstance(assign_var, metamodel['environment_variable']):
                    raise Exception('Action ' + node.name + ' is updating ' + assign_var.name + ' as part of a read statement but it is an Environment Variable')
                validate_variable_assignment(assign_var, env_statement, {'blackboard', 'local', 'environment'}, all_vars, deterministic = False, init_mode = None)
        else:
            raise Exception('Action ' + node.name + ' has a statement of an unrecognized type (should be impossible)')
    for case_result in node.return_statement.case_results:
        validate_condition(case_result.condition, {'blackboard', 'local'}, all_vars)
    return


def validate_variable(variable, scopes, variable_names):
    global metamodel
    if variable.model_as != 'DEFINE':
        if variable.domain.min_val is not None:
            min_val = handle_constant(variable.domain.min_val)
            max_val = handle_constant(variable.domain.max_val)
            if max_val < min_val:
                raise Exception('Variable ' + variable.name + ' domain has a minimum value of ' + str(min_val) + ' which is greater than its maximum value of ' + str(max_val))
            if variable.domain.condition is not None:
                cond_func = build_range_func(variable.domain.condition)
                if not any(map(cond_func, range(min_val, max_val + 1))):
                    raise Exception('Variable ' + variable.name + ' has an empty range domain when condition is applied')
        elif variable.domain.boolean is not None:
            pass
        else:
            var_type = variable_type(variable)
            for enum in variable.domain.enums:
                if constant_type(enum) != var_type:
                    raise Exception('Variable ' + variable.name + ' mixes enumeration types')
    validate_variable_assignment(variable, variable.initial_value, scopes, variable_names, deterministic = not textx.textx_isinstance(variable, metamodel['environment_variable']), init_mode = 'default')
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
            raise Exception('True memory not yet implemented')
        if current_node.node_type == 'parallel':
            if current_node.parallel_policy == 'success_on_one' and current_node.memory != '':
                raise Exception('Node ' + current_node.name + ' is success_on_one and has memory. This combination does not make sense.')
    if current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            raise Exception('Node ' + current_node.name + ' is of type X_is_Y where X==Y')

    if hasattr(current_node, 'child'):
        (node_names, node_names_map) = walk_tree(current_node.child, node_names, node_names_map)
    if hasattr(current_node, 'children'):
        if len(current_node.children) < 2:
            raise Exception('Node ' + current_node.name + ' has less than 2 children.')
        for child in current_node.children:
            (node_names, node_names_map) = walk_tree(child, node_names, node_names_map)
    return (node_names, node_names_map)


def validate_model(model, constants_, metamodel_):
    global metamodel, constants
    metamodel = metamodel_
    constants = constants_

    global all_node_names
    (all_node_names, _) = walk_tree(model.root, set(), {})

    variables_so_far = set()
    for variable in model.blackboard_variables:
        validate_variable(variable, {'blackboard'}, variables_so_far)
        variables_so_far.add(variable.name)
    for variable in model.local_variables:
        validate_variable(variable, {'blackboard'}, variables_so_far)
    for variable in model.environment_variables:
        validate_variable(variable, {'blackboard', 'environment'}, variables_so_far)
        variables_so_far.add(variable.name)

    for env_statement in model.update:
        validate_variable_assignment(env_statement.variable, env_statement, {'blackboard', 'local', 'environment'}, None, deterministic = False, init_mode = None)
    for check in model.check_nodes:
        validate_check(check)
    for check_env in model.environment_checks:
        validate_check_env(check_env)
    for action in model.action_nodes:
        validate_action(action)

    if model.tick_condition is not None:
        validate_condition(model.tick_condition, {'blackboard', 'local', 'environment'}, None)
    for specification in model.specifications:
        validate_condition(specification.code_statement, {'blackboard', 'local', 'environment'}, None)
    return
