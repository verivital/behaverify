#!/bin/bash

folders=("auto_example" "basic" "blueROV" "gcd" "robot")
#folders=("blueROV")

for folder in ${folders[@]}; do
    echo $folder
    pushd ./$folder/$folder
    ./generate.sh
    popd
done
