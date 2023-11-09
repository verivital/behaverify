'''
Module for visualizing Behavior Trees
'''
import os
import json
import tkinter
from tkinter import ttk
import graphviz
from dsl_to_nuxmv import dsl_to_nuxmv

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
    node_type = node['type']
    base_name = node.get('name', node_type)
    node_name = fix_name(base_name, nodes)
    nodes[node_name] = 'temp'
    children = []
    if 'children' in node:
        for child in node['children']:
            (child_name, nodes) = chatGPT_json_to_BehaVerify_json(child, node_name, nodes)
            children.append(child_name)
    nodes[node_name] = {'parent' : parent_name, 'type' : node_type, 'children' : children}
    return (node_name, nodes)

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

def create_dot_from_BehaVerify_json(nodes, root_node_name, output_file = 'behavior_tree'):
    dot = graphviz.Digraph(format='png', filename=output_file)
    def process_node(node_name):
        node = nodes[node_name]
        node_type = node['type']
        parent_name = node['parent']
        node_label = node_name if node_type in SHAPES else (node_name + os.linesep + node_type)
        dot.node(node_name, label = node_label, style = 'filled', fillcolor = COLORS.get(node_type, '#C0C0C0'), shape = SHAPES.get(node_type, 'oval'))
        if parent_name is not None:
            dot.edge(parent_name, node_name)
        for child in node['children']:
            process_node(child)
    process_node(root_node_name)
    return dot

