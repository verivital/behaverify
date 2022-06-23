#!/bin/bash

folders=("models_leaf" "models_total" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child")
files=("gcd_example")


for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	echo $cur_folder $cur_file
	timeout 1h ./run_tests.sh gcd $cur_folder $cur_file
    done
done

