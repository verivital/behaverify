#!/bin/bash


folders=("auto_example" "basic" "blueROV" "gcd" "checklist" "parallel-checklist")
#folders=("basic" "blueROV")
#folders=("robot")
#folders=("blueROV")

for folder in ${folders[@]}; do
    echo $folder
    ./$folder-run_all.sh
done