def visualize_BehaVerify_json(nodes, root_node_name, output_file = 'behavior_tree', mode = 'render'):
    dot = create_dot_from_BehaVerify_json(nodes, root_node_name, output_file)
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

    def load_json():
        nonlocal root_node_name, nodes
        try:
            with open(from_file_entry.get(), 'r', encoding = 'utf-8') as input_file:
                behavior_tree_json = json.load(input_file)
            if json_type.get() == 'Recursive Json':
                (root_node_name, nodes) = chatGPT_json_to_BehaVerify_json(behavior_tree_json)
            else:
                nodes = behavior_tree_json
                root_node_name = get_root_from_BehaVerify_json(nodes)
            status_text.config(text = 'Loaded Json, root node name: ' + root_node_name)
        except:
            status_text.config(text = 'An exception occurred during Loading')
    def save_json():
        nonlocal nodes
        try:
            with open(to_file_entry.get() + '.json', 'w', encoding = 'utf-8') as input_file:
                json.dump(nodes, input_file)
            status_text.config(text = 'Saved Json, root node name: ' + root_node_name)
        except:
            status_text.config(text = 'An exception occurred during Saving')
    def visualize():
        if len(nodes) == 0:
            status_text.config(text = 'You must Load Json before Visualizing')
            return
        try:
            visualize_BehaVerify_json(nodes, root_node_name, output_file = to_file_entry.get(), mode = 'view')
            status_text.config(text = 'Visualization finished. root node name: ' + root_node_name)
        except Exception as cur_exception:
            status_text.config(text = 'An exception occurred during Visualization: ' + str(cur_exception))
    def export_dsl():
        status_text.config(text = 'EXPORT DSL NOT IMPLEMENTED. root node name: ' + root_node_name)
    def add_node():
        if len(nodes) == 0:
            status_text.config(text = 'You must Load Json before adding nodes')
            return
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
        node_type = (custom_type_entry.get() if node_type_var.get() == 'Custom' else node_type_var.get())
        nodes[node_name] = {'parent' : parent_name, 'type' : node_type, 'children' : []}
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
        if len(nodes) == 0:
            status_text.config(text = 'You must Load Json before changing nodes')
            return
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
                nodes[node_name]['type'] = node_type
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
        if len(nodes) == 0:
            status_text.config(text = 'You must Load Json before changing nodes')
            return
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
        try:
            (nodes, variables) = dsl_to_nuxmv('../metamodel/behaverify.tx', from_file_entry.get(), None, False, False, False, None, 0, True)
            root_node_name = get_root_from_BehaVerify_json(nodes)
            status_text.config(text = 'Imported DSL, root node name: ' + root_node_name)
        except Exception as error:
            status_text.config(text = 'An exception occurred during Import: ' + str(error))
    def visualize_trace():
        smv_run = handle_smv(from_file_entry.get())
        for (tick_number, state) in enumerate(smv_run):
            dot = create_dot_from_BehaVerify_json(nodes, root_node_name, output_file = to_file_entry.get() + '/' + str(tick_number))
            nodes_to_status = {}
            nodes_to_var_values = {}
            misc_var_values = []
            for node_or_var_name in state:
                if node_or_var_name in nodes:
                    nodes_to_status[node_or_var_name] = state[node_or_var_name]
                else:
                    for stage in state[node_or_var_name]:
                        string_to_add = node_or_var_name + '_stage_' + str(stage) + ' := ' + state[node_or_var_name][stage]
                        if node_or_var_name not in variables or stage == 0:
                            misc_var_values.append(string_to_add)
                        elif len(variables[node_or_var_name]['next_value']) >= stage:
                            node_name = variables[node_or_var_name]['next_value'][stage - 1][0]
                            if node_name not in nodes_to_var_values:
                                nodes_to_var_values[node_name] = []
                            nodes_to_var_values[node_name].append(string_to_add)
                        else:
                            misc_var_values.append(string_to_add)
            for node_name in nodes:
                node_info = (nodes_to_status[node_name] + os.linesep + (os.linesep).join(sorted(nodes_to_var_values[node_name]))) if node_name in nodes_to_var_values else nodes_to_status[node_name]
                dot.node(node_name + '_INFO', label = node_info, shape = 'plaintext', fontcolor = 'blue')
                dot.edge(node_name, node_name + '_INFO')
            dot.node('MISC_INFO', label = (os.linesep).join(sorted(misc_var_values)), shape = 'note', fontcolor = 'red')
            dot.render()
        return

    #../examples/ANSR_ONNX/ANSR_ONNX.tree
    #../examples/ANSR_ONNX/smv/trace.txt
    nodes = {}
    root_node_name = None
    variables = {}

    root = tkinter.Tk()
    root.title('Dot Graph Viewer')


    frame = ttk.Frame(root, padding=10)
    frame.grid(column=0, row=0)

    status_text = ttk.Label(frame, text = 'Nothing Loaded')
    status_text.grid(column = 0, row = 0)

    ########################################################################

    load_json_button = ttk.Button(frame, text='Load JSON', command = load_json)
    load_json_button.grid(column=0, row=1)

    save_json_button = ttk.Button(frame, text='Save JSON', command = save_json)
    save_json_button.grid(column=1, row=1)

    visualize_button = ttk.Button(frame, text='Visualize', command = visualize)
    visualize_button.grid(column=2, row=1)

    import_dsl_button = ttk.Button(frame, text='Import DSL', command = import_dsl)
    import_dsl_button.grid(column=3, row=1)

    export_dsl_button = ttk.Button(frame, text='Export DSL', command = export_dsl)
    export_dsl_button.grid(column=4, row=1)

    visualize_button = ttk.Button(frame, text='Visualize Trace', command = visualize_trace)
    visualize_button.grid(column=5, row=1)

    ########################################################################

    from_file_label = ttk.Label(frame, text='From File:')
    from_file_label.grid(column = 0, row = 2)

    from_file_entry = ttk.Entry(frame)
    from_file_entry.grid(column = 1, row = 2)

    json_type = tkinter.StringVar()
    json_type.set('Recursive Json')  # Default node type

    json_type_selector = ttk.OptionMenu(frame, json_type, 'Recursive Json', 'Recursive Json', 'Reference Json')
    json_type_selector.grid(column = 2, row = 2)

    ########################################################################

    to_file_label = ttk.Label(frame, text='To File (no extension):')
    to_file_label.grid(column = 0, row = 3)

    to_file_entry = ttk.Entry(frame)
    to_file_entry.grid(column = 1, row = 3)

    ########################################################################

    add_node_button = ttk.Button(frame, text='Add Node', command = add_node)
    add_node_button.grid(column=0, row=4)

    node_type_label = ttk.Label(frame, text='Node Type:')
    node_type_label.grid(column = 1, row = 4)

    node_type_var = tkinter.StringVar()
    node_type_var.set('Custom')  # Default node type

    node_type_selector = ttk.OptionMenu(frame, node_type_var, 'Custom', 'selector', 'sequence', 'parallel', 'inverter', 'success_is_failure', 'success_is_running', 'running_is_failure', 'running_is_success', 'failure_is_success', 'failure_is_running')
    node_type_selector.grid(column = 2, row = 4)

    custom_type_label = ttk.Label(frame, text='Custom Type:')
    custom_type_label.grid(column = 3, row = 4)

    custom_type_entry = ttk.Entry(frame)
    custom_type_entry.grid(column = 4, row = 4)

    node_name_label = ttk.Label(frame, text='Node Name:')
    node_name_label.grid(column = 5, row = 4)

    node_name_entry = ttk.Entry(frame)
    node_name_entry.grid(column = 6, row = 4)

    parent_name_label = ttk.Label(frame, text='Parent Name:')
    parent_name_label.grid(column = 1, row = 5)

    parent_name_entry = ttk.Entry(frame)
    parent_name_entry.grid(column = 2, row = 5)

    child_number_label = ttk.Label(frame, text='Child Number (-1 for Last):')
    child_number_label.grid(column = 3, row = 5)

    child_number_entry = ttk.Entry(frame)
    child_number_entry.grid(column = 4, row = 5)

    ########################################################################

    change_node_button = ttk.Button(frame, text='Change Node', command = change_node)
    change_node_button.grid(column=0, row=6)

    change_name_label = ttk.Label(frame, text='Current Name:')
    change_name_label.grid(column = 1, row = 6)

    change_name_entry = ttk.Entry(frame)
    change_name_entry.grid(column = 2, row = 6)

    var_change_name = tkinter.IntVar()
    var_change_type = tkinter.IntVar()
    var_change_parent = tkinter.IntVar()
    var_change_number = tkinter.IntVar()

    change_name_button = ttk.Checkbutton(frame, text = 'Change Name', variable = var_change_name, onvalue = 1, offvalue = 0)
    change_name_button.grid(column = 3, row = 6)

    change_type_button = ttk.Checkbutton(frame, text = 'Change Type', variable = var_change_type, onvalue = 1, offvalue = 0)
    change_type_button.grid(column = 4, row = 6)

    change_parent_button = ttk.Checkbutton(frame, text = 'Change Parent', variable = var_change_parent, onvalue = 1, offvalue = 0)
    change_parent_button.grid(column = 5, row = 6)

    change_number_button = ttk.Checkbutton(frame, text = 'Change Number', variable = var_change_number, onvalue = 1, offvalue = 0)
    change_number_button.grid(column = 6, row = 6)

    ########################################################################

    delete_node_button = ttk.Button(frame, text='Delete Node', command = delete_node)
    delete_node_button.grid(column=0, row=7)

    delete_name_label = ttk.Label(frame, text='To Delete Name:')
    delete_name_label.grid(column = 1, row = 7)

    delete_name_entry = ttk.Entry(frame)
    delete_name_entry.grid(column = 2, row = 7)

    var_delete_children = tkinter.IntVar()

    delete_children_button = ttk.Checkbutton(frame, text = 'Delete Children', variable = var_delete_children, onvalue = 1, offvalue = 0)
    delete_children_button.grid(column = 3, row = 7)

    root.mainloop()

if __name__ == '__main__':
    main()
