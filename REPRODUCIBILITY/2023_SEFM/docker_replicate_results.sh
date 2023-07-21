#!/bin/bash

fileLoc=$1
no_haskell=$2

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_SEFM/results_script.sh /behaverify/REPRODUCIBILITY/2023_SEFM/ $no_haskell
docker cp behaverify:/behaverify/REPRODUCIBILITY/2023_SEFM/examples/. "${fileLoc}behaverify_results"
docker stop behaverify
