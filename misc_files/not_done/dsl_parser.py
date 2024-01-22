

def parse_dsl(dsl_file_path):

    with open(dsl_file_path, 'r', encoding = 'utf-8') as dsl_file:
        dsl_string = ' '.join(dsl_file.readlines())
    reserved_symbols = {
        'configuration', 'end_configuration', 'enumerations', 'end_enumerations', 'constants', 'end_constants', 'variables', 'end_variables', 'environment_update', 'end_environment_update', 'checks', 'end_checks', 'environment_checks', 'end_environment_checks', 'actions', 'end_actions', 'sub_trees', 'end_sub_trees', 'tree', 'end_tree', 'tick_prerequisite', 'end_tick_prerequisite', 'specifications', 'end_specifications',
        'hypersafety', 'use_reals',
        'variable', 'bl', 'local', 'env', 'array',  'VAR', 'FROZENVAR', 'DEFINE', 'INT', 'ENUM', 'BOOLEAN', 'REAL', 'range', 'per_index', 'end_variable',
        'check', 'environment_check', 'action', 'arguments', 'end_arguments', 'local_variables', 'end_local_variables', 'read_variables', 'end_read_variables', 'write_variables', 'end_write_variables', 'condition', 'end_condition', 'initial_values', 'end_initial_values', 'update', 'end_update', 'end_check', 'end_environment_check', 'end_action',
        'composite', 'parallel', 'policy', 'success_on_all', 'success_on_one', 'sequence', 'selector', 'with_partial_memory', 'with_true_memory', 'children', 'end_children', 'end_composite',
        'decorator', 'X_is_Y', 'X', 'Y', 'inverter', 'child', 'end_child', 'end_decorator',
        'sub_tree', 'insert', 'end_insert', 'end_sub_tree',
        'return_statement', 'success', 'running', 'failure', 'end_return_statement',
        'variable_statement', 'instant', 'constant_index', 'end_variable_statement',
        'write_environment', 'end_write_environment',
        'read_environment', 'end_read_environment',
        'index_of', 'end_index_of',
        'assign', 'end_assign', 'case', 'end_case', 'result', 'end_result'
        'LTLSPEC', 'end_LTLSPEC', 'CTLSPEC', 'end_CTLSPEC', 'INVARSPEC', 'end_INVARSPEC',
        '+oo', 'abs', 'max', 'min', 'sin', 'cos', 'exp', 'tan', 'ln', 'eq', 'neq', 'lt', 'gt', 'lte', 'gte', 'neg', 'add', 'sub', 'mult', 'idiv', 'mod', 'rdiv', 'floor', 'count', 'index', 'not', 'and', 'or', 'xor', 'xnor', 'imply', 'equiv', 'active', 'next', 'globally', 'globally_bounded', 'finally', 'finally_bounded', 'until', 'until_bounded', 'release', 'release_bounded', 'previous', 'not_previous_not', 'historically', 'historically_bounded', 'once', 'once_bounded', 'since', 'since_bounded', 'triggered', 'triggered_bounded', 'exists_globally', 'exists_next', 'exists_finally', 'exists_until', 'always_globally', 'always_next', 'always_finally', 'always_until' 
    }
    model = {}
