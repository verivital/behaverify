import argparse
import docker
from docker_copy_util import copy_into

def add_nuxmv(nuxmv_location):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    behaverify = client.containers.get('behaverify')
    behaverify.start()
    # https://stackoverflow.com/questions/46390309/how-to-copy-a-file-from-host-to-container-using-docker-py-docker-sdk
    # https://docker-py.readthedocs.io/en/stable/containers.html
    #docker_copy_util.copy_into(behaverify, nuxmv_location, '/home/behaverify/nuXmv')
    print('Copying nuXmv into the container.')
    if not copy_into(behaverify, nuxmv_location, '/home/behaverify/'):
        raise RuntimeError('Failed to copy nuXmv into the container.')
    print('Copyied nuXmv into the container.')
    print('Making nuXmv runnable.')
    behaverify.exec_run('chmod +x /home/behaverify/nuXmv')
    print('Made nuXmv runnable.')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('nuxmv_location')
    args = arg_parser.parse_args()
    add_nuxmv(args.nuxmv_location)
