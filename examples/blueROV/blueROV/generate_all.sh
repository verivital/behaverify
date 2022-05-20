#!/bin/bash



python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_mixed/blueROV_warnings_only.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_parallel/blueROV_warnings_only.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_non_parallel/blueROV_warnings_only.smv --selector_mode 2 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_mixed2/blueROV_warnings_only.smv --selector_mode 0 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_parallel2/blueROV_warnings_only.smv --selector_mode 1 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_selector_non_parallel2/blueROV_warnings_only.smv --selector_mode 2 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_mixed/blueROV_full.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_parallel/blueROV_full.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_non_parallel/blueROV_full.smv --selector_mode 2 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_mixed2/blueROV_full.smv --selector_mode 0 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_parallel2/blueROV_full.smv --selector_mode 1 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_selector_non_parallel2/blueROV_full.smv --selector_mode 2 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_mixed/blueROV_full_small.smv --selector_mode 0 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_parallel/blueROV_full_small.smv --selector_mode 1 --overwrite

python3 behaverify_selector.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_non_parallel/blueROV_full_small.smv --selector_mode 2 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_mixed2/blueROV_full_small.smv --selector_mode 0 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_parallel2/blueROV_full_small.smv --selector_mode 1 --overwrite

python3 behaverify_selector2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_selector_non_parallel2/blueROV_full_small.smv --selector_mode 2 --overwrite


python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_sequence/blueROV_warnings_only.smv --overwrite

python3 behaverify_sequence2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_sequence2/blueROV_warnings_only.smv --overwrite


python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_sequence/blueROV_full.smv --overwrite

python3 behaverify_sequence2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_sequence2/blueROV_full.smv --overwrite

python3 behaverify_sequence.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_sequence/blueROV_full_small.smv --overwrite

python3 behaverify_sequence2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_sequence2/blueROV_full_small.smv --overwrite



python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules\ and\ specs/blueROV_warnings_only.smv --specs_input_file ../modules\ and\ specs/demo_spec --output_file ../models_ultimate/blueROV_warnings_only.smv --overwrite

python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full.smv --output_file ../models_ultimate/blueROV_full.smv --overwrite

python3 behaverify_ultimate.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules\ and\ specs/blueROV_status_check.smv --specs_input_file ../modules\ and\ specs/demo_spec --blackboard_input_file ../modules\ and\ specs/blueROV_full_small.smv --output_file ../models_ultimate/blueROV_full_small.smv --overwrite
