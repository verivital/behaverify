#!/bin/bash

folders=("models_BTCompiler" "models_leaf_v1" "models_leaf_v2" "models_total_v1" "models_total_v2" "models_total_v3")
files=("example0" "example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	echo $cur_folder $cur_file
	timeout 2m ./run_tests.sh basic $cur_folder $cur_file
    done
done
