#!/bin/bash

versions=("BTCompiler" "leaf_v1" "leaf_v2" "total_v1" "total_v2" "total_v3")

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for sel_num in {1..50}; do
	echo $sel_num $cur_version
	python3 behaverify_$cur_version.py checklist create_root --root_args $sel_num --specs_input_file ../modules_and_specs/$cur_version/$sel_num.smv --output_file ../models_$cur_version/$sel_num.smv --overwrite
    done
done
