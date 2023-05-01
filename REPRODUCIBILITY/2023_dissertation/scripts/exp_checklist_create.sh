#!/bin/bash

for num in {1..50}; do
    echo "now on iteration: "
    echo $num
    new_num=$((10*$num-1))
    ./generate.sh ../examples/checklist checklist_parallel_$num
    ./generate.sh ../examples/checklist checklist_sequence_$num
    python3 ../examples/checklist/fix_checklist.py ../examples/checklist/ checklist_parallel_$num.smv
    python3 ../examples/checklist/fix_checklist.py ../examples/checklist/ checklist_sequence_$num.smv
done
