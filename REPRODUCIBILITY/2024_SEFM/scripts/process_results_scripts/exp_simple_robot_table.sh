#!/bin/bash

python_command=python3
min_val=2
max_val=20
step_size=1

if [[ "$#" -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

path_name="../../examples/simple_robot"
if test -e "${path_name}/processed_data"; then
    rm -r "${path_name}/processed_data"
fi
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
#encoding_groups=("all" "internal" "core" "aut" "func" "opt")
#encoding_groups=("opt")
encoding_groups=("simple_robot")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
    $python_command ./build_table.py --folder_name simple_robot --file_name simple_robot --minV $min_val --maxV $max_val --step $step_size --xLabel "Grid Size" --encodings $encoding_group
done
