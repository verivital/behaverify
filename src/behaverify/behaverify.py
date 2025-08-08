import argparse
import os
import subprocess
from importlib.resources import files

from behaverify.dsl_to_haskell import dsl_to_haskell
from behaverify.dsl_to_latex import dsl_to_latex
from behaverify.dsl_to_nuxmv import dsl_to_nuxmv
from behaverify.dsl_to_python import dsl_to_python
from behaverify.counter_trace import counter_trace

def main():
    metamodel_file = None
    try:
        metamodel_file = files('behaverify').joinpath('metamodel', 'behaverify.tx')
    except ModuleNotFoundError:
        metamodel_file = os.path.dirname(os.path.realpath(__file__)) + '/metamodel/behaverify.tx'
        print('did not find module; attempted to find files directly')
    print(metamodel_file)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('mode')
    (args, _) = arg_parser.parse_known_args()
    if args.mode == 'haskell':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location', default = './')
        arg_parser.add_argument('output_name')
        arg_parser.add_argument('--max_iter', default = 100)
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        args = arg_parser.parse_args()
        dsl_to_haskell(metamodel_file, args.model_file, args.location, args.output_name, args.max_iter, args.recursion_limit, args.no_checks)
    elif args.mode == 'latex':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('output_file')
        arg_parser.add_argument('--insert_only', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--on_sides', action = 'store_true')
        args = arg_parser.parse_args()
        dsl_to_latex(metamodel_file, args.model_file, args.output_file, args.insert_only, args.recursion_limit, args.on_sides)
    elif args.mode == 'nuxmv':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location', default = './')
        arg_parser.add_argument('output_name')
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
        args = arg_parser.parse_args()
        if os.path.exists(args.location) and not os.path.isdir(args.location):
            raise FileExistsError('Specified Output Location cannot be used as it exists and is not a folder')
        if os.path.exists(os.path.join(args.location, 'nuxmv')):
            raise FileExistsError('Specified Output Location contains an element named nuxmv so the output cannot be written here')
        if not os.path.exists(os.path.join(args.location, 'nuxmv')):
            os.makedirs(os.path.join(args.location, 'nuxmv'))
        # dsl_to_nuxmv(args.metamodel_file, args.model_file, args.output_file, args.keep_stage_0, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks)
        input_file = args.model_file
        if args.generate:
            dsl_to_nuxmv(metamodel_file, args.model_file, os.path.join(args.location, 'nuxmv', args.output_name), True, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks, args.record_times)
            input_file = os.path.join(args.location, 'nuxmv', args.output_name)
        if any((args.invar, args.ctl, args.ltl, args.simulate > 0)):
            input_string = (
                'go' + os.linesep
                + (('check_invar' + os.linesep) if args.invar else '')
                + (('check_ctlspec' + os.linesep) if args.ctl else '')
                + (('check_ltlspec' + os.linesep) if args.ltl else '')
                + ('pick_state -r' + os.linesep + ('simulate -r -v -k ' + str(args.simulate) + os.linesep) if args.simulate > 0 else '')
                + 'quit' + os.linesep
            )
            with open(os.path.join(args.location, 'nuxmv', args.output_name + 'input.txt'), 'w', encoding = 'utf-8') as command_file:
                command_file.write(input_string)
            with open(os.path.join(args.location, 'nuxmv', args.output_name + 'output.txt'), 'w', encoding = 'utf-8') as output_file:
                with open(os.path.join(args.location, 'nuxmv', args.output_name + 'error.txt'), 'w', encoding = 'utf-8') as error_file:
                    subprocess.run([args.nuxmv_path, '-source', os.path.join(args.location, 'nuxmv', args.output_name + 'input.txt'), input_file], check = True, stdout = output_file, stderr = error_file, text = True)
    elif args.mode == 'python':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('name')
        arg_parser.add_argument('--max_iter', default = 100)
        arg_parser.add_argument('--no_var_print', action = 'store_true')
        arg_parser.add_argument('--serene_print', action = 'store_true')
        arg_parser.add_argument('--py_tree_print', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--safe_assignment', action = 'store_true')
        arg_parser.add_argument('--no_checks', action = 'store_true')
        args = arg_parser.parse_args()
        dsl_to_python(metamodel_file, args.model_file, args.name, args.location, args.serene_print, args.max_iter, args.no_var_print, args.py_tree_print, args.recursion_limit, args.safe_assignment, args.no_checks)
    elif args.mode == 'trace':
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('mode')
        arg_parser.add_argument('model_file')
        arg_parser.add_argument('trace_file')
        arg_parser.add_argument('location')
        arg_parser.add_argument('name')
        arg_parser.add_argument('--do_not_trim', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        args = arg_parser.parse_args()
        counter_trace(metamodel_file, args.model_file, args.trace_file, args.location, args.do_not_trim, args.recursion_limit)
    else:
        print('Unknown mode. Modes are haskell, latex, nuxmv, or python. Exiting')


if __name__ == '__main__':
    main()
