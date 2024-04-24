#!/bin/bash


min_val=2
max_val=9
step_size=1

if [[ $# -eq 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi
./clean_temp.sh

path_name="../../examples/ANSR_scaling_with_state"
exp_name="ANSR_scaling_with_state_flat"

echo "${path_name} ${exp_name}" > ./exp_info

range_string=""

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    range_string="${range_string} ${num}"
done

echo "${range_string}" > ./range_info


encodings="full_opt"

echo "${encodings}" > ./encoding_info

tests="test_ctl_silent test_model test_states_silent"

echo "${tests}" > ./test_info


./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
exp_name="ANSR_scaling_with_state_square"

echo "${path_name} ${exp_name}" > ./exp_info
./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info

./clean_temp.sh
