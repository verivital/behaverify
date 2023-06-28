#!/bin/bash

fileLoc=$1

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_SEFM/partial_results_script.sh /behaverify/REPRODUCIBILITY/2023_SEFM/
docker cp behaverify:/behaverify/REPRODUCIBILITY/2023_SEFM/examples/. "${fileLoc}behaverify_partial_results"
docker stop behaverify
