#!/bin/bash

#folders=("models_BTCompiler" "models_leaf" "models_total")
folders=("models_BTCompiler" "models_leaf" "models_total" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child")
files=("example0" "example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	echo $cur_folder $cur_file
	timeout 5m ./run_tests.sh basic $cur_folder $cur_file
	if [ $? == 0 ]; then
	    break
	fi
    done
done
