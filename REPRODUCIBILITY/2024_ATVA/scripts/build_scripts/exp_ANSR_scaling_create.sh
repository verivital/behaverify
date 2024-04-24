#!/bin/bash



min_val=2
max_val=9
step_size=1

if [[ $# -ge 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

./make_folder_structure.sh ANSR_scaling

path_name="../../examples/ANSR_scaling"

python3 "${path_name}/generate_fake_tree.py" "${path_name}/template.tree" "${path_name}/tree" $min_val $max_val $step_size

#encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    #./generate_encoding.sh "${path_name}" bigger_fish_parallel_$num "${encodings[@]}"
    #./generate_encoding.sh "${path_name}" bigger_fish_sequence_$num "${encodings[@]}"
    ./make_optimized_smv.sh "${path_name}" "ANSR_scaling_flat_${num}"
    ./make_optimized_smv.sh "${path_name}" "ANSR_scaling_square_${num}"
done
