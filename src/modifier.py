import argparse
import sys
import os
import re
import pprint
#----------------------------------------------------------------------------------------------------------------
#todo: add a way to delete variables and change access

def main():

    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('input_file') 
    arg_parser.add_argument('--output_file', default = None)
    
    arg_parser.add_argument('--interactive_mode', action = 'store_true')
    arg_parser.add_argument('--instruction_file', action = 'store_true')
    
    arg_parser.add_argument('--force_parallel_unsynch', action = 'store_true')
    arg_parser.add_argument('--force_parallel_synch', action = 'store_true')
    arg_parser.add_argument('--force_selector_memory', action = 'store_true')
    arg_parser.add_argument('--force_selector_memoryless', action = 'store_true')
    arg_parser.add_argument('--force_sequence_memory', action = 'store_true')
    arg_parser.add_argument('--force_sequence_memoryless', action = 'store_true')
    
    arg_parser.add_argument('--min_value', default = None)
    arg_parser.add_argument('--max_value', default = None)
    arg_parser.add_argument('--init_value', default = None)
    arg_parser.add_argument('--no_init_value', action = 'store_true')
    arg_parser.add_argument('--next_value', default = None)
    arg_parser.add_argument('--no_next_value', action = 'store_true')
    arg_parser.add_argument('--use_global_value', action = 'store_true')
    arg_parser.add_argument('--use_individual_value', action = 'store_true')
    arg_parser.add_argument('--always_exist', action = 'store_true')
    arg_parser.add_argument('--sometimes_exist', action = 'store_true')
    arg_parser.add_argument('--init_exist', default = None)
    arg_parser.add_argument('--no_init_exist', action = 'store_true')
    arg_parser.add_argument('--next_exist', default = None)
    arg_parser.add_argument('--no_next_exist', action = 'store_true')
    
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']

    if args.force_parallel_synch:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'parallel_synchronized' in node['type']:
                node['type'] = node['type'].replace('_synchronized', '_unsynchronized')
    if args.force_parallel_unsynch:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'parallel_unsynchronized' in node['type']:
                node['type'] = node['type'].replace('_unsynchronized', '_synchronized')
    if args.force_selector_memory:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'selector_without_memory' == node['type']:
                node['type'] = 'selector_with_memory'
    if args.force_selector_memoryless:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'selector_with_memory' == node['type']:
                node['type'] = 'selector_without_memory'
    if args.force_sequence_memory:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'sequence_without_memory' == node['type']:
                node['type'] = 'sequence_with_memory'
    if args.force_sequence_memoryless:
        for node_id in nodes:
            node = nodes[node_id]
            if node['category'] == 'composite' and 'sequence_with_memory' == node['type']:
                node['type'] = 'sequence_without_memory'


    for variable_name in variables:
        variable = variables[variable_name]
        if args.min_value:
            variable['min_val'] = int(args.min_value)
        if args.max_value:
            variable['max_val'] = int(args.max_value)
        if args.init_value:
            variable['init_val'] = int(args.init_value)
        if args.no_init_value:
            variable['init_val'] = None
        if args.next_value:
            variable['global_next_value'] = args.next_value
        if args.no_next_value:
            variable['global_next_value'] = None
        if args.use_global_value:
            variable['global_next_mode'] = True
        if args.use_individual_value:
            variable['global_next_mode'] = False
        if args.always_exist:
            variable['always_exists'] = True
    arg_parser.add_argument('--always_exist', action = 'store_true')
    arg_parser.add_argument('--sometimes_exist', action = 'store_true')
    arg_parser.add_argument('--init_exist', default = None)
    arg_parser.add_argument('--no_init_exist', action = 'store_true')
    arg_parser.add_argument('--next_exist', default = None)
    arg_parser.add_argument('--no_next_exist', action = 'store_true')
        
    if args.interactive_mode:
        done = False
        while not done:
            modify_nodes = input("Modify nodes? (Enter y for yes, n for no)")
            if modify_nodes == "y":
                done = True
                for node in nodes:
                    done2 = False
                    while not done2:
                        print(nodes[node])
                        modify_node = input("Modify this node? (Enter y for yes, n for no)")
                        if modify_node == 'y':
                            modify_key = input("Enter key to modify: ")
                            try:
                                print("current value: " + str(nodes[node][modify_key]))
                                modify_value = input("Enter new value: ")
                                nodes[node][modify_key] = modify_value
                            except KeyValueError:
                                print(modify_key + " is not a valid key")
                        elif modify_node == 'n':
                            done2 = True
                        else:
                            print('input was not y or n')
            elif modify_nodes == "n":
                done = True
            else:
                print('input was not y or n')
        
        done = False
        while not done:
            modify_variables = input("Modify variables? (Enter y for yes, n for no)")
            if modify_variables == "y":
                done = True
                for variable in variables:
                    done2 = False
                    while not done2:
                        print(variable)
                        print(variables[variable])
                        modify_variable = input("Modify this variable? (Enter y for yes, n for no)")
                        if modify_variable == 'y':
                            modify_key = input("Enter key to modify: ")
                            try:
                                print("current value: " + str(variables[variable][modify_key]))
                                modify_value = input("Enter new value: ")
                                variables[variable][modify_key] = modify_value
                            except KeyValueError:
                                print(modify_key + " is not a valid key")
                        elif modify_variable == 'n':
                            done2 = True
                        else:
                            print('input was not y or n')
            elif modify_variables == "n":
                done = True
            else:
                print('input was not y or n')
    if args.instruction_file:
        pass

    if args.output_file:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
main()
