import argparse
import docker
from install import create_image_and_container
from docker_util import IMAGE_NAME, CONTAINER_NAME

def reinstall(dockerfile_path, nuxmv_loc, local):
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
    create_image_and_container(dockerfile_path, nuxmv_loc, local)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    arg_parser.add_argument('--nuxmv_loc', type = str, default = None)
    arg_parser.add_argument('--local', action = 'store_true')
    args = arg_parser.parse_args()
    reinstall(args.input_path, args.nuxmv_loc, args.local)
