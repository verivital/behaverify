'''
Module for visualizing Behavior Trees

Author: Serena Serafina Serbinowska
Last Edit: 2023-11-10
'''
import os
import json
import tkinter
from tkinter import ttk
import graphviz
from dsl_to_nuxmv import dsl_to_nuxmv
from behaverify_common import BTreeException, indent
import traceback

def handle_smv(trace_file_string):
    smv_run = []  # an array of dicts where each dict maps node_names to statuses and maps var_names to dicts which map integers (stages) to values.
    smv_arrays_to_build = {}  # a dict which maps array variables to dicts which maps integers (stages) to dicts which map integers (indices) to values.
    def build_arrays():
        for array_name in smv_arrays_to_build:
            stages_to_array_of_values = {}
            stage = 0
            while stage in smv_arrays_to_build[array_name]:
                indices_to_values = []
                index = 0
                while index in smv_arrays_to_build[array_name][stage]:
                    indices_to_values.append(smv_arrays_to_build[array_name][stage][index])
                    index = index + 1
                stages_to_array_of_values[stage] = '[' + ', '.join(indices_to_values) + ']'
                stage = stage + 1
            smv_run[-1][array_name] = stages_to_array_of_values
        return
    with open(trace_file_string, 'r', encoding = 'utf-8') as trace_file:
        ignore = True
        for line in trace_file:
            line.strip()
            if 'State: ' in line:
                if ignore:
                    ignore = False
                    smv_run.append({})
                    continue
                build_arrays()
                smv_run.append({})
                smv_arrays_to_build = {}
            elif not ignore:
                line = line.replace('system.', '')
                if '.status' in line:
                    node_name = line.split('.status')[0].strip()
                    status = line.split('=')[-1].strip()
                    smv_run[-1][node_name] = status
                elif '_stage_' in line:
                    var_name_stage = line.split('=')[0]
                    var_name_stage = var_name_stage.strip()
                    index = -1
                    if '_index_' in line:
                        (var_name_stage, index) = var_name_stage.split('_index_')
                        index = int(index)
                    elif '[' in var_name_stage:
                        (var_name_stage, index) = var_name_stage.split('[')
                        index = index.replace(']', '')
                        index = int(index)
                    var_name = var_name_stage.split('_stage_')[0]
                    var_name = var_name.strip()
                    var_stage = var_name_stage.split('_stage_')[1]
                    var_stage = var_stage.strip()
                    var_stage = int(var_stage)
                    var_val = line.split('=')[1]
                    var_val = var_val.strip()
                    if index >= 0:
                        if var_name not in smv_arrays_to_build:
                            smv_arrays_to_build[var_name] = {}
                        if var_stage not in smv_arrays_to_build[var_name]:
                            smv_arrays_to_build[var_name][var_stage] = {}
                        smv_arrays_to_build[var_name][var_stage][index] = var_val
                    else:
                        if var_name not in smv_run[-1]:
                            smv_run[-1][var_name] = {}
                        smv_run[-1][var_name][var_stage] = var_val
    build_arrays()
    return smv_run

def fix_name(base_name, nodes):
    node_name = base_name
    count = 1
    while node_name in nodes:
        node_name = base_name + '_' + str(count)
        count = count + 1
    return node_name

