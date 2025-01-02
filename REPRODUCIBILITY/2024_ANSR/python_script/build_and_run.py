import sys
import os
import reinstall
import add_nuxmv
import generate

dockerfile_path = sys.argv[1]
nuxmv_location = sys.argv[2]
mode = sys.argv[3]
write_location = sys.argv[4]
if not os.path.isdir(dockerfile_path):
    print('you did not point to a directory for dockerfile, exiting')
    sys.exit()
if not os.path.exists(nuxmv_location):
    print('you did not point to nuXmv, exiting')
    sys.exit()
if mode not in ('install', 'full', 'timeout'):
    print(mode + ' must be one of install, full, timeout. Exiting')
    sys.exit()
if os.path.exists(write_location):
    print('write location exists, exiting')
    sys.exit()
if not os.path.isdir(os.path.dirname(write_location)):
    print('write location parent director doen not exist, exiting')
    sys.exit()

reinstall.reinstall(dockerfile_path)
add_nuxmv.add_nuxmv(nuxmv_location)
generate.generate(mode, write_location)
