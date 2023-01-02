#!/bin/bash

folders=("models_leaf_v1" "models_leaf_v2" "models_total_v1" "models_total_v2" "models_total_v3")
files=("gcd_example")


for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	echo $cur_folder $cur_file
	timeout 15m ./run_tests.sh gcd $cur_folder $cur_file
    done
done

