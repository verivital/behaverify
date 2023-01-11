#
# python3 tree_parser.py root_file root_method --root_args ROOT_ARGS \
# --string_args STRING_ARGS --output_file OUTPUT_FILE

# WARNING: OneShot not supported in this verison.

# -----------------------------------------------------------------------------
import argparse
import py_trees
import sys
# import os
import re
# import inspect
# import operator
import pprint
import itertools
# import read_files
from behaverify_common import get_root_node, order_nodes, map_node_name_to_number

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


def make_node_name(node_id, index):
    return (node_id[-1] if index == 0 else (node_id[-1] + '_' + str(index)))


def create_nodes(node, preappend = (), node_child_number = 0):
    return {preappend + (node_child_number, node.name) : handle_node(node, preappend, node_child_number),
            **{descendent_key : descendant
               for child_id in range(len(node.children))
               for descendent_key, descendant in create_nodes(
                       node.children[child_id],
                       preappend + (node_child_number, node.name),
                       child_id
               ).items()}
            }


def map_node_id_to_name(nodes):
    return {grouped[index] : make_node_name(grouped[index], index)
            for _, group in itertools.groupby(
                    sorted(nodes.keys(), key = (lambda x : x[-1])),
                    key = (lambda x : x[-1]))
            if len(grouped := list(group)) > 0
            for index in range(len(grouped))}


def refine_nodes(nodes, node_id_to_name):
    # print(node_id_to_name)
    return {
        node_id_to_name[node_id] : {
            'name' : node_id_to_name[node_id],
            'parent' : ((node_id_to_name[nodes[node_id]['parent']])
                        if nodes[node_id]['parent'] in node_id_to_name else None),
            'children' : [node_id_to_name[child_id] for child_id in nodes[node_id]['children']],
            'category' : nodes[node_id]['category'],
            'type' : nodes[node_id]['type'],
            'return_possibilities' : nodes[node_id]['return_possibilities'],
            'additional_arguments' : nodes[node_id]['additional_arguments'],
            'internal_status_module_name' : nodes[node_id]['internal_status_module_name'],
            'internal_status_module_code' : nodes[node_id]['internal_status_module_code']
        }
        for node_id in nodes}


def create_variables(node, node_id_to_name, node_name_to_number, preappend = (), node_child_number = 0):
    return merge_variables(
        ([check_for_variables(node, node_id_to_name, preappend, node_child_number)] if len(node.children) == 0 else [])
        +
        [create_variables(
            node.children[child_id],
            node_id_to_name,
            node_name_to_number,
            preappend + (node_child_number, node.name),
            child_id
        )
         for child_id in range(len(node.children))],
        node_name_to_number
    )


def merge_variables(list_of_variable_maps, node_name_to_number):
    return {variable_name : template_variable(variable_name,
                                              '',
                                              False,
                                              sorted(list(itertools.chain.from_iterable(
                                                  [variable_map[variable_name]['next_value']
                                                   for variable_map in list_of_variable_maps
                                                   if variable_name in variable_map])),
                                                     key = (lambda x : node_name_to_number[x[0]])
                                                     )
                                              )
            for variable_map in itertools.chain(list_of_variable_maps)
            for variable_name in variable_map}


def template_variable(variable_name, node_name, update, next_value = None):
    return {
        'name' : variable_name,
        'mode' : 'VAR',
        'custom_value_range' : None,
        'min_value' : 0,
        'max_value' : 1,
        'init_value' : None,
        'next_value' : ([(node_name, [('TRUE', '{0, 1}')])] if update else []) if next_value is None else next_value,
        'environment_update' : None
    }


def check_for_variables(node, node_id_to_name, preappend, node_child_number):
    return ({node.variable_name : template_variable(node.variable_name, node_id_to_name[preappend + (node_child_number, node.name)], True)} if hasattr(node, 'variable_name') else (
        {node.check.variable : template_variable(node.check.variable, node_id_to_name[preappend + (node_child_number, node.name)], False)} if hasattr(node, 'check') else (
            {}
            # read_files.attempt_to_find_variables(node)
        )
    ))


def handle_node(node, preappend, node_child_number):
    return {
        'name' : preappend + (node_child_number, node.name),
        'parent' : preappend,
        'children' : [(preappend + (node_child_number, node.name, child_id, node.children[child_id].name)) for child_id in range(len(node.children))],
        'category' : get_node_category(node),
        'type' : get_node_type(node),
        'return_possibilities' : get_return_possibilities(node),
        'additional_arguments' : get_additional_arguments(node),
        'internal_status_module_name' : None,
        'internal_status_module_code' : None
        }


def get_node_category(node):
    return ('composite' if len(node.children) > 1 else (
        'decorator' if len(node.children) == 1 else 'leaf'))


