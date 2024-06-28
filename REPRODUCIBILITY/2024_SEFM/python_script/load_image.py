import argparse
import docker
from install import create_image_and_container
from docker_util import IMAGE_NAME, CONTAINER_NAME

def reinstall(dockerimage_path):
    '''Stop behaverify (Docker Container), Remove behaverify (Docker Container), Remove behaverify_img (Docker Image)
    creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Removing old behaverify docker image and container.')
    try:
        behaverify = client.containers.get(CONTAINER_NAME)
        behaverify.stop()
        behaverify.remove()
    except docker.errors.NotFound:
        pass
    try:
        behaverify_img = client.images.get(IMAGE_NAME)
        behaverify_img.remove()
    except docker.errors.ImageNotFound:
        pass
    print('End: Removing old behaverify docker image and container.')
    with open(dockerimage_path, 'rb') as tar_file:
        behaverify_img = client.images.load(tar_file.read())[0]
    print('Start: Creating new BehaVerify Container.')
    behaverify = client.containers.create(behaverify_img, command = '/bin/bash', name = CONTAINER_NAME, stdin_open = True, tty = True)
    print('End: Creating new BehaVerify Container.')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    reinstall(args.input_path)
