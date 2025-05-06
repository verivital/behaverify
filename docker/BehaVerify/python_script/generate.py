import os
import sys
import argparse
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR, BEHAVERIFY_VENV, RESULTS_VENV

def move_files(behaverify, input_path, networks_path, demo_copy = False):
    input_name = os.path.basename(input_path)
    (input_name_only, _) = os.path.splitext(input_name)
    serene_exec(behaverify, 'bash -c \'[ -d ' + USER_DIR + ' ] && sudo rm -rf ' + USER_DIR + '\'', 'Removing old user directory.', True)
    serene_exec(behaverify, 'bash -c \'mkdir ' + USER_DIR + '\'', 'Creating new user directory.', True)
    # serene_exec(behaverify, 'bash -c \'mkdir ' + USER_DIR + '/' + input_name_only + '\'', 'Creating new user directory.', True)
    serene_exec(behaverify, 'bash -c \'mkdir ' + USER_DIR + '/output\'', 'Creating new user directory subfolder 1.', True)
    serene_exec(behaverify, 'bash -c \'mkdir ' + USER_DIR + '/app\'', 'Creating new user directory subfolder 2.', True)
    if demo_copy:
        serene_exec(behaverify, 'bash -c \'cp ' + HOME_DIR + '/behaverify/demos/' + input_name_only + '/' + input_name_only + '.tree ' + USER_DIR + '/' + input_name_only + '.tree\'', 'Moving .tree file into place.', True)
        if networks_path != '-':
            serene_exec(behaverify, 'bash -c \'cp -r ' + HOME_DIR + '/behaverify/demos/' + input_name_only + '/networks ' + USER_DIR + '/' + '\'', 'Moving networks into place.', True)
    else:
        print('Start: adding relevant files from source to container.')
        if not copy_into(behaverify, input_path, USER_DIR):
            raise RuntimeError('Failed to copy input!')
        if networks_path != '-':
            print('network copy start')
            # (networks_location, networks_name) = os.path.split(networks_path)
            # if networks_name == '':
            #     networks_path = networks_location
            #     (networks_location, networks_name) = os.path.split(networks_path)
            # print(str((networks_location, networks_name)))
            if not copy_into(behaverify, networks_path, USER_DIR):
                raise RuntimeError('Failed to copy input!')
        print('End: adding relevant files from source to container.')
    return (input_name, input_name_only)

def generate(behaverify, input_name, input_name_only, to_generate, flags):
    serene_exec(behaverify,
                ' '.join(
                    [
                        BEHAVERIFY_VENV,
                        HOME_DIR + '/behaverify/src/' + ('dsl_to_' + to_generate + '.py'),
                        HOME_DIR + '/behaverify/metamodel/behaverify.tx',
                        USER_DIR + '/' + input_name
                    ]
                    + [USER_DIR + '/app/' + ((input_name_only + '.smv') if to_generate == 'nuXmv' else '')]
                    + ([input_name_only] if to_generate != 'nuXmv' else [])
                    + [flags]
                ),
                'Generation of requested code/model.',
                True)
    return

def evaluate(behaverify, input_name_only, to_generate, command):
    message_string = ''
    command_string = ''
    if to_generate == 'python':
        message_string = 'Simulation using Python.'
        command_string = ' '.join(
            [
                'bash -c',
                '\'' + ' '.join([
                    BEHAVERIFY_VENV,
                    USER_DIR + '/app/' + input_name_only + '_runner.py',
                    '>',
                    USER_DIR + '/output/python_simulation.txt'
                ]) + '\''
            ]
        )
    elif to_generate == 'nuxmv':
        message_string = ('Simulation' if command == 'evaluate' else ('Verifying ' + command + ' specifications')) + ' using nuXmv.'
        command_string = ' '.join(
            [
                'bash -c',
                '\'' + ' '.join([
                    HOME_DIR + '/nuXmv',
                    '-source',
                    HOME_DIR + '/behaverify/scripts/nuxmv_commands/command_' + command,
                    USER_DIR + '/app/' + input_name_only + '.smv',
                    '>',
                    USER_DIR + '/output/nuxmv_' + command + '_results.txt'
                ]) + '\''
            ]
        )
    elif to_generate == 'latex':
        print('SORRY! This script currently only allows you to generate LaTeX files, not evaluate them.')
        return
    elif to_generate == 'haskell':
        print('SORRY! This script currently only allows you to generate Haskell files, not evaluate them.')
        return
    serene_exec(behaverify, command_string, message_string, True)
    return

