import argparse
import docker
from docker_util import CONTAINER_NAME, IMAGE_NAME

def create_image_and_container(dockerfile_path):
    '''creates nurv_img (Docker Image) and nurv (Docker Container)'''
    client = docker.from_env()
    print('Start: Building image: ' + IMAGE_NAME)
    (image, logs) = client.images.build(path = dockerfile_path, tag = IMAGE_NAME + ':latest')
    print('End: Building Image: ' + IMAGE_NAME)
    print('Start: Creating Container: ' + CONTAINER_NAME)
    container = client.containers.create(image, command = '/bin/bash', name = CONTAINER_NAME, stdin_open = True, tty = True)
    print('End: Creating Container: ' + CONTAINER_NAME)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path)
