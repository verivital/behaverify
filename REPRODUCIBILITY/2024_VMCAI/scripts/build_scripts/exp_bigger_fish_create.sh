#!/bin/bash



min_val=9
max_val=200
step_size=10

if [ "$#" == 3 ]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

./make_folder_structure.sh bigger_fish

path_name="../../examples/bigger_fish"

python3 "${path_name}/create_bigger_fish.py" "${path_name}/tree" $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for ((num=min_val; num<=max_val; num=(num + step_size))); do
    echo "now on iteration: "
    echo $num
    #./generate_encoding.sh "${path_name}" bigger_fish_parallel_$num "${encodings[@]}"
    #./generate_encoding.sh "${path_name}" bigger_fish_sequence_$num "${encodings[@]}"
    ./make_optimized_smv.sh "${path_name}" bigger_fish_parallel_$num
    ./make_optimized_smv.sh "${path_name}" bigger_fish_sequence_$num
done
