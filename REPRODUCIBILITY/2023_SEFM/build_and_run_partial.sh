#!/bin/bash

nuXmvLoc=$1
outputLoc=$2
no_haskell=$3

if [[ "$no_haskell" == "no_haskell" ]]; then
    echo "Haskell will NOT be installed or used."
else
    echo "Haskell WILL be installed and used."
fi

./docker_build_script.sh $no_haskell
echo "docker build finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
./docker_replicate_partial.sh $outputLoc $no_haskell
echo "replication of partial results finished!"
