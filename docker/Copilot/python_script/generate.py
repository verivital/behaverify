import os
import sys
import argparse
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR#, NURV_LOC


def generate_monitor(container, args):
    serene_exec(container,
                ' '.join(
                    [
                        'bash -c \'cd ' + USER_DIR + ';',
                        'runhaskell',
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
    return


def non_demo_mode():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('model')
    arg_parser.add_argument('output')
    args = arg_parser.parse_args()
    verify_args(args)
    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)
    container.start()
    serene_exec(container, 'bash -c \'rm -rf ' + USER_DIR + '\'', 'Deleting User Dir in Container.', False)
    serene_exec(container, 'bash -c \'rm -rf ' + HOME_DIR + '/command' + '\'', 'Deleting User Command in Container.', False)
    serene_exec(container, 'bash -c \'mkdir ' + USER_DIR + '\'', 'Creating User Dir in Container.', False)
    copy_into(container, args.model, USER_DIR)
    generate_monitor(container, args)
    container.stop()

if __name__ == '__main__':
    non_demo_mode()
