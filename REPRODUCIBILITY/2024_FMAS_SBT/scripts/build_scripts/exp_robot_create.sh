#!/bin/bash

python_command=python3
min_val=2
max_val=20
step_size=1

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh robot

path_name="../../examples/robot"

$python_command "${path_name}/make_tree.py" "${path_name}" "${path_name}/tree" $min_val $max_val $step_size
# $python_command "${path_name}/create_robot.py" "${path_name}/tree" $min_val $max_val $step_size
# $python_command "${path_name}/create_robot_MoVe4BT_xml.py" "${path_name}/xml" $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_optimized_smv.sh $python_command "${path_name}" robot_$num
done
