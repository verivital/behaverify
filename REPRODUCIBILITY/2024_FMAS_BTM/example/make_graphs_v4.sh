#!/bin/bash


python_results=python3

if [[ $# -ge 1 ]]; then
    python_results=$1
fi

$python_results graph_sizes.py ./dense_fixed/collision_v4_behaverify_sizes.txt ./dense_fixed/collision_v4_copilot_sizes.txt ./collision_v4_sizes_dense_fixed
$python_results graph_sizes.py ./sparse_random/collision_behaverify_sizes.txt ./sparse_random/collision_copilot_sizes.txt ./collision_sizes_sparse_random

$python_results graph_timing.py ./dense_fixed/timing_v4_behaverify.txt ./dense_fixed/timing_v4_copilot.txt ./dense_fixed/timing_v4_monitorless.txt ./dense_fixed/timing_v4_nurv.txt ./timing_v4_dense_fixed
$python_results graph_timing.py ./sparse_random/timing_v4_behaverify.txt ./sparse_random/timing_v4_copilot.txt ./sparse_random/timing_v4_monitorless.txt ./sparse_random/timing_v4_nurv.txt ./timing_v4_sparse_random

$python_results graph_timing_v4_design_time.py ./dense_fixed/timing_v4_design_time.txt ./sparse_random/timing_v4_design_time.txt ./timing_v4_design_time

