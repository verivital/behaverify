#!/bin/bash

folders=("auto_example" "basic" "blueROV" "gcd" "checklist" "parallel-checklist")

for folder in ${folders[@]}; do
    echo $folder
    pushd ./$folder/$folder
    ./generate.sh
    popd
done
