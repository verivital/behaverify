#!/bin/bash


min_val=2
max_val=9
step_size=1

if [[ "$#" -ge 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/ANSR_scaling_grid"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("full_opt")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done

python3 ./build_table.py --folder_name ANSR_scaling_grid --file_name ANSR_scaling_grid --minV $min_val --maxV $max_val --step $step_size --xLabel "n" --encodings "full_opt"
