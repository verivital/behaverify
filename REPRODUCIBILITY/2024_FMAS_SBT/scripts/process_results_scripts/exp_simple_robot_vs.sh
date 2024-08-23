#!/bin/bash

python_command=python3
min_val=2
max_val=30
step_size=4

if [[ "$#" -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

path_name="../../examples/simple_robot"
if ! test -e "${path_name}/processed_data"; then
    mkdir "${path_name}/processed_data"
fi
if ! test -e "${path_name}/processed_data/pictures"; then
    mkdir "${path_name}/processed_data/pictures"
fi

$python_command vs_MoVe4BT.py --folder_name simple_robot --file_name simple_robot --minV $min_val --maxV $max_val --step $step_size --xLabel "Grid Size" --encodings "vs_robot"
