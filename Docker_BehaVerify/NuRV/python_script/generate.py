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
                        '\'printf',
                        (
                            '"go\n'
                            + 'build_monitor -n 0\n'
                            + 'read_trace ' + USER_DIR + '/' + os.path.basename(args.trace) + '\n'
                            + 'verify_property -n 0 1\n'
                            + 'quit\n"'
                        ),
                        '>',
                        HOME_DIR + '/command\''
                    ]
                ),
                'Creating Trace command.',
                True)
    serene_exec(container,
                ' '.join(
                    [
                        'bash -c \'',
                        NURV_LOC,
                        '-quiet',
                        '-source',
                        HOME_DIR + '/command',
                        USER_DIR + '/' + os.path.basename(args.model),
                        '>',
                        USER_DIR + '/' + os.path.basename(args.output),
                        '\''
                    ]
                ),
                'Verifying Trace.',
                True)
    print('Start: Copy output to source.')
    copy_out_of(container, USER_DIR + '/' + os.path.basename(args.output), args.output + '.tar')
    print('End: Copy output to source.')
    return

def generate_monitor(container, args):
    serene_exec(container,
                ' '.join(
                    [
                        'bash',
                        '-c',
                        '\'printf ' + (
                            '"go\n'
                            + 'build_monitor -n ' + str(args.n) + '\n'
                            + 'generate_monitor '
                            + '-n ' + str(args.n) + ' '
                            + (('-P \\"' + args.P + '\\" ') if args.P is not None else '')
                            + '-l ' + str(args.l) + ' '
                            + '-L \\"' + str(args.L) + '\\" '
                            + ('-p ' if args.p else '')
                            + ('-x ' if args.x else '')
                            + ('-S ' if args.S else '')
                            + (('-m \\"' + args.m + '\\" ') if args.m is not None else '')
                            + (('-o \\"' + args.o + '\\"') if args.m is not None else '')
                            + '\nquit\n"'
                        ),
                        '>',
                        HOME_DIR + '/command\''
                    ]
                ),
                'Creating Generate command.',
                True)
    serene_exec(container,
                ' '.join(
                    [
                        'bash -c \'cd ' + USER_DIR + ';',
                        NURV_LOC,
                        '-quiet',
                        '-source',
                        HOME_DIR + '/command',
                        USER_DIR + '/' + os.path.basename(args.model),
                        '\''
                    ]
                ),
                'Generating Monitor.',
                True)
    print('Start: Copy output to source.')
    copy_out_of(container, USER_DIR, args.output + '.tar')
    print('End: Copy output to source.')
    return

def verify_args(args):
    if not os.path.exists(args.model):
        raise ValueError('Model Path does not exist.')
    if os.path.exists(args.output):
        raise ValueError('Output Path exists.')
    if not os.path.isdir(os.path.dirname(args.output)):
        raise ValueError('Output Path is in a directory that does not exist.')
    if args.trace is not None and not os.path.exists(args.trace):
        raise ValueError('Trace Path does not exist.')
    if args.L not in ('dot', 'c', 'cpp', 'java', 'lisp', 'prolog', 'llvm', 'smv', 'FMU', 'FMU3'):
        raise ValueError('Unrecognized generate option: ' + args.L + '. Options are ' + str(('dot', 'c', 'cpp', 'java', 'lisp', 'prolog', 'llvm', 'smv', 'FMU', 'FMU3')) + '.')
    if args.trace is not None and args.generate_monitor:
        raise ValueError('Both Trace Path and Generate Monitor were set. Only one is allowed.')
    if args.trace is None and not args.generate_monitor:
        raise ValueError('Neither Trace Path nor Generate Monitor were set. Exactly one is required.')
    if args.l not in (1, 2, 3, 4):
        raise ValueError('Argument l (monitor level) must be an integer between 1 and 4 inclusive')
    return


def non_demo_mode():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('model')
    arg_parser.add_argument('output')
    arg_parser.add_argument('--trace', type = str, default = None)
    arg_parser.add_argument('--generate_monitor', action = 'store_true')
    arg_parser.add_argument('--n', type = int, default = 0) # property number to monitor
    arg_parser.add_argument('--P', type = str, default = None) # property Name
    arg_parser.add_argument('--l', type = int, default = 3) # level of monitoring
    arg_parser.add_argument('--L', type = str, default = 'c') # language of monitor
    arg_parser.add_argument('--p', action = 'store_true') # powerset for partial observability
    arg_parser.add_argument('--x', action = 'store_true') # true integers and the like
    arg_parser.add_argument('--S', action = 'store_true') # use NuRV as symbolic library
    arg_parser.add_argument('--m', type = str, default = None) # module name
    arg_parser.add_argument('--o', type = str, default = None) # file name
    args = arg_parser.parse_args()
    verify_args(args)
    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)
    container.start()
    serene_exec(container, 'bash -c \'rm -rf ' + USER_DIR + '\'', 'Deleting User Dir in Container.', False)
    serene_exec(container, 'bash -c \'rm -rf ' + HOME_DIR + '/command' + '\'', 'Deleting User Command in Container.', False)
    serene_exec(container, 'bash -c \'mkdir ' + USER_DIR + '\'', 'Creating User Dir in Container.', False)
    copy_into(container, args.model, USER_DIR)
    if args.trace is not None:
        copy_into(container, args.trace, USER_DIR)
        monitor_trace(container, args)
    else:
        generate_monitor(container, args)
    container.stop()

if __name__ == '__main__':
    non_demo_mode()
