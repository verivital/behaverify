#!/bin/bash

fileLoc=$1

if [[ "${fileLoc: -1}" != "/" ]]; then
    fileLoc="{fileLoc}/"
fi

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2024_VMCAI/test_script.sh /behaverify/REPRODUCIBILITY/2024_VMCAI/
docker cp behaverify:/behaverify/REPRODUCIBILITY/2024_VMCAI/examples/. "${fileLoc}behaverify_install_test_results"
docker stop behaverify
