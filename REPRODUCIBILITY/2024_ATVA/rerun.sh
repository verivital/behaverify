#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

this_script_location_arg=$1
python_behaverify=python3
python_results=python3
start_location=$(pwd)

if [[ $# -ge 3 ]]; then
    python_behaverify=$2
    python_results=$3
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/scripts/build_scripts"
./exp_bigger_fish_create.sh $python_behaverify 50 1000 50
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_bigger_fish_run.sh 50 1000 50
cd "${this_script_location}/scripts/process_results_scripts"
./exp_bigger_fish_table.sh $python_results 50 1000 50

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_simple_robot_create.sh $python_behaverify 2 30 4
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_simple_robot_run.sh 2 30 4
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_simple_robot_table.sh $python_results 2 30 4

cd $start_location
