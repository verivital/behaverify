import os
import sys
import argparse
import docker
from docker_util import copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, TEST_DIR, USER

def generate(mode, write_location):
    if mode not in ('install', 'full', 'timeout'):
        print('unknown argument. Must be one of install, full, or timeout. Got: ' + str(mode))
        sys.exit()
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command_start = TEST_DIR + '/' + USER + '_'
    command_end = '.sh ' + TEST_DIR + ' ' + HOME_DIR + '/python_venvs/behaverify/bin/python3 ' + HOME_DIR + '/python_venvs/results/bin/python3'
    command = ''
    if mode == 'install':
        command = 'test_installation'
    elif mode == 'timeout':
        command = 'timeout_results'
    elif mode == 'full':
        command = 'full_results'
    serene_exec(behaverify, command_start + command + command_end, command, True)
    copy_out_of(behaverify, TEST_DIR + '/examples', write_location + '.tar')


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
