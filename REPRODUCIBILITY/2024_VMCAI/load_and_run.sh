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
use_haskell=1
to_gen=5000
if [[ $# -ge 2 ]]; then
    use_haskell=$3
fi
if [[ $# -ge 3 ]]; then
    to_gen=$4
fi

./docker_load_script.sh
echo "docker load finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
./docker_test_install.sh $outputLoc $use_haskell $to_gen
echo "installation test finished!"
./docker_replicate_partial.sh $outputLoc $use_haskell $to_gen
echo "replication of partial results finished!"
./docker_replicate_results.sh $outputLoc $use_haskell $to_gen
echo "replication of results finished!"
