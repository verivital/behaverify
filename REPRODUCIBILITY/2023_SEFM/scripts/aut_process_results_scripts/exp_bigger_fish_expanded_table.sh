#!/bin/bash


min_val=50
max_val=600
step_size=50

if [ "$#" == 4 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/bigger_fish_expanded"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("opt")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done

python3 ./build_table.py --folder_name bigger_fish_expanded --file_name bigger_fish_parallel bigger_fish_sequence --minV $min_val --maxV $max_val --step $step_size --xLabel "Biggest Fish Check" --encodings "opt"
