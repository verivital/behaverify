#!/bin/bash

folders=("models_BTCompiler")
mkdir -p ./results/checklist
mkdir -p ./results/parallel-checklist
mkdir -p ./processed_data/checklist
mkdir -p ./processed_data/parallel-checklist

for cur_folder in ${folders[@]}; do
    timeout_val_silent=7m
    fail_count_silent=5
    for sel_num in {1..50}; do
	echo $sel_num $cur_folder
	echo $timeout_val_silent
	timeout $timeout_val_silent ./run_ltl_silent.sh checklist $cur_folder $sel_num
	if [ $? == 124 ]; then
	    fail_count_silent=$(($fail_count_silent-1))
	    if [ $fail_count_silent == 0 ]; then
		timeout_val_silent=1s
	    fi
	fi
    done
done

python3 build_table.py checklist minimal

for cur_folder in ${folders[@]}; do
    timeout_val_silent=7m
    fail_count_silent=5
    for sel_num in {1..50}; do
	echo $sel_num $cur_folder
	echo $timeout_val_silent
	timeout $timeout_val_silent ./run_ltl_silent.sh parallel-checklist $cur_folder $sel_num
	if [ $? == 124 ]; then
	    fail_count_silent=$(($fail_count_silent-1))
	    if [ $fail_count_silent == 0 ]; then
		timeout_val_silent=1s
	    fi
	fi
    done
done

python3 build_table.py parallel-checklist minimal
