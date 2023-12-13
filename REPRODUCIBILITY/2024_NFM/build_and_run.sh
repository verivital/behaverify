#!/bin/bash

nuXmvLoc=$1
outputLoc=$2
mode=$3

if ! test -f "${nuXmvLoc}"; then
    echo "${nuXmvLoc} is not a file. Exiting"
    exit 1
fi
if ! test -d "${outputLoc}"; then
    echo "${outputLoc} is not a folder. Exiting"
    exit 1
fi

./docker_build_script.sh
echo "docker build finished!"
./docker_add_nuxmv.sh $nuXmvLoc
echo "added nuXmv!"
if [[ "${mode}" == "full" ]]; then
    echo "running full results"
    mode="behaverify_nfm_full_results"
elif [[ "${mode}" == "partial" ]]; then
    echo "running partial results"
    mode="behaverify_nfm_partial_results"
elif [[ "${mode}" == "test" ]]; then
    echo "testing install"
    mode="behaverify_nfm_install_test"
else
    echo "unknown mode, defaulting to testing install"
    mode="behaverify_nfm_install_test"
fi


./docker_replicate_results.sh $outputLoc $mode
echo "finished!"
