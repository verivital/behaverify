#!/bin/bash

docker start behaverify
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_sefm/minimal_script.sh
docker exec behaverify /behaverify/REPRODUCIBILITY/2023_sefm/gather_data.sh
docker cp behaverify:/behaverify/REPRODUCIBILITY/2022_SEFM/examples/. ./behaverify_test
