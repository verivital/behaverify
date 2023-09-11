#!/bin/bash

nuXmvLoc=$1

docker start behaverify
docker cp $nuXmvLoc behaverify:/behaverify/REPRODUCIBILITY/2024_VMCAI/nuXmv
docker exec behaverify chmod +x /behaverify/REPRODUCIBILITY/2024_VMCAI/nuXmv
docker stop behaverify
