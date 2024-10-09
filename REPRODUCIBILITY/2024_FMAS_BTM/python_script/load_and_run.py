import sys
import os
import load_image
import add_nuxmv
import generate

dockerimage_path = sys.argv[1]
nuxmv_location = sys.argv[2]
mode = sys.argv[3]
write_location = sys.argv[4]
if not os.path.exists(dockerimage_path):
    print('you did not point to a dockerimage, exiting')
    sys.exit()
if not os.path.exists(nuxmv_location):
    print('you did not point to nuXmv, exiting')
    sys.exit()
if mode not in ('install', 'partial', 'full'):
    print(mode + ' must be one of install, partial, full. Exiting')
    sys.exit()
if os.path.exists(write_location):
    print('write location exists, exiting')
    sys.exit()
if not os.path.isdir(os.path.dirname(write_location)):
    print('write location parent director doen not exist, exiting')
    sys.exit()

load_image.reinstall(dockerimage_path)
add_nuxmv.add_nuxmv(nuxmv_location)
generate.generate(mode, write_location)
