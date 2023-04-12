import textx
import argparse
import os
import itertools
from behaverify_common import indent


def format_function_before(function_name, code, node_name):
    return (
        function_name + '('
        + ', '.join([format_code(value, node_name) for value in code.function_call.values])
        + ')'
        )


def format_function_between(function_name, code, node_name):
    return (
        '('
        + (' ' + function_name + ' ').join([format_code(value, node_name) for value in code.function_call.values])
        + ')'
        )


FUNCTION_FORMAT = {
    'abs' : ('abs', format_function_before),
    'max' : ('max', format_function_before),
    'min' : ('min', format_function_before),
    'sin' : ('math.sin', format_function_before),
    'cos' : ('math.cos', format_function_before),
    'tan' : ('math.tan', format_function_before),
    'ln' : ('math.log', format_function_before),
    'not' : ('not', format_function_before),
    'and' : ('and', format_function_between),
    'or' : ('or', format_function_between),
    'xor' : ('operator.xor', format_function_between),
    'xnor' : ('xnor', format_function_between),
    'implies' : ('->', format_function_between),
    'equivalent' : ('==', format_function_between),
    'equal' : ('==', format_function_between),
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
    'mod' : ('%', format_function_between),
    'count' : ('count', format_function_before)
}


def format_variable_name_only(variable_name, is_local, is_env, node_name):
    return (((node_name + '.') if is_local else ('blackboard.' if not is_env else '')) + variable_name)


def format_variable(variable, is_local, is_env, node_name):
    return (((node_name + '.') if is_local else ('blackboard.' if not is_env else '')) + variable.name)


def format_code(code, node_name):
    # print(code)
    # print(dir(code))
    return (
        ((("'" + code.constant + "'") if isinstance(code.constant, str) else str(code.constant)) if code.constant is not None else (
            (format_variable(code.variable, False if code.is_local is None else code.is_local, (False if not hasattr(code, 'is_env') else (False if code.is_env is None else True)), node_name)) if code.variable is not None else (
                ('(' + format_code(code.code_statement, node_name) + ')') if code.code_statement is not None else (
                    FUNCTION_FORMAT[code.function_call.function_name][1](FUNCTION_FORMAT[code.function_call.function_name][0], code, node_name)
                )
            )
        )
         )
    )


def variable_assignment(values, node_name):
    if len(values) > 1 :
        return ('random.choice('
                + '['
                + ', '.join([format_code(value, node_name) for value in values])
                + ']'
                + ')')
    return format_code(values[0], node_name)


