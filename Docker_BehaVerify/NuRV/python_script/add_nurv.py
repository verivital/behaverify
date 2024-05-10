import argparse
import os
import docker
from docker_util import copy_into, serene_exec, HOME_DIR, CONTAINER_NAME, NURV_LOC

def add_nurv(nurv_location):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    container = client.containers.get(CONTAINER_NAME)
    container.start()
    # https://stackoverflow.com/questions/46390309/how-to-copy-a-file-from-host-to-container-using-docker-py-docker-sdk
    # https://docker-py.readthedocs.io/en/stable/containers.html
    #docker_copy_util.copy_into(behaverify, nuxmv_location, '/home/behaverify/nuXmv')
    print('Start: Adding NuRV to container.')
    if not copy_into(container, nurv_location, HOME_DIR):
        raise RuntimeError('Failed to copy NuRV into the container.')
    print('End: Adding NuRV to container.')
    serene_exec(container, 'tar -xf ' + HOME_DIR + '/' + os.path.basename(nurv_location), 'Extracting NuRV.', True)
    serene_exec(container, 'sudo chmod +x ' + NURV_LOC, 'Making NuRV runnable (running chmod).', True)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('nurv_location')
    args = arg_parser.parse_args()
    add_nurv(args.nurv_location)
