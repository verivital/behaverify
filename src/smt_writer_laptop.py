
# arg_parser.add_argument('input_file')
# arg_parser.add_argument('--blackboard_input_file', default = None)
# arg_parser.add_argument('--module_input_file', default = None)
# arg_parser.add_argument('--specs_input_file', default = None)
# arg_parser.add_argument('--output_file', default = None)
# arg_parser.add_argument('--blackboard_output_file', default = None)
# arg_parser.add_argument('--module_output_file', default = None)
# arg_parser.add_argument('--overwrite', action = 'store_true')

#-----------------------------------------------------------------------------------------------------------------------
import argparse
import py_trees
import sys
import time
import os
import re
import inspect
import json
#----------------------------------------------------------------------------------------------------------------
import py_trees.console as console
import node_creator
import compute_resume_info


##############################################################################
# Main
##############################################################################

def main():
    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('--blackboard_input_file', default = None)
    arg_parser.add_argument('--module_input_file', default = None)
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--blackboard_output_file', default = None)
    arg_parser.add_argument('--module_output_file', default = None)
    #arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']
    
    node_to_local_root_map = compute_resume_info.create_node_to_local_root_map(nodes)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = compute_resume_info.create_local_root_to_relevant_list_map(nodes, node_to_local_root_map)
    node_to_descendants_map = compute_resume_info.create_node_to_descendants_map(nodes)

    for node_id in nodes:
        node = nodes[node_id]
        parent_id = node['parent']
        if parent_id == -1:
            #this is the root. do nothing
            continue
        parent = nodes[parent_id]
        if parent['children'][0] == node_id:
            #this is the first child
            #no left neighbor
            node['left_neighbor'] = None
        else:
            node_index = parent['children'].index(node_id)
            node['left_neigbor'] = parent['children'][node_index - 1]

    #------------------------------------------------------------------------------------------------------------------------
    #done with variable decleration, moving into string building.

    smt_node_string = ''
    

    for node_id in nodes:
        node = nodes[node_id]
        first_child = True
        for child_id in node['children']:
            child = nodes[child_id]
            if first_child:
                #TODO: handle cases where we have memory and it is skippable
                smt_node_string += '(assert (= (= ' + child['name'] + ' invalid) (= ' + node['name'] + ' invalid)))' + os.linesep
            else:
                if node['type'] == 'selector_without_memory':
                    smt_node_string += '(assert (= (= ' + child['name'] + 'not(invalid)) (= ' + previous_child['name'] + ' failure)))' + os.linesep
                elif node['type'] == 'sequence_without_memory':
                    smt_node_string += '(assert (= (= ' + child['name'] + 'not(invalid)) (= ' + previous_child['name'] + ' success)))' + os.linesep
                elif 'parallel_unsynchronized' in node['type']:
                    smt_node_string += '(assert (= (= ' + child['name'] + 'invalid) (= ' + node['name'] + ' invalid)))' + os.linesep
            previous_child = child

    if args.output_file is None:
        print(nuxmv_string)
    else:
        with open(args.output_file, 'w') as f:
            f.write(nuxmv_string)
    
    
    return
    

main()
