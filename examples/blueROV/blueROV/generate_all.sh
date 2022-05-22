#!/bin/bash

#-------------------------------------------------------------------------------------------------------------------------------------------

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --output_file ../models_selector_mixed/blueROV_warnings_only_ltl_battery_only.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --output_file ../models_selector_parallel/blueROV_warnings_only_ltl_battery_only.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --output_file ../models_selector_non_parallel/blueROV_warnings_only_ltl_battery_only.smv --selector_mode 2 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_mixed/blueROV_full_ltl_battery_only.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_parallel/blueROV_full_ltl_battery_only.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_non_parallel/blueROV_full_ltl_battery_only.smv --selector_mode 2 --overwrite


python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_mixed/blueROV_full_small_ltl_battery_only.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_parallel/blueROV_full_small_ltl_battery_only.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_non_parallel/blueROV_full_small_ltl_battery_only.smv --selector_mode 2 --overwrite



python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --output_file ../models_sequence/blueROV_warnings_only_ltl_battery_only.smv --overwrite


python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_sequence/blueROV_full_ltl_battery_only.smv --overwrite

python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_sequence/blueROV_full_small_ltl_battery_only.smv --overwrite



python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --output_file ../models_path/blueROV_warnings_only_ltl_battery_only.smv --overwrite

python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_path/blueROV_full_ltl_battery_only.smv --overwrite

python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_path/blueROV_full_small_ltl_battery_only.smv --overwrite

#-------------------------------------------------------------------------------------------------------------------------------------------

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_full --output_file ../models_selector_mixed/blueROV_warnings_only_ltl_full.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_full --output_file ../models_selector_parallel/blueROV_warnings_only_ltl_full.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_full --output_file ../models_selector_non_parallel/blueROV_warnings_only_ltl_full.smv --selector_mode 2 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_mixed/blueROV_full_ltl_full.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_parallel/blueROV_full_ltl_full.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_non_parallel/blueROV_full_ltl_full.smv --selector_mode 2 --overwrite


python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_mixed/blueROV_full_small_ltl_full.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_parallel/blueROV_full_small_ltl_full.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_non_parallel/blueROV_full_small_ltl_full.smv --selector_mode 2 --overwrite



python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_full --output_file ../models_sequence/blueROV_warnings_only_ltl_full.smv --overwrite


python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_sequence/blueROV_full_ltl_full.smv --overwrite

python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_sequence/blueROV_full_small_ltl_full.smv --overwrite



python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/ltl_full --output_file ../models_path/blueROV_warnings_only_ltl_full.smv --overwrite

python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_path/blueROV_full_ltl_full.smv --overwrite

python3 behaverify_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/ltl_full --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_path/blueROV_full_small_ltl_full.smv --overwrite
