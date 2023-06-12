#!/bin/bash

min_val=1
max_val=50
step_size=1

if [ "$#" == 3 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

./make_folder_structure.sh checklist

path_name="../../examples/checklist"

python3 "${path_name}/create_checklist.py" "${path_name}/tree" $min_val $max_val $step_size

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for ((num=min_val; num<=max_val; num=(num + step_size))); do
    echo "now on iteration: "
    echo $num
    ./generate_encoding.sh "${path_name}" checklist_parallel_$num "${encodings[@]}"
    ./generate_encoding.sh "${path_name}" checklist_sequence_$num "${encodings[@]}"
    python3 "${path_name}/fix_checklist.py" "${path_name}/" checklist_parallel_$num.smv
    python3 "${path_name}/fix_checklist.py" "${path_name}/" checklist_sequence_$num.smv
done
