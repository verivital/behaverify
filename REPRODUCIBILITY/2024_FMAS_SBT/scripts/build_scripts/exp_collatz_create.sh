#!/bin/bash

python_command=python3
min_val=10
max_val=100
step_size=10

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh collatz

path_name="../../examples/collatz"

$python_command "${path_name}/create_collatz.py" "${path_name}/tree" $min_val $max_val $step_size
#$python_command "${path_name}/create_collatz.py" "${path_name}/tree" sequence $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_full_opt_smv.sh $python_command "${path_name}" collatz_$num 
    
done
