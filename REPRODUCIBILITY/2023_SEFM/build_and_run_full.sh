#!/bin/bash

nuXmvLoc=$1
outputLoc=$2

./docker_build_script.sh
echo "docker build finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
./docker_replicate_results.sh $outputLoc
echo "replication of results finished!"
