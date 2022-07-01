#!/bin/bash


folders=("blueROV" "checklist" "parallel-checklist")

for folder in ${folders[@]}; do
    echo $folder
    ./$folder-run_minimal.sh
done
