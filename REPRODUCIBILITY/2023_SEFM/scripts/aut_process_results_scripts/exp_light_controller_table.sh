#!/bin/bash

min_val=1
max_val=1
step_size=1

# if [ "$#" == 3 ]; then
#     min_val=$1
#     max_val=$2
#     step_size=$3
# fi

path_name="../../examples/light_controller"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("opt")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done

python3 ./build_table.py --folder_name light_controller --file_name light_controller --minV $min_val --maxV $max_val --step $step_size --xLabel "No Label" --encodings "opt"
