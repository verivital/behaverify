#!/bin/bash

files=("gcd_example")

versions=("leaf_v2" "total_v2" "total_v3")

#gen_mode=2
gen_mode=0

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for cur_file in ${files[@]}; do
	if [ $gen_mode -eq 0 ]; then
	   python3 behaverify_$cur_version.py $cur_file create_root --root_args False --min_val -1 --max_val 100 --no_seperate_variable_modules --blackboard_input_file ../modules_and_specs/$cur_version/$cur_file-blackboard.smv --module_input_file ../modules_and_specs/$cur_version/$cur_file.smv --specs_input_file ../modules_and_specs/$cur_version/$cur_file-specs.smv  --output_file ../models_$cur_version/$cur_file.smv --overwrite
	else
	   python3 behaverify_$cur_version.py $cur_file create_root --root_args False --min_val -1 --max_val 100 --no_seperate_variable_modules --gen_modules $gen_mode --output_file ../models_$cur_version/$cur_file.smv --module_output_file ../modules_and_specs/$cur_version/$cur_file-gen-$gen_mode.smv --blackboard_output_file ../modules_and_specs/$cur_version/$cur_file-blackboard-gen-$gen_mode.smv --overwrite
	fi
    done
done

