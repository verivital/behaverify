#!/bin/bash

python_command=python3
min_val=50
max_val=1000
step_size=50

if [[ "$#" -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

path_name="../../examples/bigger_fish"
if test -e "${path_name}/processed_data"; then
    rm -r "${path_name}/processed_data"
fi
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
#encoding_groups=("opt")
encoding_groups=("bigger_fish")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
    $python_command ./build_table.py --folder_name bigger_fish --file_name bigger_fish --minV $min_val --maxV $max_val --step $step_size --xLabel "Number of Nodes" --encodings $encoding_group
done
