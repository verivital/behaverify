import argparse
import sys
import os
from reinstall import reinstall
from generate import generate


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('dockerfile_path')
arg_parser.add_argument('output_location')
arg_parser.add_argument('nuxmv_location')
arg_parser.add_argument('--local', action = 'store_true')
args = arg_parser.parse_args()

dockerfile_path = args.dockerfile_path
nuxmv_location = args.nuxmv_location
nuxmv_local = args.local
write_location = args.output_location
if not os.path.isdir(dockerfile_path):
    print('you did not point to a directory for dockerfile, exiting')
    sys.exit()
if nuxmv_local and (not os.path.exists(nuxmv_location)):
    print('you marked local but did not point to nuXmv, exiting')
    sys.exit()
if os.path.exists(write_location):
    print('write location exists, exiting')
    sys.exit()
if not os.path.isdir(os.path.dirname(write_location)):
    print('write location parent director doen not exist, exiting')
    sys.exit()

reinstall(dockerfile_path, nuxmv_location, nuxmv_local)
generate(write_location)
