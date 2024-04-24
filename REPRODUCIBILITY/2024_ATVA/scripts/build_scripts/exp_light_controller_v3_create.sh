#!/bin/bash

min_val=1
max_val=1
step_size=1

# if [ "$#" == 3 ]; then
#     min_val=$1
#     max_val=$2
#     step_size=$3
# fi

./make_folder_structure.sh light_controller_v3

path_name="../../examples/light_controller_v3"

cp "${path_name}/light_controller.tree" "${path_name}/tree/light_controller_1.tree"

# python3 "${path_name}/make_tree.py" "${path_name}" "${path_name}/tree" $min_val $max_val $step_size

encodings=("norm")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    # ./generate_encoding.sh "${path_name}" light_controller_$num "${encodings[@]}"
    ./make_optimized_smv.sh "${path_name}" light_controller_$num
done
