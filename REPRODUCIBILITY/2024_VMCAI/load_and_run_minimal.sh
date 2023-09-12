#!/bin/bash

nuXmvLoc=$1
outputLoc=$2

if ! test -f "${nuXmvLoc}"; then
    echo "${nuXmvLoc} is not a file. Exiting"
    exit 1
fi
if ! test -d "${outputLoc}"; then
    echo "${outputLoc} is not a folder. Exiting"
    exit 1
fi

./docker_load_script.sh
echo "docker load finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
./docker_test_install.sh $outputLoc
echo "installation test finished!"
