import tkinter
from tkinter import ttk
import graphviz
import json


def fix_name(base_name, nodes):
    node_name = base_name
    count = 1
    while node_name in nodes:
        node_name = base_name + '.' + str(count)
        count = count + 1
    return node_name

def chatGPT_json_to_BehaVerify_json(node, parent_name = None, nodes = None):
    if nodes is None:
        nodes = {}
    node_type = node['type']
    base_name = node.get('name', node_type)
    node_name = fix_name(base_name, nodes)
    children = []
    if 'children' in node:
        for child in node['children']:
            (child_name, nodes) = chatGPT_json_to_BehaVerify_json(child, node_name, nodes)
            children.append(child_name)
    nodes[node_name] = {'parent' : parent_name, 'type' : node_type, 'children' : children}
    return (node_name, nodes)

def visualize_BehaVerify_json(nodes, root_node_name, output_file = 'behavior_tree', mode = 'render'):
    # Create a Graphviz Digraph object
    dot = graphviz.Digraph(format='png', filename=output_file)

    def process_node(node_name):
        node = nodes[node_name]
        node_type = node['type']
        parent_name = node['parent']
        dot.node(node_name, label = node_name, shape = (
            'star'
            if node_type == 'selector' else
            'egg'
        )
                 )
        if parent_name is not None:
            dot.edge(parent_name, node_name)
        for child in node['children']:
            process_node(child)
    process_node(root_node_name)
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
        node_type = (node_name_entry.get() if node_type_var.get() == 'Custom' else node_type_var.get())
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
            node_type = (node_name_entry.get() if node_type_var.get() == 'Custom' else node_type_var.get())
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

    nodes = {}
    root_node_name = None

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

    export_dsl_button = ttk.Button(frame, text='Export DSL', command = export_dsl)
    export_dsl_button.grid(column=3, row=1)
    
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

    node_name_label = ttk.Label(frame, text='Node Name/Custom Type:')
    node_name_label.grid(column = 3, row = 4)

    node_name_entry = ttk.Entry(frame)
    node_name_entry.grid(column = 4, row = 4)

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
