#!/bin/bash

USER=NuRV
NuRVLoc='/home/serene/tools/NuRV-2.0.0-linuxx64'

docker start nurv
docker cp $NuRVLoc nurv:"/home/${USER}/NuRV"
docker exec nurv chmod +x "/home/${USER}/NuRV/NuRV"
docker stop nurv
