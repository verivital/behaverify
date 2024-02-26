import argparse
import docker

def add_nuxmv(nuxmv_location):
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    try:
        behaverify = client.containers.get('behaverify')
        behaverify.start()
        # https://stackoverflow.com/questions/46390309/how-to-copy-a-file-from-host-to-container-using-docker-py-docker-sdk
        # https://docker-py.readthedocs.io/en/stable/containers.html
        behaverify.exec_run('chmod +x /home/behaverify/nuXmv')
    behaverify = client.containers.create(client.images.get('behaverify_img'), command = '/bin/bash', name = 'behaverify')
    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('nuxmv_location')
    args = arg_parser.parse_args()
    add_nuxmv(args.nuxmv_location)
