#!/bin/bash

min_val=5
max_val=10
step_size=5

path_name="../../examples/ANSR_no_net"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/tables"
mkdir "${path_name}/processed_data/pictures"
encoding_groups=("opt")
for encoding_group in "${encoding_groups[@]}"; do
    mkdir "${path_name}/processed_data/tables/${encoding_group}"
    mkdir "${path_name}/processed_data/pictures/${encoding_group}"
done
mkdir "${path_name}/processed_data/pictures/counterexample_for_5"

python3 ./build_table.py --folder_name light_controller_v3 --file_name light_controller --minV $min_val --maxV $max_val --step $step_size --xLabel "No Label" --encodings "opt"

python3 "${path_name}/parse_nuxmv_output.py" "${path_name}/results/CTL_ANSR_no_net_5.smv" "${path_name}/processed_data/pictures/counterexample_for_5/11x11" 11 11
