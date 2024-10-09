#!/bin/bash

python_command=python3
min_val=5
max_val=10
step_size=5

if [[ $# -ge 1 ]]; then
    python_command=$1
fi

./make_folder_structure.sh ISR

path_name="../../examples/ISR"

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    $python_command ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/ISR_${num}.tree" "${path_name}/smv/full_opt_ISR_${num}.smv" --recursion_limit 5000
done
