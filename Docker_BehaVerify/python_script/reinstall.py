import argparse
import docker
from install import create_image_and_container

def reinstall(dockerfile_path):
    '''Stop behaverify (Docker Container), Remove behaverify (Docker Container), Remove behaverify_img (Docker Image)
    creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Removing old behaverify docker.')
    try:
        behaverify = client.containers.get('behaverify')
        behaverify.stop()
        behaverify.remove()
    except docker.errors.NotFound:
        pass
    try:
        behaverify_img = client.images.get('behaverify_img')
        behaverify_img.remove()
    except docker.errors.ImageNotFound:
        pass
    print('Old behaverify docker removed.')
    create_image_and_container(dockerfile_path)
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    reinstall(args.input_path)
