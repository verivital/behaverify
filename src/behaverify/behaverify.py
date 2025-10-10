'''
This file is used as the main entry point for BehaVerify.
It can be used to call the various modes of BehaVerify. If nuXmv has been downloaded, it can also envoke nuXmv.
For usage details, please consult: https://github.com/verivital/behaverify/blob/main/README.md
For instructions on how to create a new model, please consult: https://github.com/verivital/behaverify/blob/main/tutorial_examples/README.md

Original Author: Serena Serafina Serbinowska, serena.serbinowska@vanderbilt.edu
Current Maintainer:
'''
import argparse
import os
import subprocess
from importlib.resources import files

from behaverify.dsl_to_haskell import dsl_to_haskell
from behaverify.dsl_to_latex import dsl_to_latex
from behaverify.dsl_to_nuxmv import dsl_to_nuxmv
from behaverify.dsl_to_python import dsl_to_python
from behaverify.counter_trace import counter_trace
from behaverify.grid_world_draw.parse_nuxmv_output import handle_file as grid_world_draw_nuxmv_output
from behaverify.grid_world_draw.parse_python_output import handle_file as grid_world_draw_python_output
from behaverify.behaverify_gui import main as gui_main


def verify_location(directory_mode, current_location, overwrite):
    """
    Verify and create output location for generated files.

    Args:
        directory_mode: If None or False, current_location is a single file.
                       Otherwise, it's the directory name to create inside current_location.
        current_location: The output location (file path or parent directory).
        overwrite: Whether to allow overwriting existing files/directories.

    Raises:
        FileExistsError: If the output location exists and overwrite is False,
                        or if parent directory is not a directory.
    """
    if directory_mode is None or (not directory_mode):
        if os.path.exists(current_location) and not overwrite:
            raise FileExistsError('The file ' + current_location + ' already exists.')
        if os.path.exists(os.path.dirname(current_location)) and not os.path.isdir(os.path.dirname(current_location)):
            raise FileExistsError('The parent directory of ' + current_location + ' is not a directory.')
        if not os.path.isdir(os.path.dirname(current_location)):
            os.makedirs(os.path.dirname(current_location))
        return
    if os.path.exists(current_location) and not os.path.isdir(current_location):
        raise FileExistsError('Specified Output Location cannot be used as it exists and is not a folder')
    if os.path.exists(os.path.join(current_location, directory_mode)) and not overwrite:
        raise FileExistsError('Specified Output Location contains an element named ' + directory_mode + ' so the output cannot be written here')
    if not os.path.exists(os.path.join(current_location, directory_mode)):
        os.makedirs(os.path.join(current_location, directory_mode))


def verify_input(current_input):
    """
    Verify that input file exists and is a file.

    Args:
        current_input: Path to the input file.

    Raises:
        FileNotFoundError: If the input file doesn't exist or is not a file.
    """
    if not os.path.isfile(current_input):
        raise FileNotFoundError('Specified input file ' + current_input + ' could not be found')
    return


def get_metamodel_file():
    """
    Get the path to the metamodel file.

    Returns:
        Path to the behaverify.tx metamodel file.
    """
    try:
        return files('behaverify').joinpath('data', 'metamodel', 'behaverify.tx')
    except ModuleNotFoundError:
        metamodel_file = os.path.dirname(os.path.realpath(__file__)) + '/data/metamodel/behaverify.tx'
        print('did not find module; attempted to find files directly')
        return metamodel_file


