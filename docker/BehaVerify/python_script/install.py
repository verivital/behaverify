import argparse
import docker
from docker_util import IMAGE_NAME, CONTAINER_NAME

def create_image_and_container(dockerfile_path):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Building image: ' + IMAGE_NAME)
    (behaverify_img, logs) = client.images.build(path = dockerfile_path, tag = IMAGE_NAME + ':latest')
    print('End: Building image: ' + IMAGE_NAME)
    # behaverify = client.containers.create(client.images.get('behaverify_img'), command = '/bin/bash', name = 'behaverify', stdin_open = True, tty = True)
    print('Start: Creating container: ' + CONTAINER_NAME)
    behaverify = client.containers.create(behaverify_img, command = '/bin/bash', name = CONTAINER_NAME, stdin_open = True, tty = True)
    print('End: Creating container: ' + CONTAINER_NAME)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path)