def chatGPT_json_to_BehaVerify_json(node, parent_name = None, nodes = None):
    if nodes is None:
        nodes = {}
    node_type = node['type'].strip()  # remove annoying whitespace
    base_name = ''
    node_name = ''
    if node_type.lower() in ('selector', 'fallback', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running'):
        custom_type = None
        node_type = node_type.lower()
        node_name = fix_name(node_type, nodes)  # fix the name
    else:
        node_name = fix_name(node_type, nodes)  # fix the name
        if node_type.lower() in ('check', 'condition', 'guard'):
            custom_type = 'unknown'
            node_type = 'check'
        elif node_type == 'action':
            custom_type = 'unknown'
            node_type = 'action'
        else:
            custom_type = node_type
            node_type = 'action'

    nodes[node_name] = 'temp'
    children = []
    the_children = node.get('children', node.get('nodes', []))
    for child in the_children:
        (child_name, nodes) = chatGPT_json_to_BehaVerify_json(child, node_name, nodes)
        children.append(child_name)
    nodes[node_name] = {'parent' : parent_name, 'type' : node_type, 'custom_type' : custom_type, 'children' : children}
    return (node_name, nodes)


def behaVerify_json_to_chatGPT_json(nodes, root_node_name):
    node = nodes[root_node_name]
    if node['type'] in ('selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running'):
        return {
            'type' : node['type'],
            'children' : [behaVerify_json_to_chatGPT_json(nodes, child_name) for child_name in node['children']]
        }
    return {'type' : root_node_name}

SHAPES = {
    'selector' : 'octagon',
    'sequence' : 'rectangle',
    'parallel' : 'parallelogram',
    'inverter' : 'trapezium',
    'success_is_failure' : 'trapezium',
    'success_is_running' : 'trapezium',
    'running_is_failure' : 'trapezium',
    'running_is_success' : 'trapezium',
    'failure_is_success' : 'trapezium',
    'failure_is_running' : 'trapezium'
}

COLORS = {
    'selector' : '#00FFFF',
    'sequence' : '#FFA500',
    'parallel' : '#FFD700',
    'inverter' : '#FFFFFF',
    'success_is_failure' : '#FFFFFF',
    'success_is_running' : '#FFFFFF',
    'running_is_failure' : '#FFFFFF',
    'running_is_success' : '#FFFFFF',
    'failure_is_success' : '#FFFFFF',
    'failure_is_running' : '#FFFFFF'
}

STATUS_COLORS = {
    'invalid' : 'gray',
    'success' : 'blue',
    'failure' : 'red',
    'running' : 'black'
}

SHORT_TYPE = {
    'action' : 'A',
    'check' : 'C',
    'environment_check' : 'E'
}

def create_dot_from_BehaVerify_json(nodes, root_node_name, output_file = 'behavior_tree', detailed_nodes = True):
    dot = graphviz.Digraph(format='png', filename=output_file)
    def process_node(node_name):
        node = nodes[node_name]
        node_type = node['type']
        parent_name = node['parent']
        node_label = (
            (
                node_name
                if node_type in SHAPES else
                (node_name + os.linesep + SHORT_TYPE.get(node['type'], '?') + ' -> ' + str(node.get('custom_type', None)))
            )
            if detailed_nodes else
            node_name
        )
        #node_label = node_name if node_type in SHAPES else (node_name + os.linesep + str(node.get('custom_type', None)))
        dot.node(node_name, label = node_label, style = 'filled', fillcolor = COLORS.get(node_type, '#C0C0C0'), shape = SHAPES.get(node_type, 'oval'), fontcolor = ('red' if node.get('custom_type', None) in ('check', 'environment_check') else '#000000'))
        if parent_name is not None:
            dot.edge(parent_name, node_name)
        for child in node['children']:
            process_node(child)
    process_node(root_node_name)
    return dot

def visualize_BehaVerify_json(nodes, root_node_name, output_file = 'behavior_tree', mode = 'render', detailed_nodes = True):
    dot = create_dot_from_BehaVerify_json(nodes, root_node_name, output_file, detailed_nodes)
    if mode == 'render':
        dot.render()
    else:
        dot.view()

def get_root_from_BehaVerify_json(nodes):
    for node in nodes:
        if nodes[node]['parent'] is None:
            return node
    raise ValueError('No node without a parent')

def main():
    def import_json():
        nonlocal root_node_name, nodes
        if not os.path.isfile(from_file_entry.get()):
            status_text.config(text = 'Not a file: "' + from_file_entry.get() + '"')
            return
        try:
            with open(from_file_entry.get(), 'r', encoding = 'utf-8') as input_file:
                behavior_tree_json = json.load(input_file)
            (root_node_name, nodes) = chatGPT_json_to_BehaVerify_json(behavior_tree_json)
            status_text.config(text = 'Imported Json, root node name: ' + root_node_name)
        except:
            status_text.config(text = 'An exception occurred during Loading')
    def export_json():
        nonlocal nodes, root_node_name
        try:
            with open(to_file_entry.get() + '.json', 'w', encoding = 'utf-8') as input_file:
                json.dump(behaVerify_json_to_chatGPT_json(nodes, root_node_name), input_file)
            status_text.config(text = 'Exported Json, root node name: ' + root_node_name)
        except:
            status_text.config(text = 'An exception occurred during Saving')
    def visualize():
        try:
            visualize_BehaVerify_json(nodes, root_node_name, output_file = to_file_entry.get(), mode = 'view', detailed_nodes = (True if var_detailed_nodes.get() == 1 else 0))
            status_text.config(text = 'Visualization finished. root node name: ' + root_node_name)
        except Exception as cur_exception:
            status_text.config(text = 'An exception occurred during Visualization: ' + str(cur_exception))
    def export_dsl():
        warning_string = ''
        check_string = ''
        env_check_string = ''
        action_string = ''
        tree_string = ''
        action_names = set()
        check_names = set()
        env_check_names = set()
        def recursive_walk(node_name, indent_level):
            node = nodes[node_name]
            nonlocal tree_string, check_string, action_string, env_check_string, warning_string, action_names, check_names, env_check_names
            if node['custom_type'] is not None:
                tree_string += indent(indent_level) + node_name + ' : ' + node['custom_type'] + '{}' + os.linesep
                if node['type'] == 'check':
                    if node['custom_type'] in check_names:
                        return
                    if node['custom_type'] in action_names or node_name in env_check_names:
                        warning_string += 'Duplicate leaf type: ' + node['custom_type'] + '. '
                    check_names.add(node['custom_type'])
                    check_string += (
                        indent(1) + 'check {' + os.linesep
                        + indent(2) + node['custom_type'] + os.linesep
                        + indent(2) + 'arguments {}' + os.linesep
                        + indent(2) + 'read_variables {}' + os.linesep
                        + indent(2) + 'condition {True}' + os.linesep
                        + indent(1) + '}' + os.linesep
                    )
                    return
                if node['type'] == 'environment_check':
                    if node['custom_type'] in env_check_names:
                        return
                    if node['custom_type'] in action_names or node_name in check_names:
                        warning_string += 'Duplicate leaf type: ' + node['custom_type'] + '. '
                    env_check_names.add(node['custom_type'])
                    env_check_string += (
                        indent(1) + 'environment_check {' + os.linesep
                        + indent(2) + node['custom_type'] + os.linesep
                        + indent(2) + 'arguments {}' + os.linesep
                        + indent(2) + 'read_variables {}' + os.linesep
                        + indent(2) + 'condition {True}' + os.linesep
                        + indent(1) + '}' + os.linesep
                    )
                    return
                if node['custom_type'] in action_names:
                    return
                if node['custom_type'] in check_names or node_name in env_check_names:
                    warning_string += 'Duplicate leaf type: ' + node['custom_type'] + '. '
                action_names.add(node['custom_type'])
                action_string += (
                    indent(1) + 'action {' + os.linesep
                    + indent(2) + node['custom_type'] + os.linesep
                    + indent(2) + 'arguments {}' + os.linesep
                    + indent(2) + 'local_variables {}' + os.linesep
                    + indent(2) + 'read_variables {}' + os.linesep
                    + indent(2) + 'write_variables {}' + os.linesep
                    + indent(2) + 'initial_values {}' + os.linesep
                    + indent(2) + 'update {' + os.linesep
                    + indent(3) + 'return_statement {success}' + os.linesep
                    + indent(2) + '}' + os.linesep
                    + indent(1) + '}' + os.linesep
                )
                return
            if node['type'] in ('parallel', 'selector', 'sequence'):
                tree_string += (
                    indent(indent_level) + 'composite {' + os.linesep
                    + indent(indent_level + 1) + node_name + ' ' + node['type'] + (' policy success_on_all' if node['type'] == 'parallel' else '') + os.linesep
                    + indent(indent_level + 1) + 'children {' + os.linesep
                )
                for child in node['children']:
                    recursive_walk(child, indent_level + 2)
                tree_string += (
                    indent(indent_level + 1) + '}' + os.linesep
                    + indent(indent_level) + '}' + os.linesep
                )
                return
            if node['type'] == 'inverter':
                tree_string += (
                    indent(indent_level) + 'decorator {' + os.linesep
                    + indent(indent_level + 1) + node_name + ' inverter' + os.linesep
                    + indent(indent_level + 1) + 'child {' + os.linesep
                )
                for child in node['children']:
                    recursive_walk(child, indent_level + 2)
                tree_string += (
                    indent(indent_level + 1) + '}' + os.linesep
                    + indent(indent_level) + '}' + os.linesep
                )
                return
            (x_status, y_status) = node['type'].split('_is_')
            tree_string += (
                indent(indent_level) + 'decorator {' + os.linesep
                + indent(indent_level + 1) + node_name + ' X_is_Y ' + x_status + ' ' + y_status + os.linesep
                + indent(indent_level + 1) + 'child {' + os.linesep
            )
            for child in node['children']:
                recursive_walk(child, indent_level + 2)
            tree_string += (
                indent(indent_level + 1) + '}' + os.linesep
                + indent(indent_level) + '}' + os.linesep
            )
            return
        recursive_walk(root_node_name, 1)
        with open (to_file_entry.get() + '.tree', 'w', encoding = 'utf-8') as write_file:
            write_file.write(
                'configuration {}' + os.linesep
                + 'enumerations {}' + os.linesep
                + 'constants {}' + os.linesep
                + 'variables {}' + os.linesep
                + 'environment_update {}' + os.linesep
                + 'checks { ' + os.linesep
                + check_string
                + '}' + os.linesep
                + 'environment_checks { ' + os.linesep
                + env_check_string
                + '}' + os.linesep
                + 'actions { ' + os.linesep
                + action_string
                + '}' + os.linesep
                + 'sub_trees {}' + os.linesep
                + 'tree {' + os.linesep
                + tree_string
                + '}' + os.linesep
                + 'tick_prerequisite {True}' + os.linesep
                + 'specifications {}' + os.linesep
            )
        status_text.config(text = 'Exported DSL. ' + warning_string)
    def add_node():
        parent_name = parent_name_entry.get()
        if parent_name not in nodes:
            status_text.config(text = 'Parent Node: "' + parent_name + '" does not exist')
            return
        parent = nodes[parent_name]
        if parent['type'] not in ('selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running'):
            status_text.config(text = 'Cannot add children to node type: ' + parent['type'])
            return
        if parent['type'] in ('inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and len(parent['children'] > 0):
            status_text.config(text = 'Cannot add more children to node type: ' + parent['type'])
            return
        node_name = fix_name(node_name_entry.get(), nodes)
        node_custom_type = (custom_type_entry.get() if node_type_var.get() == 'Custom' else None)
        node_type = (custom_class.get() if node_type_var.get() == 'Custom' else node_type_var.get())
        nodes[node_name] = {'parent' : parent_name, 'type' : node_type, 'custom_type' : node_custom_type, 'children' : []}
        index = 0
        try:
            index = int(child_number_entry.get())
        except ValueError:
            status_text.config(text = 'Index must be integer')
            return
        if index < 0 or index >= len(parent['children']):
            nodes[parent_name]['children'].append(node_name)
        else:
            nodes[parent_name]['children'].insert(index, node_name)
        status_text.config(text = 'Added node: ' + node_name)
        return
    def change_node():
        node_name = change_name_entry.get()
        if node_name not in nodes:
            status_text.config(text = 'Current Node: "' + node_name + '" does not exist')
            return
        status_string = ''
        if var_change_name.get() == 1:
            new_name = fix_name(node_name_entry.get(), nodes)
            if nodes[node_name]['parent'] is None:
                nonlocal root_node_name
                root_node_name = new_name
            else:
                index = nodes[nodes[node_name]['parent']]['children'].index(node_name)
                nodes[nodes[node_name]['parent']]['children'][index] = new_name
            for child_name in nodes[node_name]['children']:
                nodes[child_name]['parent'] = new_name
            nodes[new_name] = nodes.pop(node_name)
            node_name = new_name
            status_string += 'Updated Name. '
        if var_change_type.get() == 1:
            node_type = (custom_type_entry.get() if node_type_var.get() == 'Custom' else node_type_var.get())
            if node_type not in ('selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and len(nodes[node_name]['children']) > 0:
                status_string += 'Cannot Change node with children to type: ' + node_type + '. '
            elif node_type in ('inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and len(nodes[node_name]['children'] > 1):
                status_string += 'Cannot Change node with this many children to type: ' + node_type + '. '
            else:
                node_custom_type = (custom_type_entry.get() if node_type_var.get() == 'Custom' else None)
                node_type = (custom_class.get() if node_type_var.get() == 'Custom' else node_type_var.get())
                nodes[node_name]['type'] = node_type
                nodes[node_name]['custom_type'] = node_custom_type
                status_string += 'Updated Type. '
        if var_change_parent.get() == 1:
            original_parent = nodes[node_name]['parent']
            parent_name = parent_name_entry.get()
            if original_parent is None:
                status_string += 'Cannot change root node parent. '
            elif parent_name not in nodes:
                status_string += 'Parent Node: "' + parent_name + '" does not exist. '
            else:
                parent = nodes[parent_name]
                if parent['type'] not in ('selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running'):
                    status_string += 'Cannot add children to node type: ' + parent['type']
                elif parent['type'] in ('inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and len(parent['children'] > 0):
                    status_string += 'Cannot add more children to node type: ' + parent['type']
                else:
                    ancestor_name = parent_name
                    error = False
                    while ancestor_name is not None:
                        if ancestor_name == node_name:
                            error = True
                            status_string += 'Node cannot be it\'s own ancestor. '
                            break
                        ancestor_name = nodes['ancestor_name']['parent']
                    if not error:
                        index = 0
                        try:
                            index = int(child_number_entry.get())
                            if index < 0 or index >= len(parent['children']):
                                nodes[parent_name]['children'].append(node_name)
                            else:
                                nodes[parent_name]['children'].insert(index, node_name)
                            nodes[original_parent]['children'].remove(node_name)
                            status_string += 'Changed Parent. '
                        except ValueError:
                            status_string += 'Index must be integer. '
        if var_change_number.get() == 1:
            original_parent = nodes[node_name]['parent']
            parent_name = parent_name_entry.get()
            if original_parent is None:
                status_string += 'Cannot change root node parent. '
            elif parent_name not in nodes:
                status_string += 'Parent Node: "' + parent_name + '" does not exist. '
            else:
                index = 0
                try:
                    index = int(child_number_entry.get())
                    nodes[parent_name]['children'].remove(node_name)
                    if index < 0 or index >= len(parent['children']):
                        nodes[parent_name]['children'].append(node_name)
                    else:
                        nodes[parent_name]['children'].insert(index, node_name)
                    status_string += 'Changed index. '
                except ValueError:
                    status_string += 'Index must be integer. '
        status_text.config(text = status_string)
        return
    def delete_node_recursive(to_delete_name):
        for child_name in nodes[to_delete_name]['children']:
            delete_node_recursive(child_name)
        nodes.pop(to_delete_name)
        return
    def delete_node():
        node_name = delete_name_entry.get()
        if node_name not in nodes:
            status_text.config(text = 'Delete Node: "' + node_name + '" does not exist')
            return
        if nodes[node_name]['parent'] is None:
            status_text.config(text = 'Cannot delete root node')
            return
        if var_delete_children.get() == 1:
            delete_node_recursive(node_name)
            nodes[nodes[node_name]['parent']]['children'].remove(node_name)
            status_text.config(text = 'Deleted node and children')
            return
        parent = nodes[nodes[node_name]['parent']]
        if parent['type'] not in ('selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and len(nodes[node_name]['children']) > 0:
            status_text.config(text = 'Deletion would add children. Cannot add children to node type: ' + parent['type'])
            return
        if parent['type'] in ('inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running') and (len(parent['children']) + len(nodes[node_name]['children'])) > 0:
            status_text.config(text = 'Deletion would add children. Cannot add more children to node type: ' + parent['type'])
            return
        parent_name = nodes[node_name]['parent']
        index = parent['children'].index(node_name)
        nodes[parent_name]['children'].remove(node_name)
        for child_name in reversed(nodes[node_name]['children']):
            nodes[child_name]['parent'] = parent_name
            nodes[parent_name]['children'].insert(index, child_name)
        nodes.pop(node_name)
        status_text.config(text = 'Deleted node: ' + node_name)
        return
    def import_dsl():
        nonlocal nodes, root_node_name, variables
        if not os.path.isfile(from_file_entry.get()):
            status_text.config(text = 'Not a file: "' + from_file_entry.get() + '"')
            return
        try:
            (nodes, variables) = dsl_to_nuxmv(
                metamodel_file = '../metamodel/behaverify.tx',
                model_file = from_file_entry.get(),
                output_file = None,
                keep_stage_0 = True,
                keep_last_stage = True,
                do_not_trim = True,
                behave_only = False,
                recursion_limit = 0,
                return_values = True,
                skip_grammar_check = True)
            root_node_name = get_root_from_BehaVerify_json(nodes)
            status_text.config(text = 'Imported DSL, root node name: ' + root_node_name)
        except Exception as error:
            print(traceback.format_exc())
            print(error)
            status_text.config(text = 'An exception occurred during Import: ' + str(error))
    def visualize_trace():
        smv_run = handle_smv(from_file_entry.get())
        previous_value = {}
        previous_status = {}
        previous_misc = {}
        # ../examples/simple_robot/tree/CHANGED_simple_robot_2.tree
        # ../examples/simple_robot/results/LTL_full_opt_CHANGED_simple_robot_2.txt
        for (tick_number, state) in enumerate(smv_run):
            dot = create_dot_from_BehaVerify_json(nodes, root_node_name, output_file = to_file_entry.get() + '/' + str(tick_number), detailed_nodes = (True if var_detailed_nodes.get() == 1 else 0))
            nodes_to_status = {}
            nodes_to_var_values = {}
            misc_var_values = []
            seen_variables = set()
            for node_or_var_name in state:
                if node_or_var_name in nodes:
                    nodes_to_status[node_or_var_name] = state[node_or_var_name]
                else:
                    for stage in state[node_or_var_name]:
                        string_to_add = node_or_var_name + '_stage_' + str(stage) + ' := ' + state[node_or_var_name][stage]
                        if node_or_var_name not in variables or stage == 0:
                            misc_var_values.append(string_to_add)
                            seen_variables.add(node_or_var_name + '_stage_' + str(stage))
                            previous_misc[node_or_var_name + '_stage_' + str(stage)] = string_to_add
                        elif len(variables[node_or_var_name]['next_value']) >= stage:
                            node_name = variables[node_or_var_name]['next_value'][stage - 1][0]
                            if node_name not in nodes_to_var_values:
                                nodes_to_var_values[node_name] = []
                            nodes_to_var_values[node_name].append(string_to_add)
                        else:
                            misc_var_values.append(string_to_add)
                            seen_variables.add(node_or_var_name + '_stage_' + str(stage))
                            previous_misc[node_or_var_name + '_stage_' + str(stage)] = string_to_add
            for var_name in previous_misc:
                if var_name in seen_variables:
                    continue
                misc_var_values.append(previous_misc[var_name])
            for node_name in nodes:
                node_status = nodes_to_status[node_name] if node_name in nodes_to_status else previous_status[node_name]
                node_info = (
                    (node_status + os.linesep + (os.linesep).join(sorted(nodes_to_var_values[node_name])))
                    if node_name in nodes_to_var_values else
                    node_status
                )
                dot.node(node_name + '_INFO', label = node_info, shape = 'plaintext', fontcolor = STATUS_COLORS[node_status])
                dot.edge(node_name, node_name + '_INFO')
                previous_value[node_name] = node_info
                previous_status[node_name] = node_status
            dot.node('MISC_INFO', label = (os.linesep).join(sorted(misc_var_values)), shape = 'note', fontcolor = '#000000')
            dot.render()
        return

    nodes = {'root' : {'parent' : None, 'type' : 'selector', 'custom_type' : None, 'children' : []}}
    root_node_name = 'root'
    variables = {}

    root = tkinter.Tk()
    root.title('BehaVerify Tree Visualizer')

    status_text = ttk.Label(root, text = 'Default Loaded')
    status_text.grid(column = 0, row = 0, sticky = tkinter.W)

    ########################################################################

    state_frame = ttk.Frame(root, padding = 5)
    state_frame.grid(column = 0, row = 1, sticky = tkinter.W)

    load_json_button = ttk.Button(state_frame, text='Import JSON', command = import_json)
    load_json_button.grid(column=0, row=0)

    save_json_button = ttk.Button(state_frame, text='Export JSON', command = export_json)
    save_json_button.grid(column=1, row=0)

    visualize_button = ttk.Button(state_frame, text='Visualize', command = visualize)
    visualize_button.grid(column=2, row=0)

    import_dsl_button = ttk.Button(state_frame, text='Import DSL', command = import_dsl)
    import_dsl_button.grid(column=3, row=0)

    export_dsl_button = ttk.Button(state_frame, text='Export DSL Template', command = export_dsl)
    export_dsl_button.grid(column=4, row=0)

    visualize_button = ttk.Button(state_frame, text='Visualize Trace', command = visualize_trace)
    visualize_button.grid(column=5, row=0)

    var_detailed_nodes = tkinter.IntVar()

    detailed_nodes_button = ttk.Checkbutton(state_frame, text = 'Detailed Nodes', variable = var_detailed_nodes, onvalue = 1, offvalue = 0)
    detailed_nodes_button.grid(column = 6, row = 0)

    ########################################################################

    from_file_frame = ttk.Frame(root, padding = 5)
    from_file_frame.grid(column = 0, row = 2, sticky = tkinter.W)

    from_file_label = ttk.Label(from_file_frame, text='From File:')
    from_file_label.grid(column = 0, row = 0, sticky = tkinter.E)

    from_file_entry = ttk.Entry(from_file_frame)
    from_file_entry.grid(column = 1, row = 0)

    ########################################################################

    to_file_frame = ttk.Frame(root, padding = 5)
    to_file_frame.grid(column = 0, row = 3, sticky = tkinter.W)

    to_file_label = ttk.Label(to_file_frame, text='To File (no extension):')
    to_file_label.grid(column = 0, row = 0, sticky = tkinter.E)

    to_file_entry = ttk.Entry(to_file_frame)
    to_file_entry.grid(column = 1, row = 0)

    ########################################################################

    add_node_frame = ttk.Frame(root, padding = 5)
    add_node_frame.grid(column = 0, row = 4, sticky = tkinter.W)

    add_node_button = ttk.Button(add_node_frame, text='Add Node', command = add_node)
    add_node_button.grid(column=0, row=0)

    add_node_frame1 = ttk.Frame(add_node_frame, padding = 5)
    add_node_frame1.grid(column = 1, row = 0, sticky = tkinter.W)

    node_type_label = ttk.Label(add_node_frame1, text='Node Type:')
    node_type_label.grid(column = 0, row = 0, sticky = tkinter.E)

    node_type_var = tkinter.StringVar()
    node_type_var.set('Custom')  # Default node type

    node_type_selector = ttk.OptionMenu(add_node_frame1, node_type_var, 'Custom', 'Custom', 'selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running')
    node_type_selector.grid(column = 1, row = 0)

    custom_type_frame = ttk.Frame(add_node_frame1, padding = 1)
    custom_type_frame.grid(column=2, row=0, sticky = tkinter.W)

    custom_type_label = ttk.Label(custom_type_frame, text='Custom Type:')
    custom_type_label.grid(column = 0, row = 1, sticky = tkinter.W)

    custom_class = tkinter.StringVar()
    custom_class.set('action')

    custom_class_radio1 = ttk.Radiobutton(custom_type_frame, variable = custom_class, text = 'Action', value = 'action')
    custom_class_radio1.grid(column = 1, row = 0, sticky = tkinter.W)

    custom_class_radio2 = ttk.Radiobutton(custom_type_frame, variable = custom_class, text = 'Check', value = 'check')
    custom_class_radio2.grid(column = 1, row = 1, sticky = tkinter.W)

    custom_class_radio3 = ttk.Radiobutton(custom_type_frame, variable = custom_class, text = 'Env Check', value = 'environment_check')
    custom_class_radio3.grid(column = 1, row = 2, sticky = tkinter.W)

    custom_type_entry = ttk.Entry(custom_type_frame)
    custom_type_entry.grid(column = 2, row = 1)

    add_node_frame2 = ttk.Frame(add_node_frame, padding = 5)
    add_node_frame2.grid(column = 1, row = 1, sticky = tkinter.W)

    node_name_label = ttk.Label(add_node_frame2, text='Node Name:')
    node_name_label.grid(column = 0, row = 0, sticky = tkinter.E)

    node_name_entry = ttk.Entry(add_node_frame2)
    node_name_entry.grid(column = 1, row = 0, sticky = tkinter.W)

    parent_name_label = ttk.Label(add_node_frame2, text='Parent Name:')
    parent_name_label.grid(column = 2, row = 0, sticky = tkinter.E)

    parent_name_entry = ttk.Entry(add_node_frame2)
    parent_name_entry.grid(column = 3, row = 0, sticky = tkinter.W)

    child_number_label = ttk.Label(add_node_frame2, text='Child Number (-1 for Last):')
    child_number_label.grid(column = 4, row = 0, sticky = tkinter.E)

    child_number_entry = ttk.Entry(add_node_frame2)
    child_number_entry.grid(column = 5, row = 0, sticky = tkinter.W)

    ########################################################################

    change_node_frame = ttk.Frame(root, padding = 5)
    change_node_frame.grid(column = 0, row = 5, sticky = tkinter.W)

    change_node_button = ttk.Button(change_node_frame, text='Change Node', command = change_node)
    change_node_button.grid(column = 0, row = 0)

    change_name_label = ttk.Label(change_node_frame, text='Current Name:')
    change_name_label.grid(column = 1, row = 0, sticky = tkinter.E)

    change_name_entry = ttk.Entry(change_node_frame)
    change_name_entry.grid(column = 2, row = 0, sticky = tkinter.W)

    var_change_name = tkinter.IntVar()
    var_change_type = tkinter.IntVar()
    var_change_parent = tkinter.IntVar()
    var_change_number = tkinter.IntVar()

    change_name_button = ttk.Checkbutton(change_node_frame, text = 'Change Name', variable = var_change_name, onvalue = 1, offvalue = 0)
    change_name_button.grid(column = 3, row = 0)

    change_type_button = ttk.Checkbutton(change_node_frame, text = 'Change Type', variable = var_change_type, onvalue = 1, offvalue = 0)
    change_type_button.grid(column = 4, row = 0)

    change_parent_button = ttk.Checkbutton(change_node_frame, text = 'Change Parent', variable = var_change_parent, onvalue = 1, offvalue = 0)
    change_parent_button.grid(column = 5, row = 0)

    change_number_button = ttk.Checkbutton(change_node_frame, text = 'Change Number', variable = var_change_number, onvalue = 1, offvalue = 0)
    change_number_button.grid(column = 6, row = 0)

    ########################################################################

    delete_node_frame = ttk.Frame(root, padding = 5)
    delete_node_frame.grid(column = 0, row = 6, sticky = tkinter.W)

    delete_node_button = ttk.Button(delete_node_frame, text='Delete Node', command = delete_node)
    delete_node_button.grid(column=0, row=0)

    delete_name_label = ttk.Label(delete_node_frame, text='To Delete Name:')
    delete_name_label.grid(column = 1, row = 0, sticky = tkinter.E)

    delete_name_entry = ttk.Entry(delete_node_frame)
    delete_name_entry.grid(column = 2, row = 0)

    var_delete_children = tkinter.IntVar()

    delete_children_button = ttk.Checkbutton(delete_node_frame, text = 'Delete Children', variable = var_delete_children, onvalue = 1, offvalue = 0)
    delete_children_button.grid(column = 3, row = 0)

    root.mainloop()

if __name__ == '__main__':
    main()
