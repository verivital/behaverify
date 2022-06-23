#!/bin/bash

folders=("models_BTCompiler" "models_leaf" "models_total" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child")
files=("serene_uc1")

for cur_folder in ${folders[@]}; do
    for sel_num in {0..20}; do
	for seq_num in {0..20}; do
	    echo $sel_num $seq_num $cur_folder
	    timeout 3m ./run_tests.sh auto_example $cur_folder sel$sel_num-seq$seq_num
	done
    done
done
