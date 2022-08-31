import argparse
import sys
import os
import re
import pprint
#----------------------------------------------------------------------------------------------------------------
#todo: add a way to delete variables and change access


def arg_modification(args):
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
            variable['always_exist'] = True
        if args.sometimes_exist:
            variable['always_exist'] = False
        if args.init_exist:
            variable['init_exist'] = bool(args.init_exist)
        if args.no_init_exist:
            variable['init_exist'] = None
        if args.next_exist:
            variable['next_exist'] = bool(args.next_exist)
        if args.no_next_exist:
            variable['no_next_exist'] = None
    for node_id in nodes:
        node = nodes[node_id]
        if args.force_parallel_unsynch:
            if node['category'] == 'composite' and 'parallel_synchronized' in node['type']:
                node['type'] = node['type'].replace('_synchronized', '_unsynchronized')
                node['type'] = node['type'].replace('success_on_one', 'success_on_all')
        if args.force_parallel_synch:
            if node['category'] == 'composite' and 'parallel_unsynchronized' in node['type']:
                node['type'] = node['type'].replace('_unsynchronized', '_synchronized')
        if args.force_selector_memory:
            if node['category'] == 'composite' and 'selector_without_memory' == node['type']:
                node['type'] = 'selector_with_memory'
        if args.force_selector_memoryless:
            if node['category'] == 'composite' and 'selector_with_memory' == node['type']:
                node['type'] = 'selector_without_memory'
        if args.force_sequence_memory:
            if node['category'] == 'composite' and 'sequence_without_memory' == node['type']:
                node['type'] = 'sequence_with_memory'
        if args.force_sequence_memoryless:
            if node['category'] == 'composite' and 'sequence_with_memory' == node['type']:
                node['type'] = 'sequence_without_memory'
        if args.use_next_checks:
            if node['type'] == 'check_blackboard_variable_value':
                node['use_next'] = True
        if args.use_current_checks:
            if node['type'] == 'check_blackboard_variable_value':
                node['use_next'] = False

def main():

    arg_parser = argparse.ArgumentParser()
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
    arg_parser.add_argument('--use_next_checks', action = 'store_true')
    arg_parser.add_argument('--use_current_checks', action = 'store_true')
    
    
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

    if args.force_parallel_synch or args.force_parallel_unsynch or args.force_selector_memory or args.force_selector_memoryless or args.force_sequence_memory or args.force_sequence_memoryless or args.min_value or args.max_value or args.init_value or args.no_init_value or args.next_value or args.no_next_value or args.use_global_value or args.use_individual_value or args.always_exist or args.sometimes_exist or args.init_exist or args.no_init_exist or args.next_exist or args.no_next_eixst:
        arg_modification(args)


    deletions = False
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
                for variable_name in variables:
                    done2 = False
                    while not done2:
                        print(variable_name)
                        print(variables[variable_name])
                        modify_variable = input("Modify this variable? (Enter y for yes, n for no)")
                        if modify_variable == 'y':
                            modify_key = input("Enter key to modify: ")
                            modify_key = modify_key.strip()
                            if modify_key == 'delete':
                                variable = variables.pop(variable_name)
                                for node_id in variable['access']:
                                    nodes[node_id]['variables'].remove(variable_name)
                                deletions = True
                            else:
                                try:
                                    print("current value: " + str(variables[variable_name][modify_key]))
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
        node_name_to_id = {}
        for node_id in nodes:
            node_name_to_id[nodes[node_id]['name']] = node_id
        with open(args.instruction_file, 'r') as f:
            instructions = eval(f.read())
        for instruction in instructions:
            if instruction['target'].strip().lower() == 'global_flags':
                args = arg_parser.parse_args(instruction['instruction'])
                arg_modification(args)
            elif instruction['target'].strip().lower() == 'variable':
                if instruction['instruction'].strip().lower() == 'delete':
                    variable = variabeles.pop(instruction['name'])
                    for node_id in variable['access']:
                        nodes[node_id]['variables'].remove(instruction['name'])
                    deletions = True
                else:
                    variables[instruction['name']][instruction['field']] = instruction['value']
            elif instruction['target'].strip().lower() == 'node':
                nodes[node_name_to_id[instruction['name']]][instruction['field']] = instruction['value']
            else:
                print('instruction file contains unknown modification target: ' + str(instruction['target']))
        pass
    #oh thank god indenting is working agian

    if deletions:
        count = 0
        for variable_name in variables:
            variables[variable_name]['variable_id'] = count
            count = count + 1

    if args.output_file:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
main()
