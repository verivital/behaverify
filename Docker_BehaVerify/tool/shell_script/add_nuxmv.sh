#!/bin/bash

USER=behaverify
nuXmvLoc=$1

docker start behaverify
docker cp $nuXmvLoc behaverify:"/home/${USER}/nuXmv"
docker exec behaverify chmod +x "/home/${USER}/nuXmv"
docker stop behaverify
