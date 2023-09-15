#!/bin/bash

fileLoc=$1

if ! test -d "${fileLoc}"; then
    echo "First Argument should be a writable folder. ${fileLoc} is not a folder. Exiting"
    exit 1
fi

if [[ "${fileLoc: -1}" != "/" ]]; then
    fileLoc="{fileLoc}/"
fi
use_haskell=1
to_gen=3
if [[ $# -ge 2 ]]; then
    use_haskell=$2
fi
if [[ $# -ge 3 ]]; then
    to_gen=$3
fi

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2024_VMCAI/test_script.sh /behaverify/REPRODUCIBILITY/2024_VMCAI/ $use_haskell $to_gen
docker cp behaverify:/behaverify/REPRODUCIBILITY/2024_VMCAI/examples/. "${fileLoc}behaverify_install_test_results"
docker stop behaverify
