#!/bin/bash

current_location=$(pwd)
echo "Attempting to install BehaVerify"
cd ../common
docker build -t behaverify_img:latest - < Dockerfile
docker container create -i -t --name behaverify behaverify_img
cd $current_location
