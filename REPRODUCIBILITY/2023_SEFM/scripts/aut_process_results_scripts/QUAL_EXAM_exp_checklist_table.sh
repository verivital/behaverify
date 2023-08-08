#!/bin/bash

min_val=1
max_val=50
step_size=1

if [ "$#" == 4 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/checklist"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("qual")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done

python3 ./build_table.py --folder_name checklist --file_name checklist_parallel checklist_sequence --minV $min_val --maxV $max_val --step $step_size --xLabel "Number of Checks" --encodings "qual"
