#!/bin/bash

python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/double/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/double/ltl_full --output_file ../models_double_path/blueROV_warnings_only_ltl_full.smv --overwrite

python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/double/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/double/ltl_full --blackboard_input_file ../modules\ and\ specs/double/blueROV_full.smv --output_file ../models_double_path/blueROV_full_ltl_full.smv --overwrite

python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/double/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/double/ltl_full --blackboard_input_file ../modules\ and\ specs/double/blueROV_full_small.smv --output_file ../models_double_path/blueROV_full_small_ltl_full.smv --overwrite



python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/double/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/double/ltl_battery_only --output_file ../models_double_path/blueROV_warnings_only_ltl_battery_only.smv --overwrite

python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/double/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/double/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/double/blueROV_full.smv --output_file ../models_double_path/blueROV_full_ltl_battery_only.smv --overwrite

python3 behaverify_double_path.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/double/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/double/ltl_battery_only --blackboard_input_file ../modules\ and\ specs/double/blueROV_full_small.smv --output_file ../models_double_path/blueROV_full_small_ltl_battery_only.smv --overwrite
