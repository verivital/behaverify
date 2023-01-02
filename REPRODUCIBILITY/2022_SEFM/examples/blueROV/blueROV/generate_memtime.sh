#!/bin/bash


memtime ./mem_cmd.sh behaverify_total_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules_and_specs/total/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/total/battery > ../../results/blueROV/total_v2-warnings_only.txt

memtime ./mem_cmd2.sh behaverify_total_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/battery --blackboard_input_file ../modules_and_specs/total/blueROV_full.smv > ../../results/blueROV/total_v2-full.txt

memtime ./mem_cmd2.sh behaverify_total_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/battery --blackboard_input_file ../modules_and_specs/total/blueROV_small.smv > ../../results/blueROV/total_v2-small.txt


#-----------------------------------------

memtime ./mem_cmd.sh behaverify_total_v3.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules_and_specs/total/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/total/battery > ../../results/blueROV/total_v3-warnings_only.txt

memtime ./mem_cmd2.sh behaverify_total_v3.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/battery --blackboard_input_file ../modules_and_specs/total/blueROV_full.smv > ../../results/blueROV/total_v3-full.txt

memtime ./mem_cmd2.sh behaverify_total_v3.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/total/blueROV_status_check.smv --specs_input_file ../modules_and_specs/total/battery --blackboard_input_file ../modules_and_specs/total/blueROV_small.smv > ../../results/blueROV/total_v3-small.txt


#-----------------------------------------

memtime ./mem_cmd.sh behaverify_leaf_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --module_input_file ../modules_and_specs/leaf/blueROV_warnings_only.smv --specs_input_file ../modules_and_specs/leaf/battery > ../../results/blueROV/leaf_v2-warnings_only.txt

memtime ./mem_cmd2.sh behaverify_leaf_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/leaf/blueROV_status_check.smv --specs_input_file ../modules_and_specs/leaf/battery --blackboard_input_file ../modules_and_specs/leaf/blueROV_full.smv > ../../results/blueROV/leaf_v2-full.txt

memtime ./mem_cmd2.sh behaverify_leaf_v2.py BlueROV_tree_serene_edit create_root --force_parallel_unsynch --no_seperate_variable_modules --module_input_file ../modules_and_specs/leaf/blueROV_status_check.smv --specs_input_file ../modules_and_specs/leaf/battery --blackboard_input_file ../modules_and_specs/leaf/blueROV_small.smv > ../../results/blueROV/leaf_v2-small.txt


