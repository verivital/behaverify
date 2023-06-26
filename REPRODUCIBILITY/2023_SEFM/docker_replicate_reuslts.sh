#!/bin/bash

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_SEFM/results_script.sh /behaverify/REPRODUCIBILITY/2023_SEFM/
docker cp behaverify:/behaverify/REPRODUCIBILITY/2022_SEFM/examples/. ./behaverify_results
