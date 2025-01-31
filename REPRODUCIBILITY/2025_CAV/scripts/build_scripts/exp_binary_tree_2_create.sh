#!/bin/bash

python_command=python3
min_val=1
max_val=10
step_size=1

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh binary_tree_2

path_name="../../examples/binary_tree_2"

$python_command "${path_name}/create_binary_tree_2.py" "${path_name}/tree" parallel $min_val $max_val $step_size
$python_command "${path_name}/create_binary_tree_2.py" "${path_name}/tree" sequence $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_internal_smv.sh $python_command "${path_name}" binary_tree_2_parallel_$num 
    ./make_internal_smv.sh $python_command "${path_name}" binary_tree_2_sequence_$num
    
done
