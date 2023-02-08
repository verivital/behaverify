import textx
import argparse
import os
import sys
import itertools
from behaverify_common import indent, create_node_name


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
                + indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(node.args[x]))
                        for x in range(len(node.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return True or False.' + os.linsep
                + indent(1) + 'This method is being modeled using the following behavior:' + os.linesep
                + indent(1) + format_code(node.condition) + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
                + indent(1) + 'pass' + os.linesep
                + os.linesep
                + os.linesep
            )
            if node.python_function is not None else '')


def handle_read_statement(statement):
    return (statement.import_from,
            (
                'def '
                + (
                    statement.python_function.split('.')[-1]
                    + '('
                    + ', '.join([('arg' + str(x)) for x in range(len(statement.args))]) +
                    '):' + os.linesep
                )
                + indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x]))
                        for x in range(len(statement.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method is expected to return a tuple.' + os.linsep
                + indent(1) + 'The values in the tuple should be as follows:' + os.linsep
                + indent(2) + '0: True or False. Indicates if other variables will be updated.' + os.linesep
                + indent(2) + 'Modeled using the following behavior:' + os.linesep
                + ((indent(3) + 'modeled nondeterministically. no restriction') if statement.condition_variable is not None else (
                    indent(3) + format_code(statement.condition)))
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + format_variable(statement.variable_statements[x].variable, statement.variable_statements[x].is_local)
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.variable_statements[x]) + os.linesep
                         )
                        for x in range(len(statement.variable_statements))
                    ])
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to have no side effects (for the tree).' + os.linesep
                + indent(1) + "'''" + os.linesep
                + indent(1) + 'pass' + os.linesep
                + os.linesep
                + os.linesep
            )
            if statement.python_function is not None else '')


def handle_write_statement(statement):
    return (statement.import_from,
            (
                'def '
                + (
                    statement.python_function.split('.')[-1]
                    + '('
                    + ', '.join([('arg' + str(x)) for x in range(len(statement.args))]) +
                    '):' + os.linesep
                )
                + indent(1) + "'''" + os.linesep
                + indent(1) + '-- ARGUMENTS' + os.linesep
                + ''.join(
                    [
                        (indent(1) + '@ arg' + str(x) + ' : ' + format_code(statement.args[x]))
                        for x in range(len(statement.args))
                    ]
                )
                + indent(1) + '-- RETURN' + os.linesep
                + indent(1) + 'This method does not need to return any value (though it may).' + os.linesep
                + indent(1) + '-- SIDE EFFECTS' + os.linesep
                + indent(1) + 'This method is expected to effect the environment.' + os.linsep
                + indent(1) + 'The following changes are expected:' + os.linsep
                + ''.join(
                    [
                        (indent(2) + str(x + 1) + ':'
                         + format_variable(statement.variable_statements[x].variable, statement.variable_statements[x].is_local)
                         + '. Modeled using the following behavior:' + os.linesep
                         + indent(3) + format_statement(statement.variable_statements[x]) + os.linesep
                         )
                        for x in range(len(statement.variable_statements))
                    ])
                + indent(1) + "'''" + os.linesep
                + indent(1) + 'pass' + os.linesep
                + os.linesep
                + os.linesep
            )
            if statement.python_function is not None else '')


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file', default = 'main.py')
    arg_parser.add_argument('location', default = './')
    arg_parser.add_argument('--default_file', default = None)
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    for check_env in model.environment_checks:
        (file_name, function) = handle_check_env(check_env)
        if file_name is None:
            if args.defualt_file is None:
                print('WARNING: a check environment node had no import and no default file was specified.')
                print('Node name is : ' + check_env.name)
            else:
                file_name = args.defualt_file
        if file_name is not None:
            with open(args.location + file_name + '.py', 'w') as f:
                f.write(function)

    return


if __name__ == '__main__':
    main()
