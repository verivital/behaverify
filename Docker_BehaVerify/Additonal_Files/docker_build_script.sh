#!/bin/bash

docker build -t behaverify_img:latest - < Dockerfile
docker container create -i -t --name behaverify behaverify_img