def format_statement(statement, node_name):
    variable_name = format_variable(statement.variable, statement.is_local if hasattr(statement, 'is_local') else False, True if hasattr(statement, 'instant') else False, node_name)
    if len(statement.case_results) == 0:
        return (indent(2) + variable_name + ' = ' + variable_assignment(statement.default_result.values, node_name) + os.linesep)
    return ((''.join([
        (indent(2) + 'elif ' + format_code(case_result.condition, node_name) + ':' + os.linesep
         + (indent(3) + variable_name + ' = ' + variable_assignment(case_result.values, node_name) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(2) + 'else:' + os.linesep
               + indent(3) + variable_name + ' = ' + variable_assignment(statement.default_result.values, node_name) + os.linesep)
            )


def handle_check_env(node):
    return (node.import_from,
            (
                'def '
                + (
                    node.python_function.split('.')[-1]
                    + '('
                    + ', '.join([('arg' + str(x)) for x in range(len(node.args))]) +
                    '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(node.args[x], node.name) + os.linesep)
                        for x in range(len(node.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return True or False.' + os.linesep
                + indent(1) + 'This method is being modeled using the following behavior:' + os.linesep
                + indent(1) + format_code(node.condition, node.name) + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
            )
            if node.python_function is not None else '')


def handle_read_statement(statement, node_name):
    return (statement.import_from,
            (
                'def '
                + (
                    statement.python_function.split('.')[-1]
                    + '('
                    + ', '.join([('arg' + str(x)) for x in range(len(statement.args))]) +
                    '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x], node_name) + os.linesep)
                        for x in range(len(statement.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return a tuple.' + os.linesep
                + indent(1) + 'The values in the tuple should be as follows:' + os.linesep
                + indent(2) + '0: True or False. Indicates if other variables will be updated.' + os.linesep
                + indent(2) + 'Modeled using the following behavior:' + os.linesep
                + ((indent(3) + 'modeled nondeterministically. no restriction') if statement.condition_variable is not None else (
                    indent(3) + format_code(statement.condition, node_name)))
                + os.linesep
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + format_variable(statement.variable_statements[x].variable, statement.variable_statements[x].is_local, False, node_name)
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.variable_statements[x], node_name) + os.linesep
                         )
                        for x in range(len(statement.variable_statements))
                    ])
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
            )
            if statement.python_function is not None else '')


def handle_write_statement(statement, node_name):
    return (statement.import_from,
            (
                'def '
                + (
                    statement.python_function.split('.')[-1]
                    + '('
                    + ', '.join([('arg' + str(x)) for x in range(len(statement.args))]) +
                    '):' + os.linesep
                )
            ),
            (
                indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x], node_name) + os.linesep)
                        for x in range(len(statement.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method does not need to return any value (though it may).' + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to effect the environment.' + os.linesep
                + indent(1) + 'The following changes are expected:' + os.linesep
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + format_variable(statement.update[x].variable, False, True, node_name)
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.update[x], node_name) + os.linesep
                         )
                        for x in range(len(statement.update))
                    ])
                + indent(1) + "'''" + os.linesep
            )
            if statement.python_function is not None else '')


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('default_file')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    to_write = {}
    variables_initial = {
        format_variable(statement.variable, False, True, None) : format_statement(statement, None)
        for statement in model.initial
        }
    variables_update = {
        format_variable_name_only(variable_name, False, True, None) : (
            ''.join(
                [
                    ('# ' + format_statement(statement, None).replace(os.linesep, os.linesep + '# ').rstrip() + os.linesep)
                    for statement in group
                ])
        )
        for variable_name, group in itertools.groupby(
                sorted(model.update, key = (lambda x : x.variable.name)),
                key = (lambda x : x.variable.name))
        }

    to_write[args.default_file] = {
        None : (os.linesep).join(
            [
                (
                    format_variable(variable, False, True, None) + ' = '
                    + (variables_initial[format_variable(variable, False, True, None)] if format_variable(variable, False, True, None) in variables_initial else 'None')
                    + os.linesep
                    + (('# this variable develops in the following way between ticks' + os.linesep + variables_update[format_variable(variable, False, True, None)])
                       if format_variable(variable, False, True, None) in variables_update else
                       ('# this variable does not change bewteen ticks' + os.linesep))
                )
                for variable in model.environment_variables
            ]
        )
    }

    for check_env in model.environment_checks:
        (file_name, function_name, function_body) = handle_check_env(check_env)
        if file_name is None:
            print('WARNING: a check environment node had no import.')
            print('Node name is : ' + check_env.name)
            file_name = args.defualt_file
        if file_name in to_write:
            if function_name in to_write[file_name]:
                to_write[file_name][function_name] += function_body
            else:
                to_write[file_name][function_name] = function_body
        else:
            to_write[file_name] = {function_name : function_body}

    for action in model.action_nodes:
        for statement in itertools.chain(action.init_statements, action.pre_update_statements, action.post_update_statements):
            if statement.variable_statement is not None:
                continue
            (file_name, function_name, function_body) = (
                handle_read_statement(statement.read_statement, action.name)
                if statement.read_statement is not None else
                handle_write_statement(statement.write_statement, action.name))
            if file_name is None:
                print('WARNING: a statement in an action node had no import.')
                print('Node name is : ' + action.name)
                file_name = args.defualt_file
            if file_name in to_write:
                if function_name in to_write[file_name]:
                    to_write[file_name][function_name] += function_body
                else:
                    to_write[file_name][function_name] = function_body
            else:
                to_write[file_name] = {function_name : function_body}

    for file_name in to_write:
        with open(args.location + file_name + '.py', 'w') as f:
            f.write(
                (os.linesep + os.linesep).join(
                    [
                        (
                            ('' if function_name is None else function_name)
                            + to_write[file_name][function_name]
                            + ('' if function_name is None else (indent(1) + 'pass' + os.linesep))
                        )
                        for function_name in to_write[file_name]
                    ]
                )
            )
    return


if __name__ == '__main__':
    main()
