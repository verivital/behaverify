import docker

def create_image_and_container():
    '''creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
    behaverify_img = client.images.build(path = '../common/', tag = 'behaverify_img:latest')
    behaverify = client.containers.create(client.images.get('behaverify_img'), command = '/bin/bash', name = 'behaverify')
    return

if __name__ == '__main__':
    create_image_and_container()
