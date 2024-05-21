import argparse
import docker
from install import create_image_and_container
from docker_util import CONTAINER_NAME, IMAGE_NAME

def reinstall(dockerfile_path):
    '''Stop (Docker Container), Remove (Docker Container), Remove (Docker Image)
    creates (Docker Image) and (Docker Container)'''
    client = docker.from_env()
    print('Start: Removing old docker image and container.')
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        pass
    try:
        image = client.images.get(IMAGE_NAME)
        image.remove()
    except docker.errors.ImageNotFound:
        pass
    print('End: Removing old docker image and container.')
    create_image_and_container(dockerfile_path)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    reinstall(args.input_path)
