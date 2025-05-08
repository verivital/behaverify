#!/bin/bash

this_script_location_arg=$1
start_location=$(pwd)

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)


cd "${this_script_location}/../build_scripts"
./exp_ANSR_scaling_grid_create.sh 6 20 2
cd "${this_script_location}/../encoding_timing_scripts"
./exp_ANSR_scaling_grid_run.sh 6 20 2
cd "${this_script_location}/../process_results_scripts"
./exp_ANSR_scaling_grid_table.sh 6 20 2


cd $start_location
