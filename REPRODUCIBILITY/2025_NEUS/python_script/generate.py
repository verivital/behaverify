import sys
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR, BEHAVERIFY_VENV, RESULTS_VENV, TEST_DIR, USER


def generate(write_location):
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command = TEST_DIR + '/' + USER + '.sh ' + TEST_DIR + ' ' + BEHAVERIFY_VENV
    serene_exec(behaverify, command, 'Results Script', True)
    copy_out_of(behaverify, TEST_DIR + '/examples', write_location + '.tar')

if __name__ == '__main__':
    generate(sys.argv[1])
