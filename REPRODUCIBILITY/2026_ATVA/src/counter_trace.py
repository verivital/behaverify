'''
Module for visualizing Behavior Trees

Author: Serena Serafina Serbinowska
Last Edit: 2025-05-06
'''
import argparse
import os
# import json
import traceback
import graphviz
from dsl_to_nuxmv import dsl_to_nuxmv
# from behaverify_common import BTreeException, indent


def split_file(trace_file_string):
    traces = []
    with open(trace_file_string, 'r', encoding = 'utf-8') as trace_file:
        lines = []
        for line in trace_file:
            if line[0] != ' ':
                continue
            if line.strip() == '':
                continue
            if 'State: ' in line:
                if '.1 <-' in line:
                    if len(lines) > 0:
                        traces.append(lines)
                    lines = []
            lines.append(line)
    if len(lines) > 0:
        traces.append(lines)
    return traces

def handle_smv(trace):
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
    ignore = True
    for line in trace:
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

def main(metamodel_file, model_file, trace_file, output_folder, var_detailed_nodes = False):
    def import_dsl():
        nonlocal nodes, root_node_name, variables
        if not os.path.isfile(model_file):
            print('MODEL NOT FOUND: ' + model_file)
            return
        try:
            (nodes, variables) = dsl_to_nuxmv(
                metamodel_file = metamodel_file,
                model_file = model_file,
                output_file = None,
                keep_stage_0 = True,
                keep_last_stage = True,
                do_not_trim = True,
                behave_only = False,
                recursion_limit = 0,
                return_values = True,
                skip_grammar_check = True,
                record_times = None
            )
            root_node_name = get_root_from_BehaVerify_json(nodes)
        except Exception as error:
            print(traceback.format_exc())
            print(error)
    def visualize_trace():
        all_traces = split_file(trace_file)
        for (trace_index, trace) in enumerate(all_traces):
            smv_run = handle_smv(trace)
            previous_value = {}
            previous_status = {}
            previous_misc = {}
            # ../examples/simple_robot/tree/CHANGED_simple_robot_2.tree
            # ../examples/simple_robot/results/LTL_full_opt_CHANGED_simple_robot_2.txt
            for (tick_number, state) in enumerate(smv_run):
                dot = create_dot_from_BehaVerify_json(nodes, root_node_name, output_file = output_folder + '/' + str(trace_index) + '_' + str(tick_number), detailed_nodes = var_detailed_nodes)
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
    import_dsl()
    visualize_trace()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('metamodel_file')
    arg_parser.add_argument('model_file')
    arg_parser.add_argument('trace_file')
    arg_parser.add_argument('output_folder')
    args = arg_parser.parse_args()
    main(args.metamodel_file, args.model_file, args.trace_file, args.output_folder)
