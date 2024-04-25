import os
import sys
import argparse
import docker
from docker_util import copy_out_of, serene_exec, TEST_DIR, CONTAINER_NAME, HOME_DIR

if __name__ == '__main__':
    if sys.argv[1] not in ('install', 'partial', 'full'):
        print('unknown argument. Must be one of install, partial, or full. Got: ' + str(sys.argv[1]))
        sys.exit()
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command_start = TEST_DIR + '/behaverify_atva_'
    command_end = 'sh ' + TEST_DIR + ' ' + HOME_DIR + '/python_venvs/behaverify/bin/python3 ' + HOME_DIR + '/python_venvs/results/bin/python3'
    command = ''
    if sys.argv[1] == 'install':
        command = 'install_test'
    elif sys.argv[1] == 'partial':
        command = 'partial_results'
    elif sys.argv[1] == 'full':
        command = 'full_results'
    serene_exec(behaverify, command_start + command + command_end, command, True)
    if not copy_out_of(behaverify, TEST_DIR + '/examples/', sys.argv[2]):
        print('FAILED TO COPY OUTPUT')
