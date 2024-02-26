import docker
from install import create_image_and_container

def reinstall():
    '''Stop behaverify (Docker Container), Remove behaverify (Docker Container), Remove behaverify_img (Docker Image)
    creates behaverify_img (Docker Image) and behaverify (Docker Container)'''
    client = docker.from_env()
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
    create_image_and_container()
    return

if __name__ == '__main__':
    reinstall()
