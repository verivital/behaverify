import argparse
import os
from importlib.resources import files

from behaverify.dsl_to_haskell import dsl_to_haskell
from behaverify.dsl_to_latex import dsl_to_latex
from behaverify.dsl_to_nuxmv import dsl_to_nuxmv
from behaverify.dsl_to_python import dsl_to_python

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
        arg_parser.add_argument('output_file')
        # arg_parser.add_argument('--keep_stage_0', action = 'store_true') # removed due to a bug.
        arg_parser.add_argument('--keep_last_stage', action = 'store_true')
        arg_parser.add_argument('--do_not_trim', action = 'store_true')
        arg_parser.add_argument('--behave_only', action = 'store_true')
        arg_parser.add_argument('--recursion_limit', type = int, default = 0)
        arg_parser.add_argument('--no_checks', action = 'store_true')
        arg_parser.add_argument('--record_times', type = str, default = None)
        args = arg_parser.parse_args()
        # dsl_to_nuxmv(args.metamodel_file, args.model_file, args.output_file, args.keep_stage_0, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks)
        dsl_to_nuxmv(metamodel_file, args.model_file, args.output_file, True, args.keep_last_stage, args.do_not_trim, args.behave_only, args.recursion_limit, False, args.no_checks, args.record_times)
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
    else:
        print('Unknown mode. Modes are haskell, latex, nuxmv, or python. Exiting')


if __name__ == '__main__':
    main()
