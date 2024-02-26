#!/bin/bash

docker start behaverify
docker exec -w '/home/behaverify/behaverify' behaverify git pull
docker exec behaverify '/home/behaverify/behaverify_venv/bin/python3' -m pip install --upgrade pip
docker exec behaverify '/home/behaverify/behaverify_venv/bin/python3' -m pip install -r '/home/behaverify/behaverify/Docker_BehaVerify/Additional_Files/requirements.txt'
docker stop behaverify
