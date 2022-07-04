#!/bin/bash

files=("BlueROV_tree_serene_edit")
versions=("total_v3")

constant_arg="--force_parallel_unsynch --overwrite"
ltl_versions=("battery" "emergency" "home_reached" "obstacle" "sensor")

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for ltl in ${ltl_versions[@]}; do
	for cur_file in ${files[@]}; do
	    arguments=()
	    if [[ $cur_version == *"total"* ]]; then
		arguments=("--module_input_file ../modules_and_specs/total/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/total/$ltl --output_file ../models_$cur_version/blueROV_warnings_only_$ltl.smv" "--no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/$ltl --blackboard_input_file ../modules_and_specs/total/blueROV_full.smv --output_file ../models_$cur_version/blueROV_full_$ltl.smv" "--no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/$ltl --blackboard_input_file ../modules_and_specs/total/blueROV_small.smv --output_file ../models_$cur_version/blueROV_small_$ltl.smv")
	    else
		arguments=("--module_input_file ../modules_and_specs/leaf/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/leaf/$ltl --output_file ../models_$cur_version/blueROV_warnings_only_$ltl.smv" "--no_seperate_variable_modules --module_input_file ../modules_and_specs/leaf/blueROV_status_check.smv --specs_input_file ../modules_and_specs/leaf/$ltl --blackboard_input_file ../modules_and_specs/leaf/blueROV_full.smv --output_file ../models_$cur_version/blueROV_full_$ltl.smv" "--no_seperate_variable_modules --module_input_file ../modules_and_specs/leaf/blueROV_status_check.smv --specs_input_file ../modules_and_specs/leaf/$ltl --blackboard_input_file ../modules_and_specs/leaf/blueROV_small.smv --output_file ../models_$cur_version/blueROV_small_$ltl.smv")
	    fi
	    for arg in "${arguments[@]}"; do
		echo python3 behaverify_$cur_version.py $cur_file create_root $constant_arg $arg
		python3 behaverify_$cur_version.py $cur_file create_root $constant_arg $arg
	    done
	done
    done
done
