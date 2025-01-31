#!/bin/bash

python_command=python3
min_val=5
max_val=10
step_size=5

if [[ "$#" -ge 1 ]]; then
    python_command=$1
fi

path_name="../../examples/ISR"
if test -e "${path_name}/processed_data"; then
    rm -r "${path_name}/processed_data"
fi
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/pictures"
mkdir "${path_name}/processed_data/pictures/counterexample_for_5"

$python_command "${path_name}/parse_nuxmv_output.py" "${path_name}/results/CTL_full_opt_ISR_5.txt" "${path_name}/processed_data/pictures/counterexample_for_5/11x11" 11 11
