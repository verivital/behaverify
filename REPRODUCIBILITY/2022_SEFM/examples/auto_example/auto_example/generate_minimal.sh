#!/bin/bash

versions=("BTCompiler" "leaf_v2" "total_v2" "total_v3")


for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for sel_num1 in {0..4}; do
	sel_num=$((5*$sel_num1))
	for seq_num in {0..20}; do
	    echo $sel_num $seq_num $cur_version
	    python3 behaverify_$cur_version.py auto_generate create_root --root_args False $sel_num $seq_num --output_file ../models_$cur_version/sel$sel_num-seq$seq_num.smv --overwrite
	done
    done
done

for cur_version in ${versions[@]}; do
    for seq_num1 in {0..4}; do
	seq_num=$((5*$seq_num1))
	for sel_num in {0..20}; do
	    echo $sel_num $seq_num $cur_version
	    python3 behaverify_$cur_version.py auto_generate create_root --root_args False $sel_num $seq_num --output_file ../models_$cur_version/sel$sel_num-seq$seq_num.smv --overwrite
	done
    done
done
