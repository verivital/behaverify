#!/bin/bash

fileLoc=$1
script=$2

if ! test -d "${fileLoc}"; then
    echo "First Argument should be a writable folder. ${fileLoc} is not a folder. Exiting"
    exit 1
fi

if [[ "${fileLoc: -1}" != "/" ]]; then
    fileLoc="${fileLoc}/"
fi

docker start behaverify
docker exec behaverify "/home/user/behaverify/REPRODUCIBILITY/2024_NFM/${script}.sh" /home/user/behaverify/REPRODUCIBILITY/2024_NFM/
docker cp behaverify:/home/user/behaverify/REPRODUCIBILITY/2024_NFM/examples/. "${fileLoc}${script}"
docker stop behaverify
