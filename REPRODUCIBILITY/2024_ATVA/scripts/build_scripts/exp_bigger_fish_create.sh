#!/bin/bash

python_command=python3
min_val=50
max_val=1000
step_size=50

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh bigger_fish

path_name="../../examples/bigger_fish"

$python_command "${path_name}/create_bigger_fish.py" "${path_name}/tree" MoVe4BT $min_val $max_val $step_size
$python_command "${path_name}/create_bigger_fish_MoVe4BT_xml.py" "${path_name}/xml" $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_full_opt_smv.sh $python_command "${path_name}" bigger_fish_MoVe4BT_$num
done
