#!/bin/bash

./make_folder_structure.sh checklist

python3 ../examples/checklist/create_checklist.py ../examples/checklist/

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for num in {1..50}; do
    echo "now on iteration: "
    echo $num
    new_num=$((10*$num-1))
    ./generate_encoding.sh ../examples/checklist checklist_parallel_$num "${encodings[@]}"
    ./generate_encoding.sh ../examples/checklist checklist_sequence_$num "${encodings[@]}"
    python3 ../examples/checklist/fix_checklist.py ../examples/checklist/ checklist_parallel_$num.smv
    python3 ../examples/checklist/fix_checklist.py ../examples/checklist/ checklist_sequence_$num.smv
done
