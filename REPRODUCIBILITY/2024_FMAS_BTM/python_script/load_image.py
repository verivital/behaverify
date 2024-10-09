import argparse
import docker
from install import create_image_and_container
from docker_util import IMAGE_NAME, CONTAINER_NAME

def reinstall(dockerimage_path):
    '''Stop behaverify (Docker Container), Remove behaverify (Docker Container), Remove behaverify_img (Docker Image)
    creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Removing container: ' + CONTAINER_NAME)
    try:
        behaverify = client.containers.get(CONTAINER_NAME)
        behaverify.stop()
        behaverify.remove()
    except docker.errors.NotFound:
        pass
    print('End: Removing container: ' + CONTAINER_NAME)
    print('Start: Removing image: ' + IMAGE_NAME)
    try:
        behaverify_img = client.images.get(IMAGE_NAME)
        behaverify_img.remove()
    except docker.errors.ImageNotFound:
        pass
    print('End: Removing image: ' + IMAGE_NAME)
    print('Start: Loading image from file')
    with open(dockerimage_path, 'rb') as tar_file:
        behaverify_img = client.images.load(tar_file.read())[0]
    print('End: Loading image from file')
    print('Start: Creating container: ' + CONTAINER_NAME)
    behaverify = client.containers.create(behaverify_img, command = '/bin/bash', name = CONTAINER_NAME, stdin_open = True, tty = True)
    print('End: Creating container: ' + CONTAINER_NAME)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    reinstall(args.input_path)
