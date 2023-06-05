#!/bin/bash

./make_folder_structure.sh checklist_invar

python3 ../examples/checklist_invar/create_checklist.py ../examples/checklist_invar/

encodings=("aut" "norm" "func" "no_internal" "s_var")

for num in {1..50}; do
    echo "now on iteration: "
    echo $num
    new_num=$((10*$num-1))
    ./generate_encoding.sh ../examples/checklist_invar checklist_parallel_$num "${encodings[@]}"
    ./generate_encoding.sh ../examples/checklist_invar checklist_sequence_$num "${encodings[@]}"
    python3 ../examples/checklist_invar/fix_checklist.py ../examples/checklist_invar/ checklist_parallel_$num.smv
    python3 ../examples/checklist_invar/fix_checklist.py ../examples/checklist_invar/ checklist_sequence_$num.smv
done
