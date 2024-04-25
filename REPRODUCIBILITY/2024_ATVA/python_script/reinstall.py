import argparse
import docker
from install import create_image_and_container
from docker_util import IMAGE_NAME, CONTAINER_NAME

def reinstall(dockerfile_path):
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
    create_image_and_container(dockerfile_path)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    reinstall(args.input_path)
