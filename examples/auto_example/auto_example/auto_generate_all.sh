#!/bin/bash

selector=
#versions=("total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar" "BTCompiler")
versions=("total" "double_path_ivar" "BTCompiler")
#versions=("selector_mixed" "selector_parallel" "selector_non_parallel" "sequence" "path" "total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar")


for sel_num in {0..20}; do
    for seq_num in {0..20}; do
	for cur_version in ${versions[@]}; do
	    echo $sel_num $seq_num $cur_version
	    python3 behaverify_$cur_version.py auto_generate create_root --root_args False $sel_num $seq_num --output_file ../models_$cur_version/sel$sel_num-seq$seq_num.smv --overwrite
	done
    done
done
