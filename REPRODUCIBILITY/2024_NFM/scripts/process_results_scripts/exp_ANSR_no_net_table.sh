#!/bin/bash

min_val=5
max_val=10
step_size=5

path_name="../../examples/ANSR_no_net"

rm -r "${path_name}/processed_data"
mkdir "${path_name}/processed_data"
mkdir "${path_name}/processed_data/pictures"

python3 "${path_name}/parse_nuxmv_output.py" "${path_name}/results/CTL_full_opt_ANSR_no_net_5.txt" "${path_name}/processed_data/pictures/ANSR_no_net_5_counterexample" 11 11
