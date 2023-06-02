#!/bin/bash

encodings=("aut_" "" "func_" "no_internal_" "s_var_")

for num in {1..50}; do
    echo $num
    ./run_encoding.sh ../examples/checklist_invar checklist_parallel_$num "${encodings[@]}"
    ./run_encoding.sh ../examples/checklist_invar checklist_sequence_$num "${encodings[@]}"
done
