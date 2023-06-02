#!/bin/bash

encodings=("aut_" "aut_s_" "depth_" "" "func_" "no_internal_" "s_var_")

for num in {1..50}; do
    echo $num
    ./run_all.sh ../examples/checklist checklist_parallel_$num "${encodings[@]}"
    ./run_all.sh ../examples/checklist checklist_sequence_$num "${encodings[@]}"
done
