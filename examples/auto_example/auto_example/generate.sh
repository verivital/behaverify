#!/bin/bash

versions=("total" "leaf" "BTCompiler" "leaf_no_IVAR" "total_no_IVAR_errorless_unique_child")


for sel_num in {0..20}; do
    for seq_num in {0..20}; do
	for cur_version in ${versions[@]}; do
	    echo $sel_num $seq_num $cur_version
	    python3 behaverify_$cur_version.py auto_generate create_root --root_args False $sel_num $seq_num --output_file ../models_$cur_version/sel$sel_num-seq$seq_num.smv --overwrite
	done
    done
done
