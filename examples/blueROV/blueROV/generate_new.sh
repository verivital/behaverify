#!/bin/bash

files=("BlueROV_tree_serene_edit")
#versions=("total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar")
versions=("total")
#versions=("selector_mixed" "selector_parallel" "selector_non_parallel" "sequence" "path" "total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar")


for cur_file in ${files[@]}; do
    for cur_version in ${versions[@]}; do
	arguments=()
	if [[ $cur_version == "total" ]]; then
	    arguments=("--force_parallel_unsynch --module_input_file ../modules_and_specs/total/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/total/ltl_battery_only --output_file ../models_total/blueROV_warnings_only_ltl_battery_only.smv --overwrite" "--force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/ltl_battery_only --blackboard_input_file ../modules_and_specs/total/blueROV_full.smv --output_file ../models_total/blueROV_full_ltl_battery_only.smv --overwrite" "--force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/ltl_battery_only --blackboard_input_file ../modules_and_specs/total/blueROV_full_small.smv --output_file ../models_total/blueROV_full_small_ltl_battery_only.smv --overwrite")
	else
	    arguments=("--force_parallel_unsynch --module_input_file ../modules_and_specs/double/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/double/ltl_battery_only --output_file ../models_$cur_version/blueROV_warnings_only_ltl_battery_only.smv --overwrite" "--force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/double/blueROV_status_check.smv --specs_input_file ../modules_and_specs/double/ltl_battery_only --blackboard_input_file ../modules_and_specs/double/blueROV_full.smv --output_file ../models_$cur_version/blueROV_full_ltl_battery_only.smv --overwrite" "--force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/double/blueROV_status_check.smv --specs_input_file ../modules_and_specs/double/ltl_battery_only --blackboard_input_file ../modules_and_specs/double/blueROV_full_small.smv --output_file ../models_$cur_version/blueROV_full_small_ltl_battery_only.smv --overwrite")
	fi
	for arg in "${arguments[@]}"; do
	    echo python3 behaverify_$cur_version.py $cur_file create_root $arg
	    python3 behaverify_$cur_version.py $cur_file create_root $arg
	done
    done
done
