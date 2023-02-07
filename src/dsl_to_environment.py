import textx
import argparse
import os
import sys
import itertools
from behaverify_common import indent, create_node_name


def handle_check_env(node):
    return (
        (
            'def ' + node.python_function.split('.')[-1] + ':' + os.linesep
            + indent(1) + "'''" + os.linesep
            + indent(1) + 'This method is expected to return True or False.' + os.linsep
            + indent(1) + 'This method is being modeled using the following behavior:' + os.linesep
            + indent(1) + format_code(node.condition) + os.linesep
            + indent(1) + "'''" + os.linesep
            + indent(1) + 'pass' + os.linesep
            + os.linesep
            + os.linesep
        )
        if node.python_function is not None else '')


def handle_read_statement(statement):
    return (
        (
            'def ' + statement.python_function.split('.')[-1] + ':' + os.linesep
            + indent(1) + "'''" + os.linesep
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
            + indent(1) + "'''" + os.linesep
            + indent(1) + 'pass' + os.linesep
            + os.linesep
            + os.linesep
        )
        if statement.python_function is not None else '')


def handle_write_statement(statement):
    return (
        (
            'def ' + statement.python_function.split('.')[-1] + ':' + os.linesep
            + indent(1) + "'''" + os.linesep
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


def init_method_check_env(node):
    return (indent(1) + 'def __init__(self, name):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + indent(2) + 'self.name = name' + os.linesep
            + os.linesep)


def update_method_check_env(node):
    return (indent(1) + 'def update(self):' + os.linesep
            + indent(2) + 'return ((py_trees.common.Status.SUCCESS) if ('
            + ('' if node.python_function is None else node.python_function)
            + ') else (py_trees.common.Status.FAILURE))' + os.linesep
            + os.linesep)


def variable_assignment(values):
    if len(values) > 1 :
        return ('random.choice('
                + '['
                + ', '.join([format_code(value) for value in values])
                + ']'
                + ')')
    return format_code(values[0])


def handle_variable_statement(statement):
    variable_name = format_variable(statement.variable, statement.is_local)
    if len(statement.case_results) == 0:
        return (indent(2) + variable_name + ' = ' + variable_assignment(statement.default_result.values) + os.linesep)
    return ((''.join([
        (indent(2) + 'elif ' + format_code(case_result.condition) + ':' + os.linesep
         + (indent(3) + variable_name + ' = ' + variable_assignment(case_result.values) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(2) + 'else:' + os.linesep
               + indent(3) + variable_name + ' = ' + variable_assignment(statement.default_result.values) + os.linesep)
            )





def format_returns(status_result):
    return 'py_trees.common.Status.' + status_result.status.upper()


def handle_return_statement(statement):
    variable_name = 'return_status'
    if len(statement.case_results) == 0:
        return (indent(2) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
    return ((''.join([
        (indent(2) + 'elif ' + format_code(case_result.condition) + ':' + os.linesep
         + (indent(3) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
         ) for case_result in statement.case_results])).replace('elif', 'if', 1)
            + (indent(2) + 'else:' + os.linesep
               + indent(3) + variable_name + ' = ' + format_returns(statement.default_result) + os.linesep)
            )


def init_method_action(node):
    return (indent(1) + 'def __init__(self, name):' + os.linesep
            + indent(2) + 'super(' + node.name + ', self).__init__(name)' + os.linesep
            + indent(2) + 'self.name = name' + os.linesep
            + indent(2) + 'self.blackboard = self.attach_blackboard_client(name = name)' + os.linesep
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.READ)' + os.linesep) for variable in node.read_variables])
            + ''.join([(indent(2) + 'self.blackboard.register_key(key = (' + "'" + variable.name + "'" + '), access = py_trees.common.Access.WRITE)' + os.linesep) for variable in node.write_variables])
            + ''.join([handle_statement(statement) for statement in node.init_statements])
            + os.linesep)


def handle_statement(statement):
    return (
        handle_variable_statement(statement.variable_statement) if statement.variable_statement is not None else (
            handle_read_statement(statement.read_statement) if statement.read_statement is not None else (
                handle_write_statement(statement.write_statement)
                )
            )
        )


def update_method_action(node):
    return (indent(1) + 'def update(self):' + os.linesep
            + ''.join([handle_statement(statement) for statement in node.pre_update_statements])
            + handle_return_statement(node.return_statement)
            + ''.join([handle_statement(statement) for statement in node.post_update_statements])
            + indent(2) + 'return return_status' + os.linesep
            )


def custom_imports(node):
    return ((('import ' + (os.linesep + 'import ').join(node.imports) + os.linesep) if node.imports is not None and len(node.imports) > 0 else '')
            + os.linesep + os.linesep)


def build_check_node(node):
    return (STANDARD_IMPORTS
            # + custom_imports(node)
            + class_definition(node.name)
            + init_method_check(node)
            + update_method_check(node)
            )


def build_check_environment_node(node):
    return (STANDARD_IMPORTS
            + custom_imports(node)
            + class_definition(node.name)
            + init_method_check_env(node)
            + update_method_check_env(node)
            )


def build_action_node(node):
    return (STANDARD_IMPORTS
            + custom_imports(node)
            + class_definition(node.name)
            + init_method_action(node)
            + update_method_action(node)
            )


def walk_tree(model, file_name):
    return walk_tree_recursive(model.root, set(), file_name)


def walk_tree_recursive(current_node, node_names, file_name):
    if not hasattr(current_node, 'name'):
        current_node = current_node.leaf

    node_name = create_node_name(current_node.name.replace(' ', ''), node_names)
    node_names.add(node_name)

    # ----------------------------------------------------------------------------------
    # start of massive if statements, starting with composites
    # -----------------------------------------------------------------------------------
    # start of composite nodes
    if current_node.node_type == 'check' or current_node.node_type == 'action':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = ' + current_node.name + '_file.' + current_node.name + '(' + "'" + node_name + "'" + ')' + os.linesep)
        return node_name
    elif current_node.node_type == 'X_is_Y':
        if current_node.x == current_node.y:
            print('Decorator ' + current_node.name + ' has the same X and Y. Exiting.')
            sys.exit()
        decorator_type = (current_node.x.capitalize()
                          + 'Is'
                          + current_node.y.capitalize())
        child = walk_tree_recursive(current_node.child, node_names, file_name)
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                    + child
                    + ', ' + "'" + node_name + "'" + ')' + os.linesep)
        return node_name
    elif current_node.node_type == 'inverter':
        decorator_type = ('inverter')
        child = walk_tree_recursive(current_node.child, node_names, file_name)
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.decorators.' + decorator_type + '('
                    + child
                    + ', ' + "'" + node_name + "'" + ')' + os.linesep)
        return node_name

    # so at this point, we're in composite node territory

    if current_node.node_type == 'sequence':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Sequence(' + "'" + node_name + "'" + ', ' + str(current_node.memory) + ')' + os.linesep)
    elif current_node.node_type == 'selector':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Selector(' + "'" + node_name + "'" + ', ' + str(current_node.memory) + ')' + os.linesep)
    elif current_node.node_type == 'parallel':
        with open(file_name, 'a') as f:
            f.write(indent(1) + node_name + ' = py_trees.composites.Parallel(' + "'" + node_name + "'" + ', py_trees.common.ParallelPolicy.'
                    + (('SuccessOnAll(' + str(current_node.memory) + ')') if current_node.parallel_policy == 'success_on_all' else ('SuccessOnOne()'))
                    + ')' + os.linesep)

    children = '[' + ', '.join([walk_tree_recursive(child, node_names, file_name) for child in current_node.children]) + ']'

    with open(file_name, 'a') as f:
        f.write(indent(1) + node_name + '.add_children('
                + children
                + ')'
                + os.linesep)
    return node_name


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('output_file', default = 'main.py')
    arg_parser.add_argument('location', default = './')
    args = arg_parser.parse_args()

    metamodel = textx.metamodel_from_file(args.metamodel_file, auto_init_attributes = False)
    model = metamodel.model_from_file(args.model_file)

    for action in model.action_nodes:
        with open(args.location + action.name + '_file.py', 'w') as f:
            f.write(build_action_node(action))
    for check in model.check_nodes:
        with open(args.location + check.name + '_file.py', 'w') as f:
            f.write(build_check_node(check))
    for check_env in model.environment_checks:
        with open(args.location + check_env.name + '_file.py', 'w') as f:
            f.write(build_check_environment_node(check_env))

    with open(args.location + args.output_file, 'w') as f:
        f.write(''.join([('import ' + node.name + '_file' + os.linesep) for node in itertools.chain(model.check_nodes, model.action_nodes)])
                + 'import py_trees' + os.linesep
                + os.linesep + os.linesep
                + 'def create_tree():' + os.linesep
                )
    root_name = walk_tree(model, args.location + args.output_file)

    with open(args.location + args.output_file, 'a') as f:
        f.write(indent(1) + 'return ' + root_name + os.linesep)

    return


if __name__ == '__main__':
    main()
