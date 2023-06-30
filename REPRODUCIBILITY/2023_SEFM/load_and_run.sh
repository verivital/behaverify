#!/bin/bash

nuXmvLoc=$1
outputLoc=$2

./docker_load_script.sh
echo "docker load finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
./docker_test_install.sh $outputLoc
echo "installation test finished!"
./docker_replicate_partial.sh $outputLoc
echo "replication of partial results finished!"
./docker_replicate_results.sh $outputLoc
echo "replication of results finished!"
