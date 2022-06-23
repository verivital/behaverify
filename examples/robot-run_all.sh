#!/bin/bash

folders=("models_BTCompiler" "models_leaf" "models_total" "models_total_errorless" "models_leaf_no_IVAR" "models_total_no_IVAR" "models_total_no_IVAR_errorless" "models_total_no_IVAR_errorless_unique_child")
folders=("models_total")

for cur_val in {0..7}; do
    cur_folder=${folders[$cur_val]}
    timeout_val=5m
    for sel_num in {1..50}; do
	echo $sel_num $cur_folder
	timeout $timeout_val ./run_tests.sh robot $cur_folder $sel_num
	if [ $? == 0 ]; then
	    timeout_val=15s
	fi
    done
done
