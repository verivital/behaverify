#!/bin/bash


min_val=50
max_val=1000
step_size=50

if [[ $# -eq 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

path_name="../../examples/MoVe4BT"
exp_name="binary_tree"
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
tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_invar test_invar_silent test_states test_states_silent test_model"
echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
./clean_temp.sh



path_name="../../examples/BT2BIP"
exp_name="MarsRover"
echo "${path_name} ${exp_name}" > ./exp_info

range_string="0"
echo "${range_string}" > ./range_info

#encodings="no_opt last_opt first_opt full_opt"
encodings="full_opt"
echo "${encodings}" > ./encoding_info

#tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_model test_states test_states_silent"
tests="test_invar test_invar_silent test_states test_states_silent test_model"
echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
./clean_temp.sh
path_name="../../examples/BT2BIP"
exp_name="TrainControl"
echo "${path_name} ${exp_name}" > ./exp_info

range_string="0"
echo "${range_string}" > ./range_info

#encodings="no_opt last_opt first_opt full_opt"
encodings="full_opt"
echo "${encodings}" > ./encoding_info

#tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_model test_states test_states_silent"
tests="test_invar test_invar_silent test_states test_states_silent test_model"
echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
./clean_temp.sh


path_name="../../examples/BT2Fiacre"
exp_name="drone3"
echo "${path_name} ${exp_name}" > ./exp_info

range_string="0 1 2 3 4 5 6"
echo "${range_string}" > ./range_info

#encodings="no_opt last_opt first_opt full_opt"
encodings="full_opt"
echo "${encodings}" > ./encoding_info

#tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_model test_states test_states_silent"
tests="test_ctl test_ctl_silent test_ltl test_ltl_silent test_invar test_invar_silent test_states test_states_silent test_model"
echo "${tests}" > ./test_info

./run_encoding.sh ./exp_info ./range_info ./encoding_info ./test_info
./clean_temp.sh
