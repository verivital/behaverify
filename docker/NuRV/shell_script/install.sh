#!/bin/bash

docker build -t nurv_img:latest - < Dockerfile
docker container create -i -t --name nurv nurv_img
./add_nurv.sh