def node_is_X_is_Y(node):
    return (isinstance(node, py_trees.decorators.FailureIsRunning)
            or isinstance(node, py_trees.decorators.FailureIsSuccess)
            or isinstance(node, py_trees.decorators.RunningIsFailure)
            or isinstance(node, py_trees.decorators.RunningIsSuccess)
            or isinstance(node, py_trees.decorators.SuccessIsFailure)
            or isinstance(node, py_trees.decorators.SuccessIsRunning))


def node_is_check(node):
    return (isinstance(node, py_trees.behaviours.CheckBlackboardVariableValue)
            or isinstance(node, py_trees.behaviours.CheckBlackboardVariableValues))


def check_memory(node):
    return (
        (
            ('sequence') if isinstance(node, py_trees.composites.Sequence) else (
                ('selector') if isinstance(node, py_trees.composites.Selector) else (
                    ('parallel_success_on_all') if isinstance(node.policy, py_trees.common.ParallelPolicy.SuccessOnAll) else (
                        'parallel_success_on_one'
                    )
                )
            )
        )
        +
        ('_with_memory' if ((hasattr(node, 'memory') and node.memory)
                            or (hasattr(node, 'policy') and node.policy.synchronise)) else '_without_memory')
    )


def get_node_type(node):
    return (
        (check_memory(node) if len(node.children) > 1 else (
            ('X_is_Y') if node_is_X_is_Y(node) else (
                ('unknown_decorator') if len(node.children) == 1 else (
                    ('check') if node_is_check(node) else (
                        'action'
                    )
                )
            )
        ))
    )


def x_is_y_return(node):
    return {
        'success' : not (isinstance(node, py_trees.decorators.SuccessIsFailure)
                         or isinstance(node, py_trees.decorators.SuccessIsRunning)),
        'running' : not (isinstance(node, py_trees.decorators.RunningIsFailure)
                         or isinstance(node, py_trees.decorators.RunningIsSuccess)),
        'failure' : not (isinstance(node, py_trees.decorators.FailureIsRunning)
                         or isinstance(node, py_trees.decorators.FailureIsSuccess))
        }


def get_return_possibilities(node):
    return (
        {'success' : True, 'running' : True, 'failure' : True} if len(node.children) > 1 else (
            x_is_y_return(node) if node_is_X_is_Y(node) else (
                {'success' : True, 'running' : True, 'failure' : True} if len(node.children) == 1 else (
                    {'success' : True, 'running' : False, 'failure' : True} if node_is_check(node) else (
                        {'success' : True, 'running' : True, 'failure' : True}
                    )
                )
            )
        )
    )


X_IS_Y_ARGUMENTS = {
    py_trees.decorators.FailureIsRunning : ['failure', 'running'],
    py_trees.decorators.FailureIsSuccess : ['failure', 'success'],
    py_trees.decorators.RunningIsFailure : ['running', 'failure'],
    py_trees.decorators.RunningIsSuccess : ['running', 'success'],
    py_trees.decorators.SuccessIsFailure : ['success', 'failure'],
    py_trees.decorators.SuccessIsRunning : ['success', 'running']
}


def get_additional_arguments(node):
    return (X_IS_Y_ARGUMENTS[node.__class__] if node_is_X_is_Y(node) else (None))


def write_to_file(root, file_name):
    raw_nodes = create_nodes(root)
    node_id_to_name = map_node_id_to_name(raw_nodes)
    nodes = refine_nodes(raw_nodes, node_id_to_name)
    variables = create_variables(root,
                                 node_id_to_name,
                                 map_node_name_to_number(nodes,
                                                         order_nodes(get_root_node(nodes),
                                                                     nodes)
                                                         )
                                 )
    if file_name is None:
        printer = pprint.PrettyPrinter(indent = 4)
        # printer = modified_pretty_print.modified_pprinter(indent = 4)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        with open(file_name, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, stream = f)
            # printer = modified_pretty_print.modified_pprinter(indent = 4, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('root_file')
    arg_parser.add_argument('root_method')
    arg_parser.add_argument('--root_args', default='', nargs='*')
    arg_parser.add_argument('--string_args', default='', nargs='*')
    arg_parser.add_argument('--output_file', default = None)
    args = arg_parser.parse_args()

    if '/' in args.root_file:
        sys.path.append(re.sub(r'/[^/]*$', '', args.root_file))
        args.root_file = re.sub(r'.*/', '', args.root_file)

    module = __import__(args.root_file.replace('.py', ''))
    root_string = 'module.' + args.root_method + '('
    first = True

    for root_arg in args.root_args:
        if first:
            root_string += root_arg
            first = False
        else:
            root_string += ', ' + root_arg

    for string_arg in args.string_args:
        if first:
            root_string += '\'' + string_arg + '\''
            first = False
        else:
            root_string += ', ' + '\'' + string_arg + '\''

    root_string += ')'
    root = eval(root_string)
    write_to_file(root, args.output_file)
    return


if __name__ == '__main__':
    main()
