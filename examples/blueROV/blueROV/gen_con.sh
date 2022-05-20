#!/bin/bash


python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_ultimate/blueROV_warnings_only.smv --overwrite

python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_ultimate/blueROV_full.smv --overwrite

python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_ultimate/blueROV_full_small.smv --overwrite