def verify_args(input_path, networks_path, output_path, to_generate, command, recursion_limit, max_iter, no_var_print, serene_print, py_tree_print, safe_assignment, keep_stage_0, keep_last_stage, do_not_trim, behave_only, insert_only, on_sides):
    if not os.path.exists(input_path):
        raise ValueError('Input Path does not exist.')
    if networks_path != '-' and not os.path.exists(networks_path):
        raise ValueError('Networks Path is not - and does not exist.')
    if os.path.exists(output_path):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.split(output_path)[0]):
        raise ValueError('Output Path is in a directory that does not exist.')
    # if not os.path.exists(output_path):
    #     raise ValueError('Output Path does not exist.')
    # if not os.path.isdir(output_path):
    #     raise ValueError('Output Path is not a directory.')
    if to_generate not in {'haskell', 'python', 'nuxmv', 'latex'}:
        raise ValueError('Unrecognized generate option: ' + to_generate + '. Options are Haskell, Python, and nuXmv.')
    if command not in {'generate', 'evaluate', 'ctl', 'ltl', 'invar'}:
        raise ValueError('Unrecognized command option: ' + command + '. Options are generate, evaluate, ctl, ltl, and invar.')
    if command in {'ctl', 'ltl', 'invar'} and to_generate != 'nuxmv':
        raise ValueError('Invalid generate + command combination. Python, Haskell, and LaTeX only support generate and evaluate.')
    if to_generate == 'haskell':
        return ' '.join([
            '--recursion_limit', str(recursion_limit),
            '--max_iter', str(max_iter)
            ])
    if to_generate == 'python':
        return ' '.join(filter(lambda x: x != '', [
            '--recursion_limit', str(recursion_limit),
            '--max_iter', str(max_iter),
            ('--no_var_print' if no_var_print else ''),
            ('--serene_print' if serene_print else ''),
            ('--py_tree_print' if py_tree_print else ''),
            ('--safe_assignment' if safe_assignment else ''),
            ]))
    if to_generate == 'latex':
        return ' '.join([
            '--recursion_limit', str(recursion_limit),
            ('--insert_only' if insert_only else ''),
            ('--on_sides' if on_sides else ''),
            ])
    return ' '.join(filter(lambda x: x != '', [
        '--recursion_limit', str(recursion_limit),
        ('--keep_stage_0' if keep_stage_0 else ''),
        ('--keep_last_stage' if keep_last_stage else ''),
        ('--do_not_trim' if do_not_trim else ''),
        ('--behave_only' if behave_only else ''),
    ]))


def non_demo_mode(input_path, networks_path, output_path, to_generate, command, recursion_limit = 0, max_iter = 100, no_var_print = False, serene_print = False, py_tree_print = False, safe_assignment = False, keep_stage_0 = False, keep_last_stage = False, do_not_trim = False, behave_only = False, insert_only = False, on_sides = False):
    to_generate = to_generate.lower()
    command = command.lower()
    flags = verify_args(input_path, networks_path, output_path, to_generate, command, recursion_limit, max_iter, no_var_print, serene_print, py_tree_print, safe_assignment, keep_stage_0, keep_last_stage, do_not_trim, behave_only, insert_only, on_sides)
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    (input_name, input_name_only) = move_files(behaverify, input_path, networks_path)
    generate(behaverify, input_name, input_name_only, to_generate, flags)
    if command != 'generate':
        evaluate(behaverify, input_name_only, to_generate, command)
    print('Start: Copy output to source.')
    copy_out_of(behaverify, USER_DIR, output_path + '.tar')
    print('End: Copy output to source.')
    behaverify.stop()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    arg_parser.add_argument('networks_path')
    arg_parser.add_argument('output_path')
    arg_parser.add_argument('to_generate')
    arg_parser.add_argument('command')
    arg_parser.add_argument('--recursion_limit', type = int, default = 0) # haskell, python, nuxmv
    arg_parser.add_argument('--max_iter', default = 100) # haskell, python
    arg_parser.add_argument('--no_var_print', action = 'store_true') # python
    arg_parser.add_argument('--serene_print', action = 'store_true') # python
    arg_parser.add_argument('--py_tree_print', action = 'store_true') # python
    arg_parser.add_argument('--safe_assignment', action = 'store_true') # python
    arg_parser.add_argument('--keep_stage_0', action = 'store_true') # nuxmv
    arg_parser.add_argument('--keep_last_stage', action = 'store_true') # nuxmv
    arg_parser.add_argument('--do_not_trim', action = 'store_true') # nuxmv
    arg_parser.add_argument('--behave_only', action = 'store_true') # nuxmv
    arg_parser.add_argument('--insert_only', action = 'store_true') # latex
    arg_parser.add_argument('--on_sides', action = 'store_true') # latex
    args = arg_parser.parse_args()
    non_demo_mode(args.input_path, args.networks_path, args.output_path, args.to_generate, args.command, args.recursion_limit, args.max_iter, args.no_var_print, args.serene_print, args.py_tree_print, args.safe_assignment, args.keep_stage_0, args.keep_last_stage, args.do_not_trim, args.behave_only, args.insert_only, args.on_sides)
