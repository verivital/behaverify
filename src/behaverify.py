import argparse
import py_trees

def main():
    arg_parser = argparse.ArgumentParser()
    #python3 behaverify.py create_root_FILE create_root_METHOD --root_args root_args_ARGS --string_args string_args_ARGS --min_val min_val_INT --max_val max_val_INT --force_parallel_unsynch --no_seperate_variable_modules --module_input_file module_input_file --specs_input_file specs_FILE --gen_modules gen_modules_INT --output_file ouput_file_FILE --module_output_file module_output_file_FILE --blackboard_output_file blackboard_output_file_FILE --overwrite 
    arg_parser.add_argument('json_file')
    arg_parser.add_argument('--blackboard_input_file', default = None)
    arg_parser.add_argument('--module_input_file', default = None)
    arg_parser.add_argument('--specs_input_file', default = None)
    arg_parser.add_argument('--output_file', default = None)
    arg_parser.add_argument('--blackboard_output_file', default = None)
    arg_parser.add_argument('--module_output_file', default = None)
    arg_parser.add_argument('--overwrite', action = 'store_true')
    args = arg_parser.parse_args()

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
