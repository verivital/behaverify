import os
import tarfile
import io
import docker

VENUE = '2024_FMAS_SBT'
USER = 'BehaVerify_' + VENUE
HOME_DIR = '/home/' + USER
TEST_DIR = HOME_DIR + '/behaverify/REPRODUCIBILITY/' + VENUE
CONTAINER_NAME = USER.lower()
IMAGE_NAME = CONTAINER_NAME + '_img'

def serene_exec(container, command, message, error_check):
    print('Start: ' + message)
    (_, exec_stream) = container.exec_run(command, stream = True)
    for data in exec_stream:
        print(data.decode())
    print('End: ' + message + (' <::> Check if errors were printed!' if error_check else ''))
    return

def copy_into(container, source_path, destination_path):
    '''note! Destination path is the folder where it will be unzipped! Not a direct path!'''
    stream = io.BytesIO()
    with tarfile.open(fileobj = stream, mode = 'w|') as tar_object:
        if os.path.isdir(source_path):
            (path_head, path_tail) = os.path.split(source_path)
            if path_tail == '':
                (path_head, path_tail) = os.path.split(path_head)
            tar_object.add(os.path.abspath(source_path), arcname = path_tail)
            stream.seek(0)
        else:
            with open(source_path, 'rb') as source_file:
                info = tar_object.gettarinfo(fileobj = source_file)
                info.name = os.path.basename(source_path)
                tar_object.addfile(info, source_file)
    return container.put_archive(destination_path, stream.getvalue())

def copy_out_of(container, source_path, destination_path):
    (bits, _) = container.get_archive(source_path)
    with open(destination_path, 'wb') as destination_file:
        for chunk in bits:
            destination_file.write(chunk)
    return
