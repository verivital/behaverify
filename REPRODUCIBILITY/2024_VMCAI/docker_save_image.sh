#!/bin/bash

docker build -t behaverify_img:latest - < Dockerfile
docker save behaverify_image:latest > ~/behaverify_img.tar
#there are errors to trying to save fancier directories.
