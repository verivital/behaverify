import argparse
import tarfile
import docker
from docker_util import IMAGE_NAME, CONTAINER_NAME

def create_image_and_container(dockerfile_path):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Building new BehaVerify Image.')
    (behaverify_img, logs) = client.images.build(path = dockerfile_path, tag = IMAGE_NAME + ':latest')
    print('End: Building new BehaVerify Image.')
    print('Start: Saving BehaVerify Image.')
    with open('./DockerImage.tar', 'wb') as destination_file:
        for chunk in behaverify_img.save(named = True):
            destination_file.write(chunk)
    print('End: Saving new BehaVerify Container.')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path)
