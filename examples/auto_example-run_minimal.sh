#!/bin/bash

folders=("models_BTCompiler" "models_leaf_v2" "models_total_v2" "models_total_v3")

for cur_folder in ${folders[@]}; do
    for sel_num1 in {0..4}; do
	sel_num=$((5*$sel_num1))
	for seq_num in {0..20}; do
	    echo $sel_num $seq_num $cur_folder
	    timeout 3m ./run_tests.sh auto_example $cur_folder sel$sel_num-seq$seq_num
	done
    done
done

for cur_folder in ${folders[@]}; do
    for seq_num1 in {0..4}; do
	seq_num=$((5*$seq_num1))
	for sel_num in {0..20}; do
	    echo $sel_num $seq_num $cur_folder
	    timeout 3m ./run_tests.sh auto_example $cur_folder sel$sel_num-seq$seq_num
	done
    done
done
