#!/bin/bash

docker build -t haskell_behaverify_img:latest - < Dockerfile
docker container create -i -t --name haskell_behaverify haskell_behaverify_img
