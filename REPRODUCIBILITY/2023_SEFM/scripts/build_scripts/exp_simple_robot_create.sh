#!/bin/bash

min_val=2
max_val=20
step_size=1

if [ "$#" == 3 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

./make_folder_structure.sh simple_robot

path_name="../../examples/simple_robot"

python3 "${path_name}/make_tree.py" "${path_name}" "${path_name}/tree" $min_val $max_val $step_size

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for ((num=min_val; num<=max_val; num=(num + step_size))); do
    echo "now on iteration: "
    echo $num
    ./generate_encoding.sh "${path_name}" simple_robot_$num "${encodings[@]}"
done
