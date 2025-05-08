import argparse
import docker
from docker_util import IMAGE_NAME, CONTAINER_NAME, TEST_DIR, serene_exec, copy_into

def create_image_and_container(dockerfile_path, nuxmv_loc, local):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    print('Start: Building image: ' + IMAGE_NAME)
    (behaverify_img, logs) = client.images.build(path = dockerfile_path, tag = IMAGE_NAME + ':latest')
    print('End: Building image: ' + IMAGE_NAME)
    print('Start: Creating container: ' + CONTAINER_NAME)
    behaverify = client.containers.create(behaverify_img, command = '/bin/bash', name = CONTAINER_NAME, stdin_open = True, tty = True)
    print('End: Creating container: ' + CONTAINER_NAME)
    behaverify.start()
    if nuxmv_loc is not None:
        if local:
            print('Start: Adding nuXmv to container: ' + CONTAINER_NAME)
            if not copy_into(behaverify, nuxmv_loc, TEST_DIR + '/'):
                raise RuntimeError('Failed to copy nuXmv into the container.')
            print('End: Adding nuXmv to container: ' + CONTAINER_NAME)
        else:
            serene_exec(behaverify, 'wget ' + nuxmv_loc + ' -O ' + TEST_DIR + '/nuXmv_DL.tar.xz', 'Downloading nuXmv from provided URL.', True)
            serene_exec(
                behaverify,
                'tar -xf ' + TEST_DIR + '/nuXmv_DL.tar.xz' + ' --one-top-level=nuXmv_DL --strip-components 1',
                'Extracting nuXmv from archive.',
                True
            )
            serene_exec(behaverify, 'mv ' + TEST_DIR + '/nuXmv_DL/bin/nuXmv' + ' ' + TEST_DIR + '/nuXmv', 'Moving nuXmv from extracted location.', True)
        serene_exec(behaverify, 'sudo chmod +x ' + TEST_DIR + '/nuXmv', 'Making nuXmv runnable (running chmod).', True)
    else:
        print('nuXmv was not included! This container will not be able to execute nuXmv, but it will still be able to generate nuXmv files for you to use elsewhere.')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    arg_parser.add_argument('--nuxmv_loc', type = str, default = None)
    arg_parser.add_argument('--local', action = 'store_true')
    args = arg_parser.parse_args()
    create_image_and_container(args.input_path, args.nuxmv_loc, args.local)
