#!/bin/bash

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_sefm/full_script.sh
docker cp behaverify:/behaverify/REPRODUCIBILITY/2022_SEFM/examples/. ./behaverify_results
