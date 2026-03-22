#!/bin/bash

min_val=5
max_val=10
step_size=5

./make_folder_structure.sh ANSR_no_net

path_name="../../examples/ANSR_no_net"

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    cp "${path_name}/ANSR_no_net_${num}.tree" "${path_name}/tree/ANSR_no_net_${num}.tree"
    ./make_optimized_smv.sh "${path_name}" ANSR_no_net_$num
done
