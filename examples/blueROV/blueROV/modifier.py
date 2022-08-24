import argparse
import sys
import os
import re
import pprint
#----------------------------------------------------------------------------------------------------------------
#todo: add a way to delete variables

def main():

    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('input_file') 
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--interactive_mode', action = 'store_true')
    arg_parser.add_argument('--instruction_file', action = 'store_true')
    args = arg_parser.parse_args()



    with open(args.input_file, 'r') as f:
        temp = eval(f.read())
    nodes = temp['nodes']
    variables = temp['variables']

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
    elif args.instruction_file:
        pass
    else:
        pass

    if args.output_file:
        with open(args.output_file, 'w') as f:
            printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False, stream = f)
            printer.pprint({'nodes' : nodes, 'variables' : variables})
    else:
        printer = pprint.PrettyPrinter(indent = 4, sort_dicts = False)
        printer.pprint({'nodes' : nodes, 'variables' : variables})
main()
