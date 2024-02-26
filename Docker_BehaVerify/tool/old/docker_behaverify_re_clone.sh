#!/bin/bash

docker start behaverify
docker exec behaverify rm -rf "/home/behaverify/behaverify"
docker exec behaverify rm -rf "/home/behaverify/behaverify_venv" 
./docker_behaverify_clone.sh
docker stop behaverify
