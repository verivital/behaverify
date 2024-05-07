import os
import sys
import argparse
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR, NURV_LOC

def monitor_trace(container, args):
    serene_exec(container,
                ' '.join(
                    [
                        'bash',
                        '-c',
                        'printf',
                        (
                            'go\n'
                            + 'build_monitor -n 0\n'
                            + 'read_trace ' + USER_DIR + '/' + args.trace + '\nverify_property -n 0 1\n'
                            + 'quit'
                        ),
                        '>',
                        HOME_DIR + '/command'
                    ]
                ),
                'Creating Trace command.',
                True)
    return

def generate_monitor(container, args):
    serene_exec(container,
                ' '.join(
                    [
                        'bash',
                        '-c',
                        'printf',
                        (
                            'go\n'
                            + 'build_monitor -n ' + str(args.n) + '\n'
                            + 'generate_monitor '
                            + '-n ' + str(args.n) + ' '
                            + '-P ' + str(args.P) + ' '
                            + '-l ' + str(args.l) + ' '
                            + '-L ' + str(args.L) + ' '
                            + (('-p ' + str(args.l)) if args.p else '')
                            + (('-x ' + str(args.l)) if args.x else '')
                            + (('-S ' + str(args.l)) if args.S else '')
                            + '-f ' + str(args.f) + ' '
                            + '-m ' + str(args.m) + ' '
                            + '-o ' + str(args.o) + ' '
                            + 'quit'
                        ),
                        '>',
                        HOME_DIR + '/command'
                    ]
                ),
                'Creating Trace command.',
                True)
    return

def verify_args(args):
    if not os.path.exists(args.model):
        raise ValueError('Model Path does not exist.')
    if os.path.exists(args.output):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.dirname(args.output)):
        raise ValueError('Output Path is in a directory that does not exist.')
    if args.trace is not None and not os.path.exists(args.networks_path):
        raise ValueError('Trace Path does not exist.')
    if args.generate_monitor not in ('dot', 'c', 'cpp', 'java', 'lisp', 'prolog', 'llvm', 'smv', 'FMU', 'FMU3'):
        raise ValueError('Unrecognized generate option: ' + args.generate_monitor + '. Options are ' + str(('dot', 'c', 'cpp', 'java', 'lisp', 'prolog', 'llvm', 'smv', 'FMU', 'FMU3')) + '.')
    if args.trace is not None and args.generate_monitor is not None:
        raise ValueError('Both Trace Path and Generate Monitor were set. Only one is allowed.')
    if args.trace is None and args.generate_monitor is None:
        raise ValueError('Neither Trace Path nor Generate Monitor were set. Exactly one is required.')
    if args.l not in (1, 2, 3, 4):
        raise ValueError('Argument l (monitor level) must be an integer between 1 and 4 inclusive')
    return


def non_demo_mode():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('model')
    arg_parser.add_argument('output')
    arg_parser.add_argument('--trace', type = str, default = None)
    arg_parser.add_argument('--generate_monitor', type = str, default = None)
    arg_parser.add_argument('--n', type = int, default = 0)
    arg_parser.add_argument('--P', type = str, default = None)
    arg_parser.add_argument('--l', type = int, default = 3)
    arg_parser.add_argument('--p', action = 'store_true')
    arg_parser.add_argument('--x', action = 'store_true')
    arg_parser.add_argument('--S', action = 'store_true')
    arg_parser.add_argument('--f', type = str, default = None)
    arg_parser.add_argument('--m', type = str, default = None)
    arg_parser.add_argument('--o', type = str, default = None)
    args = arg_parser.parse_args()
    verify_args(args)
    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)
    container.start()
    if args.trace is not None:
        monitor_trace(container, args)
    else:
        generate_monitor(container, args)
    serene_exec(container,
                ' '.join(
                    [
                        NURV_LOC,
                        '-quiet',
                        '-source',
                        HOME_DIR + '/command',
                        USER_DIR + '/' + os.path.basename(args.model),
                        '>',
                        USER_DIR + '/' + os.path.basename(args.output)
                    ]
                ),
                'Generation of requested code/model.',
                True)
    print('Start: Copy output to source.')
    copy_out_of(container, USER_DIR + '/' + os.path.basename(args.output), args.output + '.tar')
    print('End: Copy output to source.')
    container.stop()

if __name__ == '__main__':
    non_demo_mode()
