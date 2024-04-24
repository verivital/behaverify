#!/bin/bash

min_val=5
max_val=10
step_size=5


path_name="../../examples/ANSR_no_net"
exp_name="ANSR_no_net"

echo "${path_name} ${exp_name}" > ./exp_info

range_string=""

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    range_string="${range_string} ${num}"
done

echo "${range_string}" > ./range_info


encodings="no_opt last_opt first_opt full_opt"

echo "${encodings}" > ./encoding_info

tests="test_ctl test_ctl_silent test_model test_states test_states_silent"

echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info

./clean_temp.sh
