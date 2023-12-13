#!/bin/bash

this_script_location_arg=$1
start_location=$(pwd)

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh


cd "${this_script_location}/scripts/build_scripts"
./exp_bigger_fish_selector_create.sh 50 500 50
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_bigger_fish_selector_run.sh 50 500 50
cd "${this_script_location}/scripts/process_results_scripts"
./exp_bigger_fish_selector_table.sh 50 500 50


cd "${this_script_location}/scripts/build_scripts"
./exp_simple_robot_create.sh 2 22 4
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_simple_robot_run.sh 2 22 4
cd "${this_script_location}/scripts/process_results_scripts"
./exp_simple_robot_table.sh 2 22 4


cd $start_location
