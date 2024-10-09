#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

this_script_location_arg=$1

iterations=2

if [[ $# -ge 2 ]]; then
    iterations=$2
fi

python_behaverify=python3
python_results=python3

if [[ $# -ge 4 ]]; then
    python_behaverify=$3
    python_results=$4
fi

echo "using ${python_behaverify} for behaverify"
echo "using ${python_results} for results"

start_location=$(pwd)

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/example"
./prepare.sh
./pipeline_create_dense_fixed.sh $iterations
./pipeline_create_sparse_random.sh $iterations
./pipeline_create_design_time.sh
./pipeline_existing_behaverify_c.sh $python_behaverify $python_results
./pipeline_existing_monitorless.sh
./pipeline_existing_copilot.sh $python_behaverify $python_results
./pipeline_existing_design_time.sh $python_behaverify $python_results
./compare_timing_v4_setup.sh
./compare_timing_v4.sh
./collect_timing_design_time.sh
./read_sizes_v4.sh
./make_graphs.sh $python_results


cd $start_location
