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

collatz_min=10
collatz_max=100
collatz_step=10

cd "${this_script_location}/scripts/build_scripts"
./exp_collatz_create.sh $python_behaverify $collatz_min $collatz_max $collatz_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_collatz_run.sh $collatz_min $collatz_max $collatz_step
cd "${this_script_location}/scripts/process_results_scripts"
./exp_collatz_table.sh $python_results $collatz_min $collatz_max $collatz_step

# binary_tree_min=1
# binary_tree_max=10
# binary_tree_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_binary_tree_create.sh $python_behaverify $binary_tree_min $binary_tree_max $binary_tree_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_binary_tree_run.sh $binary_tree_min $binary_tree_max $binary_tree_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_table.sh $python_results $binary_tree_min $binary_tree_max $binary_tree_step

# binary_tree_1_min=1
# binary_tree_1_max=11
# binary_tree_1_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_binary_tree_1_create.sh $python_behaverify $binary_tree_1_min $binary_tree_1_max $binary_tree_1_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_binary_tree_1_run.sh $binary_tree_1_min $binary_tree_1_max $binary_tree_1_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_1_table.sh $python_results $binary_tree_1_min $binary_tree_1_max $binary_tree_1_step

# binary_tree_2_min=1
# binary_tree_2_max=8
# binary_tree_2_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_binary_tree_2_create.sh $python_behaverify $binary_tree_2_min $binary_tree_2_max $binary_tree_2_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_binary_tree_2_run.sh $binary_tree_2_min $binary_tree_2_max $binary_tree_2_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_2_table.sh $python_results $binary_tree_2_min $binary_tree_2_max $binary_tree_2_step

# robot_min=2
# robot_max=20
# robot_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_robot_create.sh $python_behaverify $robot_min $robot_max $robot_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_robot_run.sh $robot_min $robot_max $robot_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_robot_table.sh $python_results $robot_min $robot_max $robot_step


# simple_robot_min=2
# simple_robot_max=20
# simple_robot_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_simple_robot_create.sh $python_behaverify $simple_robot_min $simple_robot_max $simple_robot_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_simple_robot_run.sh $simple_robot_min $simple_robot_max $simple_robot_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_simple_robot_table.sh $python_results $simple_robot_min $simple_robot_max $simple_robot_step


# simple_robot_2_min=2
# simple_robot_2_max=20
# simple_robot_2_step=1

# cd "${this_script_location}/scripts/build_scripts"
# ./exp_simple_robot_2_create.sh $python_behaverify $simple_robot_2_min $simple_robot_2_max $simple_robot_2_step
# cd "${this_script_location}/scripts/encoding_timing_scripts"
# ./exp_simple_robot_2_run.sh $simple_robot_2_min $simple_robot_2_max $simple_robot_2_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_simple_robot_2_table.sh $python_results $simple_robot_2_min $simple_robot_2_max $simple_robot_2_step

cd $start_location
