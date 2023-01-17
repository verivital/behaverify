#
# python3 tree_parser.py root_file root_method --root_args ROOT_ARGS \
# --string_args STRING_ARGS --output_file OUTPUT_FILE

# WARNING: OneShot not supported in this verison.

# -----------------------------------------------------------------------------
import argparse
# import py_trees
# import sys
import os
# import re
# import inspect
# import operator
# import pprint
# import itertools
# import read_files
from behaverify_common import get_root_node, indent

# try:
#     import py_trees_ros
#     py_trees_ros_imported = True
# except ModuleNotFoundError:
#     py_trees_ros_imported = False


"""
nodes : a map (dictionary) from node name to a dictionary of information.
contains the following information
 'name' : the name of the node
 'parent' : the name of the parent
 'children' : a list of names of children
 'category' : leaf, decorator, or composite
 'type' : a string indicating the node type
 'return_arguments' : a map from {'success', 'running', 'failure'} to
    {True, False}, indicating if the type can be returned by the node
 'internal_status_module_name' : the name of the internal status module
 'internal_status_module_code' : the code for the internal status module

variables : a map (dictionary) from variable name to information
about the variable
 'name' : the name of the variable (identical to the key)
 'mode' : 'VAR', 'FROZENVAR', or 'DEFINE'. default 'VAR'
 'custom_value_range' : a string indicating a custom range of values.
    Default: None
 'min_value' : the minimum value (int) the variable can be. default 0
 'max_value' : the maximum value (int) the variable can be. default 1
 'init_value' : the value used at the very start. default None
 'next_value' : a list of pairs (node_name, update_rule), where
    update_rule is a list of pairs (condition, value) such that if the
    condition holds, the value is used.
    Default, []
 'environment_update' : an update rule (see next_value). Used only
    if this variable only updates between ticks.
    Default, None
"""

# -----------------------------------------------------------------------------


def variable_string(variable):
    return (indent(1) + 'variable {' + os.linesep
            + indent(2) + variable['name'] + os.linesep
            + indent(2) + variable['mode'] + os.linesep
            + indent(2) + (
                ('[' + str(variable['min_value']) + ', ' + str(variable['max_value']) + ']') if variable['custom_value_range'] is None else (
                    variable['custom_value_range'].replace('{TRUE, FALSE}', 'BOOLEAN')
                )
            ) + os.linesep
            + indent(1) + '} end_variable' + os.linesep
            )


def variables_string(variables):
    return ''.join([variable_string(variables[variable_name])
                    for variable_name in variables
                    if '_stage_' not in variable_name
                    ])


def check_string(node, variables):
    return (indent(1) + 'check {' + os.linesep
            + indent(2) + node['name'] + os.linesep
            + indent(2) + 'read_variables { } end_read_variables' + os.linesep
            + indent(2) + 'condition { True } end_condition' + os.linesep
            + indent(1) + '} end_check' + os.linesep
            )


def action_string(node, variables):
    return (indent(1) + 'action {' + os.linesep
            + indent(2) + node['name'] + os.linesep
            + indent(2) + 'read_variables { } end_read_variables' + os.linesep
            + indent(2) + 'write_variables { } end_write_variables' + os.linesep
            + indent(2) + 'init { } end_init' + os.linesep
            + indent(2) + 'update {' + os.linesep
            + indent(3) + 'return_statement {' + os.linesep
            + indent(4) + 'result {' + os.linesep
            + indent(5) + 'success ' + str(node['return_possibilities']['success']) + os.linesep
            + indent(5) + 'failure ' + str(node['return_possibilities']['failure']) + os.linesep
            + indent(5) + 'running ' + str(node['return_possibilities']['running']) + os.linesep
            + indent(4) + '} end_result' + os.linesep
            + indent(3) + '} end_return_statement' + os.linesep
            + indent(2) + '} end_update' + os.linesep
            + indent(1) + '} end_action' + os.linesep
            )


def checks_string(nodes, variables):
    return ''.join([check_string(nodes[action_node_name], variables) for action_node_name in nodes if nodes[action_node_name]['type'] == 'check'])


def actions_string(nodes, variables):
    return ''.join([action_string(nodes[action_node_name], variables) for action_node_name in nodes if nodes[action_node_name]['type'] == 'action'])


def handle_decorator_arguments(node, indent_level):
    return ((indent(indent_level) + 'X ' + node['additional_arguments'][0] + os.linesep
             + indent(indent_level) + 'Y ' + node['additional_arguments'][1] + os.linesep
             ) if node['type'] == 'X_is_Y' else (
                 'UNKNOWN DECORATOR TYPE')
            )


def decorator_string(nodes, node, indent_level):
    return (indent(indent_level)
            + node['type'] + os.linesep
            + handle_decorator_arguments(node, indent_level)
            + indent(indent_level) + 'child' + os.linesep
            + tree_string(nodes, node['children'][0], indent_level + 1)
            )


def composite_string(nodes, node, indent_level):
    return (indent(indent_level)
            + ('selector ' if 'selector' in node['type'] else (
                'sequence ' if 'sequence' in node['type'] else (
                    'parallel policy ' + (' success_on_all ' if 'success_on_all' in node['type'] else ' sucess_on_one ')
                    )
                )
               )
            + os.linesep
            + indent(indent_level) + 'memory ' + str('with_memory' in node['type']) + os.linesep
            + indent(indent_level) + 'children {' + os.linesep
            + ''.join([tree_string(nodes, child_name, indent_level + 1)
                       for child_name in node['children']])
            + indent(indent_level) + '} end_children' + os.linesep
            )


def tree_string(nodes, node_name, indent_level = 0):
    node = nodes[node_name]
    return (indent(indent_level)
            + (
                node_name if node['category'] == 'leaf' else (
                    node['category'] + ' {' + os.linesep
                    + indent(indent_level + 1) + node_name + os.linesep
                    + (decorator_string(nodes, node, indent_level + 1) if node['category'] == 'decorator' else composite_string(nodes, node, indent_level + 1))
                    + indent(indent_level) + '} end_' + node['category']
                )
            )
            + os.linesep
            )


def write_to_file(nodes, variables, file_name):
    dsl_string = ('variables {' + os.linesep
                  + variables_string(variables)
                  + '} end_variables' + os.linesep
                  + 'local_variables { } end_local_variables' + os.linesep
                  + 'environment { environment_variables { } end_environment_variables initial_values { } end_initial_values update_values { } end_update_values } end_environment' + os.linesep
                  + 'checks {' + os.linesep
                  + checks_string(nodes, variables)
                  + '} end_checks' + os.linesep
                  + 'actions {' + os.linesep
                  + actions_string(nodes, variables)
                  + '} end_actions' + os.linesep
                  + 'root_node ' + tree_string(nodes, get_root_node(nodes))
                  )
    if file_name is None:
        print(dsl_string)
    else:
        with open(file_name, 'w') as f:
            f.write(dsl_string)
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']
    write_to_file(nodes, variables, args.output_file)
    return


if __name__ == '__main__':
    main()
