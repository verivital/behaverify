#!/bin/bash

min_val=2
max_val=20
step_size=1

if [ "$#" == 3 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/simple_robot"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("all" "internal" "core" "aut" "func")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done

python3 ./build_table.py --folder_name simple_robot --file_name simple_robot --minV $min_val --maxV $max_val --step $step_size --xLabel "Grid Size" --encodings "all" "internal" "core" "aut" "func"
