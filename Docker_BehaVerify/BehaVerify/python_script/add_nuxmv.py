import argparse
import docker
from docker_util import copy_into, serene_exec, TEST_DIR, CONTAINER_NAME

def add_nuxmv(nuxmv_location):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    behaverify = client.containers.get(CONTAINER_NAME)
    behaverify.start()
    # https://stackoverflow.com/questions/46390309/how-to-copy-a-file-from-host-to-container-using-docker-py-docker-sdk
    # https://docker-py.readthedocs.io/en/stable/containers.html
    # docker_copy_util.copy_into(behaverify, nuxmv_location, '/home/behaverify/nuXmv')
    print('Start: Adding nuXmv to container: ' + CONTAINER_NAME)
    if not copy_into(behaverify, nuxmv_location, TEST_DIR + '/'):
        raise RuntimeError('Failed to copy nuXmv into the container.')
    print('End: Adding nuXmv to container: ' + CONTAINER_NAME)
    serene_exec(behaverify, 'sudo chmod +x ' + TEST_DIR + '/nuXmv', 'Making nuXmv runnable (running chmod).', True)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('nuxmv_location')
    args = arg_parser.parse_args()
    add_nuxmv(args.nuxmv_location)
