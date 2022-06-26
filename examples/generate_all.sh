#!/bin/bash

folders=("auto_example" "basic" "blueROV" "gcd" "robot" "robot-v2")
#folders=("robot-v2")

for folder in ${folders[@]}; do
    echo $folder
    pushd ./$folder/$folder
    ./generate.sh
    popd
done
