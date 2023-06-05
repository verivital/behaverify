#!/bin/bash

encodings=("aut" "norm" "func" "no_internal" "s_var")

for num in {1..50}; do
    echo $num
    ./run_encoding.sh ../examples/checklist_invar checklist_parallel_$num "${encodings[@]}"
    ./run_encoding.sh ../examples/checklist_invar checklist_sequence_$num "${encodings[@]}"
done
