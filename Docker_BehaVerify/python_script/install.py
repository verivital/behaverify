import argparse
import docker

def create_image_and_container(dockerfile_path):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Building new BehaVerify Image.')
    (behaverify_img, logs) = client.images.build(path = dockerfile_path, tag = 'behaverify_img:latest')
    print('End: Building new BehaVerify Image.')
    # behaverify = client.containers.create(client.images.get('behaverify_img'), command = '/bin/bash', name = 'behaverify', stdin_open = True, tty = True)
    print('Start: Creating new BehaVerify Container.')
    behaverify = client.containers.create(behaverify_img, command = '/bin/bash', name = 'behaverify', stdin_open = True, tty = True)
    print('End: Creating new BehaVerify Container.')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path)
