#!/bin/bash

#folders=("./models_selector_mixed" "./models_selector_parallel"  "./models_selector_non_parallel" "./models_sequence" "./models_path" "./models_double_path" "./models_double_path_clean" "./models_double_path_cleaner" "./models_double_path_ivar" "models_total")
folders=("./models_BTCompiler" "./models_double_path" "./models_double_path_clean" "./models_double_path_cleaner" "./models_double_path_ivar" "./models_total")
files=("serene_uc1")

for cur_folder in ${folders[@]}; do
    for sel_num in {0..10}; do
	for seq_num in {0..10}; do
	    echo $sel_num $seq_num $cur_folder
	    ./run_tests_2.sh $cur_folder sel$sel_num-seq$seq_num.smv
	done
    done
done

