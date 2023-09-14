#!/bin/bash

fileLoc=$1
to_gen=$2
if ! test -d "${fileLoc}"; then
    echo "${fileLoc} is not a folder. Exiting"
    exit 1
fi

if [[ "${fileLoc: -1}" != "/" ]]; then
    fileLoc="{fileLoc}/"
fi

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2024_VMCAI/results_script.sh /behaverify/REPRODUCIBILITY/2024_VMCAI/ $to_gen
docker cp behaverify:/behaverify/REPRODUCIBILITY/2024_VMCAI/examples/. "${fileLoc}behaverify_results"
docker stop behaverify
