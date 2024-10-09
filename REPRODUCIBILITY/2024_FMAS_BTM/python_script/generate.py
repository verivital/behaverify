import os
import sys
import argparse
import docker
from docker_util import copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, TEST_DIR, USER

def generate(mode, write_location):
    if mode not in ('install', 'partial', 'full'):
        print('unknown argument. Must be one of install, partial, or full. Got: ' + str(mode))
        sys.exit()
    iterations = '2' if mode == 'install' else ('5' if mode == 'partial' else 9))
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command = TEST_DIR + '/' + USER + '.sh ' + TEST_DIR + ' ' + iterations + ' ' + HOME_DIR + '/python_venvs/behaverify/bin/python3 ' + HOME_DIR + '/python_venvs/results/bin/python3'
    serene_exec(behaverify, command, mode, True)
    copy_out_of(behaverify, TEST_DIR + '/example', write_location + '.tar')


if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
