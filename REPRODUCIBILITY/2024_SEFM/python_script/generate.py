import os
import sys
import argparse
import docker
from docker_util import copy_out_of, serene_exec, TEST_DIR, CONTAINER_NAME, HOME_DIR

def generate(mode, write_location):
    if mode not in ('install', 'partial', 'full'):
        print('unknown argument. Must be one of install, partial, or full. Got: ' + str(mode))
        sys.exit()
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command_start = TEST_DIR + '/behaverify_sefm_'
    command_end = '.sh ' + TEST_DIR + ' ' + HOME_DIR + '/python_venvs/behaverify/bin/python3 ' + HOME_DIR + '/python_venvs/results/bin/python3'
    command = ''
    if mode == 'install':
        command = 'install_test'
    elif mode == 'partial':
        command = 'partial_results'
    elif mode == 'full':
        command = 'full_results'
    serene_exec(behaverify, command_start + command + command_end, command, True)
    copy_out_of(behaverify, TEST_DIR + '/examples', write_location + '.tar')


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