def main(argv=None):
    """
    Main entry point for behaverify.

    Args:
        argv: Optional list of command-line arguments. If None, uses sys.argv.
              Allows programmatic invocation.

    Example programmatic usage:
        main(['nuxmv', 'model.tree', './output', '--generate'])
        main(['python', 'model.tree', './output'])
    """
    metamodel_file = get_metamodel_file()
    print(metamodel_file)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('mode')
    (args, _) = arg_parser.parse_known_args(argv)
    main_mode = args.mode.lower()
    if main_mode == 'grid':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('submode')
        (args, _) = arg_parser.parse_known_args(argv)
        if args.submode.lower() == 'network':
            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument('mode')
            arg_parser.add_argument('submode')
            arg_parser.add_argument('model_file')
            arg_parser.add_argument('trace_file')
            arg_parser.add_argument('location')
            arg_parser.add_argument('name')
            arg_parser.add_argument('--do_not_trim', action = 'store_true')
            arg_parser.add_argument('--recursion_limit', type = int, default = 0)
            raise NotImplementedError('Soon')
        elif args.submode.lower() == 'nuxmv':
            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument('mode')
            arg_parser.add_argument('submode')
            arg_parser.add_argument('trace_file')
            arg_parser.add_argument('location')
            arg_parser.add_argument('x_size', type = int)
            arg_parser.add_argument('y_size', type = int)
            arg_parser.add_argument('--stage', type = int, default = -1)
            arg_parser.add_argument('--overwrite', action = 'store_true')
            args = arg_parser.parse_args(argv)
            verify_input(args.trace_file)
            verify_location('grid_nuxmv', args.location, args.overwrite)
            grid_world_draw_nuxmv_output(args.trace_file, os.path.join(args.location, 'grid_nuxmv', 'img'), args.x_size, args.y_size, args.stage)
        elif args.submode.lower() == 'python':
            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument('mode')
            arg_parser.add_argument('submode')
            arg_parser.add_argument('trace_file')
            arg_parser.add_argument('location')
            arg_parser.add_argument('x_size', type = int)
            arg_parser.add_argument('y_size', type = int)
            arg_parser.add_argument('--overwrite', action = 'store_true')
            args = arg_parser.parse_args(argv)
            verify_input(args.trace_file)
            verify_location('grid_python', args.location, args.overwrite)
            grid_world_draw_python_output(args.trace_file, os.path.join(args.location, 'grid_python', 'img'), args.x_size, args.y_size)
    elif main_mode == 'haskell':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location', default = './')
        arg_parser.add_argument('--output_name', type = str, default = None)
        arg_parser.add_argument('--max_iter', default = 100)
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        arg_parser.add_argument('--overwrite', action = 'store_true')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('haskell', args.location, args.overwrite)
        output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        dsl_to_haskell(metamodel_file, args.model_file, os.path.join(args.location, 'haskell'), output_name, args.max_iter, args.recursion_limit, args.no_checks)
    elif main_mode == 'latex':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('output_file')
        arg_parser.add_argument('--insert_only', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--on_sides', action = 'store_true')
        args = arg_parser.parse_args(argv)
        dsl_to_latex(metamodel_file, args.model_file, args.output_file, args.insert_only, args.recursion_limit, args.on_sides)
    elif main_mode == 'nuxmv':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location', default = './')
        arg_parser.add_argument('--output_name', type = str, default = None)
        arg_parser.add_argument('--out2', type = str, default = None)
        arg_parser.add_argument('--generate', action = 'store_true')
        arg_parser.add_argument('--invar', action = 'store_true')
        arg_parser.add_argument('--ctl', action = 'store_true')
        arg_parser.add_argument('--ltl', action = 'store_true')
        arg_parser.add_argument('--simulate', type = int, default = 0)
        arg_parser.add_argument('--nuxmv_path', type = str, default = None)
        # arg_parser.add_argument('--keep_stage_0', action = 'store_true') # removed due to a bug.
        arg_parser.add_argument('--keep_last_stage', action = 'store_true')
        arg_parser.add_argument('--do_not_trim', action = 'store_true')
        arg_parser.add_argument('--behave_only', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        arg_parser.add_argument('--record_times', type = str, default = None)
        arg_parser.add_argument('--use_encoding', type = str, default = 'fastfowarding')
        arg_parser.add_argument('--overwrite', action = 'store_true')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('nuxmv', args.location, args.overwrite)
        input_file = args.model_file
        # output_file = set_output(args.location, input_file, args.output_name, extra_directory = 'nuxmv', extension = ('.smv' if args.generate else '.txt'))
        output_file = os.path.join(args.location, 'nuxmv', (args.output_name if args.output_name is not None else (os.path.splitext(os.path.basename(input_file))[0] + ('.smv' if args.generate else '.txt'))))
        if args.use_encoding.lower() not in ('fastforwarding', 'naive'):
            raise ValueError('Unknown encoding: ' + args.use_encoding.lower() + '. Encoding must be fastfowarding or naive (case insensitive).')
        if args.generate:
            dsl_to_nuxmv(metamodel_file, args.model_file, output_file, True, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks, args.record_times, args.use_encoding)
            input_file = output_file
            output_file = os.path.splitext(input_file)[0] + '_output.txt'
        if any((args.invar, args.ctl, args.ltl, args.simulate > 0)):
            if args.nuxmv_path is None:
                raise ValueError('Cannot run nuXmv without a path to nuXmv. Skipping nuXmv execution. Please specify a path to nuXmv next time.')
            command_file = os.path.splitext(input_file)[0] + '_input.txt'
            error_file = os.path.splitext(input_file)[0] + '_error.txt'
            command_string = (
                'go' + os.linesep
                + (('check_invar' + os.linesep) if args.invar else '')
                + (('check_ctlspec' + os.linesep) if args.ctl else '')
                + (('check_ltlspec' + os.linesep) if args.ltl else '')
                + ('pick_state -r' + os.linesep + ('simulate -r -v -k ' + str(args.simulate) + os.linesep) if args.simulate > 0 else '')
                + 'quit' + os.linesep
            )
            with open(command_file, 'w', encoding = 'utf-8') as command_file_obj:
                command_file_obj.write(command_string)
            with open(output_file, 'w', encoding = 'utf-8') as output_file_obj:
                with open(error_file, 'w', encoding = 'utf-8') as error_file_obj:
                    subprocess.run([args.nuxmv_path, '-source', command_file, input_file], check = True, stdout = output_file_obj, stderr = error_file_obj, text = True)
    elif main_mode == 'python':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('--output_name', type = str, default = None)
        arg_parser.add_argument('--max_iter', default = 100)
        arg_parser.add_argument('--no_var_print', action = 'store_true')
        arg_parser.add_argument('--serene_print', action = 'store_true')
        arg_parser.add_argument('--py_tree_print', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--safe_assignment', action = 'store_true')
        arg_parser.add_argument('--no_checks', action = 'store_true')
        arg_parser.add_argument('--overwrite', action = 'store_true')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('python', args.location, args.overwrite)
        output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        dsl_to_python(metamodel_file, args.model_file, output_name, os.path.join(args.location, 'python'), args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print, args.recursion_limit, args.safe_assignment, args.no_checks)
    elif main_mode == 'trace':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('trace_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('--do_not_trim', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--overwrite', action = 'store_true')
        args = arg_parser.parse_args(argv)
        verify_input(args.model_file)
        verify_location('trace', args.location, args.overwrite)
        # output_name = args.output_name if args.output_name is not None else os.path.splitext(os.path.basename(args.model_file))[0]
        counter_trace(metamodel_file, args.model_file, args.trace_file, os.path.join(args.location, 'trace'), args.do_not_trim, args.recursion_limit)
    elif main_mode == 'gui':
        gui_main()
    else:
        print('Unknown mode. Modes are gui, haskell, latex, nuxmv, python, or trace. Exiting')


if __name__ == '__main__':
    main()
