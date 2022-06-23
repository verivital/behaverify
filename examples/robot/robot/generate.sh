#!/bin/bash

versions=("total" "total_errorless" "leaf" "BTCompiler" "leaf_no_IVAR" "total_no_IVAR" "total_no_IVAR_errorless" "total_no_IVAR_errorless_unique_child")
#versions=("total_no_IVAR_errorless_unique_child")

for sel_num in {1..50}; do
    for cur_version in ${versions[@]}; do
	echo $sel_num $cur_version
	python3 behaverify_$cur_version.py robot create_root --root_args $sel_num --specs_input_file ../modules_and_specs/$cur_version/$sel_num.smv --output_file ../models_$cur_version/$sel_num.smv --overwrite
    done
done
