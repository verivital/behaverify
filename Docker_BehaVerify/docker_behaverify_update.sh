#!/bin/bash

user=behaverify

docker start behaverify
docker exec behaverify rm -rf "/home/${user}/behaverify"
docker exec behaverify rm -rf "/home/${user}/behaverify_venv" 
./docker_behaverify_clone.sh
docker stop behaverify
