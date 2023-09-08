#!/bin/bash

nuXmvLoc=$1

docker start behaverify
docker cp $nuXmvLoc behaverify:/behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv
docker exec behaverify chmod +x /behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv
docker stop behaverify
