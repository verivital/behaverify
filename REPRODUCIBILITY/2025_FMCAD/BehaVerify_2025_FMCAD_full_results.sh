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

cd "${this_script_location}/examples"
# ./clean_all.sh

binary_tree_min=1
binary_tree_max=10
binary_tree_step=1

cd "${this_script_location}/scripts/build_scripts"
./exp_tool_comparisons_2025_FMCAD_create.sh $python_behaverify $binary_tree_min $binary_tree_max $binary_tree_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_tool_comparisons_2025_FMCAD_run.sh $binary_tree_min $binary_tree_max $binary_tree_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_table.sh $python_results $binary_tree_min $binary_tree_max $binary_tree_step

network_min=0
network_max=1
network_step=1
cd "${this_script_location}/scripts/build_scripts"
./exp_network_example_create.sh $python_behaverify $network_min $network_max $network_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_network_example_run.sh $network_min $network_max $network_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_table.sh $python_results $binary_tree_min $binary_tree_max $binary_tree_step

cd $start_location
