#!/bin/bash

this_script_location_arg=$1
no_haskell=$2
start_location=$(pwd)

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh


# cd "${this_script_location}/scripts/build_scripts"
# ./exp_3_node_no_var_create.sh
# cd "${this_script_location}/scripts/comparison_scripts"
# ./exp_3_node_no_var_run.sh


# cd "${this_script_location}/scripts/build_scripts"
# ./exp_bigger_fish_create.sh 9 200 10
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_bigger_fish_run.sh 9 200 10
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_bigger_fish_table.sh 9 200 10


cd "${this_script_location}/scripts/build_scripts"
./exp_bigger_fish_expanded_create.sh 50 600 50
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_bigger_fish_expanded_run.sh 50 600 50
cd "${this_script_location}/scripts/process_results_scripts"
./exp_bigger_fish_expanded_table.sh 50 600 50


# cd "${this_script_location}/scripts/build_scripts"
# ./exp_checklist_create.sh 1 50 1
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_checklist_run.sh 1 50 1
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_checklist_table.sh 1 50 1


# cd "${this_script_location}/scripts/build_scripts"
# ./exp_checklist_invar_create.sh 1 50 1
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_checklist_invar_run.sh 1 50 1
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_checklist_invar_table.sh 1 50 1


cd "${this_script_location}/scripts/build_scripts"
./exp_random_haskell_create.sh 20 2 5 $no_haskell
cd "${this_script_location}/scripts/comparison_scripts"
./exp_random_haskell_run.sh 20 $no_haskell


cd "${this_script_location}/scripts/build_scripts"
./exp_simple_robot_create.sh 2 3 4
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_simple_robot_run.sh 2 3 4
cd "${this_script_location}/scripts/process_results_scripts"
./exp_simple_robot_table.sh 2 3 4


# cd "${this_script_location}/scripts/build_scripts"
# ./exp_simplified_robot_create.sh 2 50 4
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_simplified_robot_run.sh 2 50 4
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_simplified_robot_table.sh 2 50 4


cd "${this_script_location}/scripts/build_scripts"
./exp_blueROV_mod_create.sh
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_blueROV_mod_run.sh 
cd "${this_script_location}/scripts/process_results_scripts"
./exp_blueROV_mod_table.sh


cd "${this_script_location}/scripts/build_scripts"
./exp_light_controller_create.sh
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_light_controller_run.sh 
cd "${this_script_location}/scripts/process_results_scripts"
./exp_light_controller_table.sh


cd $pwd
