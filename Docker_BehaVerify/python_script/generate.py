import os
import sys
import argparse
import docker
from docker_util import copy_into, copy_out_of, serene_exec

def move_files(behaverify, input_path, networks_path):
    input_name = os.path.basename(input_path)
    (input_name_only, _) = os.path.splitext(input_name)
    serene_exec(behaverify, '/home/behaverify/behaverify/Docker_BehaVerify/util/setup_directory.sh ' + input_name_only, 'Setting up directories in container.', True)
    print('Start: adding relevant files from source to container.')
    if not copy_into(behaverify, input_path, '/home/behaverify/user_files/' + input_name_only):
        raise RuntimeError('Failed to copy input!')
    if networks_path != '-':
        (networks_location, networks_name) = os.path.split(networks_path)
        if networks_name == '':
            networks_path = networks_location
            (networks_location, networks_name) = os.path.split(networks_path)
        if not copy_into(behaverify, networks_path, '/home/behaverify/user_files/' + input_name_only):
            raise RuntimeError('Failed to copy input!')
    print('End: adding relevant files from source to container.')
    return (input_name, input_name_only)

def move_files_demo(behaverify, input_name_only, uses_networks):
    serene_exec(behaverify, '/home/behaverify/behaverify/Docker_BehaVerify/util/setup_directory.sh ' + input_name_only, 'Setting up directories in container.', True)
    serene_exec(behaverify, 'bash -c \'cp /home/behaverify/behaverify/demos/' + input_name_only + '/' + input_name_only + '.tree /home/behaverify/user_files/' + input_name_only + '\'', 'Moving .tree file into place.', True)
    if uses_networks:
        serene_exec(behaverify, 'bash -c \'cp -r /home/behaverify/behaverify/demos/' + input_name_only + '/networks /home/behaverify/user_files/' + input_name_only + '\'', 'Moving networks into place.', True)
    return

def generate(behaverify, input_name, input_name_only, to_generate, flags):
    serene_exec(behaverify,
                ' '.join(
                    [
                        '/home/behaverify/behaverify_venv/bin/python3',
                        (
                            '/home/behaverify/behaverify/src/'
                            + ('dsl_to_nuxmv.py ' if to_generate == 'nuXmv' else ('dsl_to_python.py ' if to_generate == 'Python' else 'dsl_to_haskell.py '))
                        ),
                        '/home/behaverify/behaverify/metamodel/behaverify.tx',
                        '/home/behaverify/user_files/' + input_name_only + '/' + input_name
                    ]
                    + (
                        ['/home/behaverify/user_files/' + input_name_only + '/app/' + input_name_only + '.smv']
                        if to_generate == 'nuXmv' else
                        ['/home/behaverify/user_files/' + input_name_only + '/' + ('app/' if to_generate == 'Haskell' else ''), input_name_only]
                    )
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
                    '/home/behaverify/behaverify_venv/bin/python3',
                    '/home/behaverify/user_files/' + input_name_only + '/app/' + input_name_only + '_runner.py',
                    '>',
                    '/home/behaverify/user_files/' + input_name_only + '/output/python_simulation.txt'
                ]) + '\''
            ]
        )
    if to_generate == 'nuXmv':
        message_string = ('Simulation' if command == 'simulate' else ('Verifying ' + command + ' specifications')) + ' using nuXmv.'
        command_string = ' '.join(
            [
                'bash -c',
                '\'' + ' '.join([
                    '/home/behaverify/nuXmv',
                    '-source',
                    '/home/behaverify/behaverify/scripts/nuxmv_commands/command_' + command,
                    '/home/behaverify/user_files/' + input_name_only + '/app/' + input_name_only + '.smv',
                    '>',
                    '/home/behaverify/user_files/' + input_name_only + '/output/nuxmv_' + command + '_results.txt'
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
            ('--safe_assignment' if args.safe_assignment_print else ''),
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
    behaverify = client.containers.get('behaverify')
    behaverify.start()
    (input_name, input_name_only) = move_files(behaverify, args.input_path, args.networks_path)
    generate(behaverify, input_name, input_name_only, args.to_generate, flags)
    if args.command != 'generate':
        evaluate(behaverify, input_name_only, args.to_generate, args.command)
    print('Start: Copy output to source.')
    copy_out_of(behaverify, '/home/behaverify/user_files/' + input_name_only, args.output_path + '.tar')
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
    current_demos = {'ANSR_ONNX_2', 'ANSR_ONNX_2_counter'}
    uses_networks = {'ANSR_ONNX_2', 'ANSR_ONNX_2_counter'}
    if demo not in current_demos:
        raise ValueError('Unknown demo: ' + demo + '. Current demos are: ' + str(current_demos) + '.')
    client = docker.from_env()
    behaverify = client.containers.get('behaverify')
    behaverify.start()
    move_files_demo(behaverify, demo, demo in uses_networks)
    if demo == 'ANSR_ONNX_2':
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
        if args.additional_input != '':
            serene_exec(behaverify, ' '.join([
                '/home/behaverify/behaverify_venv/bin/python3',
                '/home/behaverify/behaverify/demos/' + demo + '/edit_constants.py',
                '/home/behaverify/user_files/' + demo + '/' + demo + '.tree',
                '\'' + args.additional_input + '\'']), 'Modifying constants for ANSR_ONNX_2.', True)
    elif demo == 'ANSR_ONNX_2_counter':
        to_generate = 'nuXmv'
        flags = ''
        command = 'ctl'
    generate(behaverify, demo + '.tree', demo, to_generate, flags)
    if command != 'generate':
        evaluate(behaverify, demo, to_generate, command)
    ##### SPECIAL ZONE
    special_command = None
    if demo == 'ANSR_ONNX_2':
        pass
    elif demo == 'ANSR_ONNX_2_counter':
        special_command = ' '.join([
            '/home/behaverify/draw_venv/bin/python3',
            '/home/behaverify/behaverify/demos/ANSR_ONNX_2_counter/parse_nuxmv_output.py',
            '/home/behaverify/user_files/' + demo + '/output/nuxmv_ctl_results.txt',
            '/home/behaverify/user_files/' + demo + '/output/' + demo,
            '11',
            '11'
        ])
    if special_command is not None:
        serene_exec(behaverify, special_command, 'Execution of extra commands necessary for Demo.', True)
    ##### END SPECIAL ZONE
    print('Start: Copy output to source.')
    copy_out_of(behaverify, '/home/behaverify/user_files/' + demo, args.output_path + '.tar')
    print('End: Copy output to source.')
    behaverify.stop()

if __name__ == '__main__':
    if sys.argv[1] == 'demo':
        demo_mode()
    else:
        non_demo_mode()
