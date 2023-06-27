#!/bin/bash

fileLoc=$1

./docker_build_script.sh
echo "docker build finished!"
./docker_test_install.sh $fileLoc
echo "installation test finished!"
./docker_replicate_results.sh $fileLoc
echo "replication of results finished!"
