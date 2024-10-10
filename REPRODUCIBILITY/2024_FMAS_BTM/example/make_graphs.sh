#!/bin/bash


python_results=python3

if [[ $# -ge 1 ]]; then
    python_results=$1
fi

if [ -f "./images" ]; then
    rm -rf "./images"
fi
mkdir "./images"

$python_results graph_sizes.py ./dense_fixed/collision_behaverify_sizes.txt ./dense_fixed/collision_copilot_sizes.txt ./images/file_sizes_dense_fixed
$python_results graph_sizes.py ./sparse_random/collision_behaverify_sizes.txt ./sparse_random/collision_copilot_sizes.txt ./images/file_sizes_sparse_random

$python_results graph_timing.py ./dense_fixed/timing_behaverify.txt ./dense_fixed/timing_copilot.txt ./dense_fixed/timing_monitorless.txt ./images/timing_dense_fixed
$python_results graph_timing.py ./sparse_random/timing_behaverify.txt ./sparse_random/timing_copilot.txt ./sparse_random/timing_monitorless.txt ./images/timing_sparse_random

$python_results graph_timing_design_time.py ./dense_fixed/timing_design_time.txt ./sparse_random/timing_design_time.txt ./images/timing_design_time

