#!/bin/bash

echo "Now ensuring we will have no name conflicts."
echo "This script will attempt to stop the BehaVerify container, remove it, and then remove the image."
echo "If the container does not exist, errors will be produced by Docker, but this will not prevent the script from installing BehaVerify."
echo "The only potential flaw is if the container exists and isn't removed"
docker stop nurv
docker container rm nurv
docker image rm nurv
./install.sh
