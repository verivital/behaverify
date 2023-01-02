#!/bin/bash

folders=("models_BTCompiler" "models_leaf_v2" "models_total_v2" "models_total_v3")


#for cur_val in {0..4}; do
    #cur_folder=${folders[$cur_val]}
for cur_folder in ${folders[@]}; do
    timeout_val=1m
    timeout_val_silent=5m
    fail_count=3
    fail_count_silent=3
    for sel_num in {1..50}; do
	echo $sel_num $cur_folder
	#timeout $timeout_val ./run_tests.sh checklist $cur_folder $sel_num
	echo "states"
	timeout 7s ./run_states.sh parallel-checklist $cur_folder $sel_num
	echo "states_silent"
	timeout 7s ./run_states_silent.sh parallel-checklist $cur_folder $sel_num
	echo "model"
	timeout 7s ./run_model.sh parallel-checklist $cur_folder $sel_num
	echo "ltl_silent"
	echo $timeout_val_silent
	timeout $timeout_val_silent ./run_ltl_silent.sh parallel-checklist $cur_folder $sel_num
	if [ $? == 124 ]; then
	    fail_count_silent=$(($fail_count_silent-1))
	    if [ $fail_count_silent == 0 ]; then
		timeout_val_silent=1s
	    fi
	fi
	echo "ltl"
	timeout $timeout_val ./run_ltl.sh parallel-checklist $cur_folder $sel_num
	if [ $? == 124 ]; then
	    fail_count=$(($fail_count-1))
	    if [ $fail_count == 0 ]; then
		timeout_val=1s
	    fi
	fi
    done
done
