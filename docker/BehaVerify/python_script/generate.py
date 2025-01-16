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
                        (
                            HOME_DIR + '/behaverify/src/'
                            + ('dsl_to_nuxmv.py ' if to_generate == 'nuXmv' else ('dsl_to_python.py ' if to_generate == 'Python' else 'dsl_to_haskell.py '))
                        ),
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
    if to_generate == 'Haskell':
        print('SORRY! This script currently only allows you to generate Haskell files, not simulate them.')
        return
    if to_generate == 'Python':
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
    if to_generate == 'nuXmv':
        message_string = ('Simulation' if command == 'simulate' else ('Verifying ' + command + ' specifications')) + ' using nuXmv.'
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
    serene_exec(behaverify, command_string, message_string, True)
    return

def verify_args(args):
    if not os.path.exists(args.input_path):
        raise ValueError('Input Path does not exist.')
    if args.networks_path != '-' and not os.path.exists(args.networks_path):
        raise ValueError('Networks Path is not - and does not exist.')
    if os.path.exists(args.output_path):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.split(args.output_path)[0]):
        raise ValueError('Output Path is in a directory that does not exist.')
    # if not os.path.exists(args.output_path):
    #     raise ValueError('Output Path does not exist.')
    # if not os.path.isdir(args.output_path):
    #     raise ValueError('Output Path is not a directory.')
    if args.to_generate not in {'Haskell', 'Python', 'nuXmv'}:
        raise ValueError('Unrecognized generate option: ' + args.to_generate + '. Options are Haskell, Python, and nuXmv.')
    if args.command not in {'generate', 'simulate', 'ctl', 'ltl', 'invar'}:
        raise ValueError('Unrecognized command option: ' + args.command + '. Options are generate, simulate, ctl, ltl, and invar.')
    if args.command in {'ctl', 'ltl', 'invar'} and args.to_generate != 'nuXmv':
        raise ValueError('Invalid generate + command combination. Python and Haskell only support generate and simulate.')
    if args.to_generate == 'Haskell':
        return ' '.join([
            '--recursion_limit', str(args.recursion_limit),
            '--max_iter', str(args.max_iter)
            ])
    if args.to_generate == 'Python':
        return ' '.join(filter(lambda x: x != '', [
            '--recursion_limit', str(args.recursion_limit),
            '--max_iter', str(args.max_iter),
            ('--no_var_print' if args.no_var_print else ''),
            ('--serene_print' if args.serene_print else ''),
            ('--py_tree_print' if args.py_tree_print else ''),
            ('--safe_assignment' if args.safe_assignment else ''),
            ]))
    return ' '.join(filter(lambda x: x != '', [
        '--recursion_limit', str(args.recursion_limit),
        ('--keep_stage_0' if args.keep_stage_0 else ''),
        ('--keep_last_stage' if args.keep_last_stage else ''),
        ('--do_not_trim' if args.do_not_trim else ''),
        ('--behave_only' if args.behave_only else ''),
    ]))


def non_demo_mode():
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
    args = arg_parser.parse_args()
    flags = verify_args(args)
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    (input_name, input_name_only) = move_files(behaverify, args.input_path, args.networks_path)
    generate(behaverify, input_name, input_name_only, args.to_generate, flags)
    if args.command != 'generate':
        evaluate(behaverify, input_name_only, args.to_generate, args.command)
    print('Start: Copy output to source.')
    copy_out_of(behaverify, USER_DIR, args.output_path + '.tar')
    print('End: Copy output to source.')
    behaverify.stop()

def demo_mode():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('demo')
    arg_parser.add_argument('output_path')
    arg_parser.add_argument('--additional_input', default = '')
    args = arg_parser.parse_args(sys.argv[2:])
    if os.path.exists(args.output_path):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.split(args.output_path)[0]):
        raise ValueError('Output Path is in a directory that does not exist.')
    demo = args.demo
    current_demos = {'grid_net', 'moving_target'}
    uses_networks = {'grid_net', 'moving_target'}
    if demo not in current_demos:
        raise ValueError('Unknown demo: ' + demo + '. Current demos are: ' + str(current_demos) + '.')
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    if demo in ('grid_net',):
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
    elif demo in ('moving_target'):
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
        ansr_x_size = 11
        ansr_y_size = 11
        if args.additional_input != '':
            serene_exec(behaverify, ' '.join([
                BEHAVERIFY_VENV,
                HOME_DIR + '/behaverify/demos/' + demo + '/edit_constants.py',
                USER_DIR + '/' + demo + '/' + demo + '.tree',
                '\'' + args.additional_input + '\'']), 'Modifying constants for ' + demo + '.', True)
            try:
                ansr_vals = [0, 0, 0, 0]
                for (index, ansr_code) in enumerate(('x_min', 'x_max', 'y_min', 'y_max')):
                    val = args.additional_input.split(ansr_code)[1]
                    val = val.split(',')[0]
                    val = val.replace(':=', '')
                    ansr_vals[index] = int(val.strip())
                ansr_x_size = (ansr_vals[1] - ansr_vals[0]) + 1
                ansr_y_size = (ansr_vals[3] - ansr_vals[2]) + 1
            except:
                pass
    move_files(behaverify, demo, 'yes' if demo in uses_networks else '-', True)
    generate(behaverify, demo + '.tree', demo, to_generate, flags)
    if command != 'generate':
        evaluate(behaverify, demo, to_generate, command)
    ##### SPECIAL ZONE
    special_command = None
    if demo == 'moving_target':
        special_command = ' '.join([
            RESULTS_VENV,
            HOME_DIR + '/behaverify/demos/moving_target/parse_nuxmv_output.py',
            USER_DIR + '/' + demo + '/output/nuxmv_ctl_results.txt',
            USER_DIR + '/' + demo + '/output/' + demo,
            str(ansr_x_size),
            str(ansr_y_size)
        ])
    if special_command is not None:
        serene_exec(behaverify, special_command, 'Execution of extra commands necessary for Demo.', True)
    ##### END SPECIAL ZONE
    print('Start: Copy output to source.')
    copy_out_of(behaverify, USER_DIR + '/' + demo, args.output_path + '.tar')
    print('End: Copy output to source.')
    behaverify.stop()

if __name__ == '__main__':
    if sys.argv[1] == 'demo':
        demo_mode()
    else:
        non_demo_mode()
