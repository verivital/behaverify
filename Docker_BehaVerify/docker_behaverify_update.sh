#!/bin/bash

docker start behaverify
docker exec -w /home/user/behaverify behaverify git pull
docker stop behaverify