
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
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    #arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']
    
    node_to_local_root_map = compute_resume_info.create_node_to_local_root_map(nodes)
    (local_root_to_relevant_list_map, nodes_with_memory_to_relevant_descendants_map) = compute_resume_info.create_local_root_to_relevant_list_map(nodes, node_to_local_root_map)
    node_to_descendants_map = compute_resume_info.create_node_to_descendants_map(nodes)


    use_valid = False
    
    #------------------------------------------------------------------------------------------------------------------------
    #done with variable decleration, moving into string building.

    recursion_stack = [0]#0 is the root.
    nodes_seen = set()

    while len(recursion_stack) > 0:
        node_id = recursion_stack.pop()
        if 'smt' in nodes[node_id]:
            continue
        first = True
        if node_id not in nodes_seen:
            for child_id in nodes[node_id]['children']:
                if 'smt' in nodes[child_id]:
                    continue
                elif first:
                    recursion_stack.append(node_id)
                    recursion_stack.append(child_id)
                    first = False
                else:
                    recursion_stack.append(child_id)
        nodes_seen.add(node_id)
        if first:
            node = nodes[node_id]
            if node['type'] == 'selector_without_memory':
                node['success_smt'] = '(or'
                node['failure_smt'] = '(and'
                node['running_smt'] = '(or'
                first = True
                for child_id in node['children']:
                    child = nodes[child_id]
                    node['success_smt'] += ' ' + child['success_smt']
                    node['failure_smt'] += ' ' + child['failure_smt']
                    node['running_smt'] += ' ' + child['running_smt']
                node['success_smt'] += ')'
                node['failure_smt'] += ')'
                node['running_smt'] += ')'
            elif node['type'] == 'sequence_without_memory':
                node['success_smt'] = '(and'
                node['failure_smt'] = '(or'
                node['running_smt'] = '(or'
                for child_id in node['children']:
                    child = nodes[child_id]
                    node['success_smt'] += ' ' + child['success_smt']
                    node['failure_smt'] += ' ' + child['failure_smt']
                    node['running_smt'] += ' ' + child['running_smt']
                node['success_smt'] += ')'
                node['failure_smt'] += ')'
                node['running_smt'] += ')'
            else:
                #for now assuming this is a leaf node. this will probably need to be expanded into something like the node_creator file
                node['smt_create'] = ('(declare-const ' + node['name'] + 'S Bool)' + os.linesep
                                      + '(declare-const ' + node['name'] + 'F Bool)' + os.linesep
                                      )
                node['success_smt'] = '(and ' + node['name'] + 'S (not ' + node['name'] + 'F))'
                node['failure_smt'] = '(and ' + node['name'] + 'F (not ' + node['name'] + 'S))'
                node['running_smt'] = '(and ' + node['name'] + 'S ' + node['name'] + 'F)'
    nodes[0]['valid_smt'] = 'true'
    for node_id in nodes:
        node = nodes[node_id]
        if node['type'] == 'selector_without_memory':
            first = True
            for child_id in node['children']:
                if first:
                    nodes[child_id]['valid_smt'] = node['valid_smt']
                    first = False
                else:
                    nodes[child_id]['valid_smt'] = nodes[prev_child]['failure_smt']
                prev_child = child_id
        elif node['type'] == 'sequence_without_memory':
            first = True
            for child_id in node['children']:
                if first:
                    nodes[child_id]['valid_smt'] = node['valid_smt']
                    first = False
                else:
                    nodes[child_id]['valid_smt'] = nodes[prev_child]['success_smt']
                prev_child = child_id

    smt_declarations = ''
    smt_assertions = ''
    for node_id in nodes:
        if 'smt_create' in nodes[node_id]:
            smt_declarations += nodes[node_id]['smt_create']
        smt_assertions += '(assert (= ' + nodes[node_id]['valid_smt'] + ' (or ' + nodes[node_id]['success_smt'] + ' ' + nodes[node_id]['running_smt'] + ' ' + nodes[node_id]['failure_smt'] + ')))' + os.linesep

    smt_string = ('(set-option :print-success false)' + os.linesep
                  + '(set-logic QF_UF)' + os.linesep
                  + os.linesep
                  + smt_declarations
                  + os.linesep
                  + smt_assertions
                  + os.linesep
                  + '(check-sat)' + os.linesep
                  + '(exit)' + os.linesep
                  )
                                                         
    if args.output_file is None:
        print(smt_string)
    else:
        with open(args.output_file, 'w') as f:
            f.write(smt_string)
    
    
    return
    

main()
