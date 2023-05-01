#!/bin/bash

for num in {1..50}; do
    echo $num
    new_num=$((10*$num-1))
    ./run_all.sh ../examples/checklist checklist_parallel_$num
    ./run_all.sh ../examples/checklist checklist_sequence_$num
done
