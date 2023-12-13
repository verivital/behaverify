#!/bin/bash



min_val=50
max_val=1000
step_size=50

if [[ $# -ge 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

./make_folder_structure.sh bigger_fish_selector

path_name="../../examples/bigger_fish_selector"

python3 "${path_name}/create_bigger_fish.py" "${path_name}/tree" selector $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_optimized_smv.sh "${path_name}" bigger_fish_selector_$num
done
