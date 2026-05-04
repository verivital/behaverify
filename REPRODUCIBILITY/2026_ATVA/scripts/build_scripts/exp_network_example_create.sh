#!/bin/bash

python_command=python3
min_val=0
max_val=1
step_size=1

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh NetworkExample

path_name="../../examples/NetworkExample"
cp "${path_name}/using1000.tree" "${path_name}/tree/network_0.tree" 
cp "${path_name}/using9995.tree" "${path_name}/tree/network_1.tree" 
cp -r "${path_name}/networks" "${path_name}/tree/networks"
for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_full_opt_smv.sh $python_command "${path_name}" network_$num
done 
