#!/bin/bash

docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
docker builder prune
