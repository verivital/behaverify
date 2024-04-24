#!/bin/bash

docker load -i behaverify_img.tar
docker container create -i -t --name behaverify behaverify_img
