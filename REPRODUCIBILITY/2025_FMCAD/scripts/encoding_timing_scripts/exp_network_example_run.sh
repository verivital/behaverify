#!/bin/bash


min_val=0
max_val=1
step_size=1

if [[ $# -eq 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/NetworkExample"
exp_name="network"
echo "${path_name} ${exp_name}" > ./exp_info

range_string=""
for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    range_string="${range_string} ${num}"
done
echo "${range_string}" > ./range_info

#encodings="no_opt last_opt first_opt full_opt"
encodings="full_opt"
echo "${encodings}" > ./encoding_info

#tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_model test_states test_states_silent"
tests="test_ctl test_ctl_silent test_invar test_invar_silent test_states test_states_silent"
echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
./clean_temp.sh
