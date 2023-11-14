#!/bin/bash

this_script_location_arg=$1
start_location=$(pwd)

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi
use_haskell=1
to_gen=5000
if [[ $# -ge 2 ]]; then
    use_haskell=$2
fi
if [[ $# -ge 3 ]]; then
    to_gen=$3
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh


cd "${this_script_location}/scripts/build_scripts"
./exp_bigger_fish_expanded_create.sh 50 600 50
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_bigger_fish_expanded_run.sh 50 600 50
cd "${this_script_location}/scripts/process_results_scripts"
./exp_bigger_fish_expanded_table.sh 50 600 50


mkdir "${this_script_location}/examples/differential_testing/moved"

cd "${this_script_location}/scripts/build_scripts"
./differential_testing_create.sh "../../examples/differential_testing/array" $to_gen 2 5 $use_haskell 1
cd "${this_script_location}/scripts/comparison_scripts"
./differential_testing_run.sh "../../examples/differential_testing/array" $to_gen $use_haskell 1 0

mv "${this_script_location}/examples/differential_testing/array/gen_files" "${this_script_location}/examples/differential_testing/moved/array_go_gen_files"
mv "${this_script_location}/examples/differential_testing/array/results" "${this_script_location}/examples/differential_testing/moved/array_go_results"

# cd "${this_script_location}/scripts/build_scripts"
# ./differential_testing_create.sh "../../examples/differential_testing/array" 20 0 1000 1 1
# cd "${this_script_location}/scripts/comparison_scripts"
# ./differential_testing_run.sh "../../examples/differential_testing/array" 20 1 1 1

# mv "${this_script_location}/examples/differential_testing/array/gen_files" "${this_script_location}/examples/differential_testing/moved/array_msat_gen_files"
# mv "${this_script_location}/examples/differential_testing/array/results" "${this_script_location}/examples/differential_testing/moved/array_msat_results"


cd "${this_script_location}/scripts/build_scripts"
./exp_simple_robot_create.sh 2 50 4
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_simple_robot_run.sh 2 50 4
cd "${this_script_location}/scripts/process_results_scripts"
./exp_simple_robot_table.sh 2 50 4


cd "${this_script_location}/scripts/build_scripts"
./exp_blueROV_mod_create.sh
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_blueROV_mod_run.sh 
cd "${this_script_location}/scripts/process_results_scripts"
./exp_blueROV_mod_table.sh


cd "${this_script_location}/scripts/build_scripts"
./exp_light_controller_v3_create.sh
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_light_controller_v3_run.sh 
cd "${this_script_location}/scripts/process_results_scripts"
./exp_light_controller_v3_table.sh


cd $start_location
