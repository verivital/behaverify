#!/bin/bash

folders=("blueROV" "checklist" "parallel-checklist")

for folder in ${folders[@]}; do
    echo $folder
    pushd ./$folder/$folder
    ./generate_memtime.sh
    popd
done
