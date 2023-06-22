#!/bin/bash

min_val=1
max_val=50
step_size=1

if [ "$#" == 3 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi


path_name="../../examples/checklist_invar"
exp_name="checklist_parallel"

echo "${path_name} ${exp_name}" > ./exp_info

range_string=""

for ((num=min_val; num<=max_val; num=(num + step_size))); do
    range_string="${range_string} ${num}"
done

echo "${range_string}" > ./range_info


encodings="aut norm func no_internal s_var no_opt last_opt first_opt full_opt"

echo "${encodings}" > ./encoding_info

tests="test_model test_states test_states_silent"

echo "${tests}" > ./test_info


./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info

exp_name="checklist_sequence"

echo "${path_name} ${exp_name}" > ./exp_info


./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info


./clean_temp.sh
