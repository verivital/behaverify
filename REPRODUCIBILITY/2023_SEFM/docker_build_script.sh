#!/bin/bash

no_haskell=$1

if [[ "$no_haskell" == "no_haskell" ]]; then
    echo "building container without haskell!"
    docker build -t behaverify_img:latest - < Dockerfile.no_haskell
    docker container create -i -t --name behaverify behaverify_img
else
    echo "building container with haskell!"
    docker build -t behaverify_img:latest - < Dockerfile.haskell
    docker container create -i -t --name behaverify behaverify_img
fi

