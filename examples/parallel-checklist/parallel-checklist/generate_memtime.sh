#!/bin/bash

versions=("BTCompiler" "leaf_v2" "total_v2" "total_v3")

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for sel_num in {1..50}; do
	echo $sel_num $cur_version
	memtime ./mem_cmd.sh behaverify_$cur_version.py checklist create_root --root_args $sel_num --specs_input_file ../modules_and_specs/$cur_version/$sel_num.smv > ../../results/parallel-checklist/$cur_version-$sel_num.txt
    done
done
