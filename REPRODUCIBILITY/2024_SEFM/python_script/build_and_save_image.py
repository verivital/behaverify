import argparse
import tarfile
import docker
from docker_util import IMAGE_NAME, CONTAINER_NAME

def create_image_and_container(dockerfile_path):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
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
    print('Start: Building image: ' + IMAGE_NAME)
    (behaverify_img, logs) = client.images.build(path = dockerfile_path, tag = IMAGE_NAME + ':latest')
    print('End: Building image: ' + IMAGE_NAME)
    print('Start: Saving image: ' + IMAGE_NAME)
    with open('./DockerImage.tar', 'wb') as destination_file:
        for chunk in behaverify_img.save(named = True):
            destination_file.write(chunk)
    print('End: Saving image: ' + IMAGE_NAME)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path)
