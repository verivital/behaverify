#!/bin/bash

nuXmvLoc=$1

docker start behaverify
docker cp $nuXmvLoc behaverify:/home/user/behaverify/REPRODUCIBILITY/2024_NFM/nuXmv
docker exec behaverify chmod +x /home/user/behaverify/REPRODUCIBILITY/2024_NFM/nuXmv
docker stop behaverify
