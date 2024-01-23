#!/bin/bash

docker start behaverify
docker exec behaverify rm -rf /home/user/behaverify
./docker_behaverify_clone.sh
docker stop behaverify
