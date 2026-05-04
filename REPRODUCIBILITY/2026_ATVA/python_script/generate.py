import sys
import os
import tarfile
import docker
from docker_util import copy_into, copy_out_of, serene_exec, CONTAINER_NAME, HOME_DIR, USER_DIR, BEHAVERIFY_VENV, RESULTS_VENV, TEST_DIR, USER


def generate(write_location):
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    command = TEST_DIR + '/' + USER + '.sh ' + TEST_DIR + ' ' + BEHAVERIFY_VENV + ' ' + RESULTS_VENV
    serene_exec(behaverify, command, 'Results Script', True)

    # Copy results out of container
    tar_path = write_location + '.tar'
    copy_out_of(behaverify, TEST_DIR + '/examples', tar_path)

    # Extract the tar file to the specified directory
    os.makedirs(write_location, exist_ok=True)
    print(f'Extracting results to: {write_location}/')
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(write_location, filter='data')

    print(f'Results extracted. Key output files:')
    for root, dirs, files in os.walk(write_location):
        for f in files:
            if f.endswith('.png') or f.endswith('.pdf'):
                print(f'  {os.path.relpath(os.path.join(root, f), write_location)}')

if __name__ == '__main__':
    generate(sys.argv[1])
