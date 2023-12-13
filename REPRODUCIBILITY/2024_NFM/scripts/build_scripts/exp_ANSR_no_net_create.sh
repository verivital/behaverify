#!/bin/bash

min_val=5
max_val=10
step_size=5

./make_folder_structure.sh ANSR_no_net

path_name="../../examples/ANSR_no_net"
file_name="ANSR_no_net"

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    python3 ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/${file_name}_${num}.tree" "${path_name}/smv/full_opt_${file_name}_${num}.smv" --recursion_limit 5000
done
