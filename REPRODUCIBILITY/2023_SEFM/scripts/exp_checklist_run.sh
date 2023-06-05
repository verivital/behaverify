#!/bin/bash

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for num in {1..50}; do
    echo $num
    ./run_encoding.sh ../examples/checklist checklist_parallel_$num "${encodings[@]}"
    ./run_encoding.sh ../examples/checklist checklist_sequence_$num "${encodings[@]}"
done
