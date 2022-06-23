#!/bin/bash

versions=("BTCompiler" "leaf" "leaf_no_IVAR" "total" "total_no_IVAR_errorless_unique_child")

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for sel_num in {1..50}; do
	echo $sel_num $cur_version
	python3 behaverify_$cur_version.py robot create_root --root_args $sel_num --specs_input_file ../modules_and_specs/$cur_version/$sel_num.smv --output_file ../models_$cur_version/$sel_num.smv --overwrite
    done
done
