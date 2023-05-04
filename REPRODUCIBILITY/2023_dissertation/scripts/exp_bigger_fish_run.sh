#!/bin/bash

encodings=("aut_" "aut_s_" "depth_" "" "func_" "no_internal_" "s_var_")

for num in {1..20}; do
    echo $num
    new_num=$((10*$num-1))
    ./run_encoding.sh ../examples/bigger_fish bigger_fish_parallel_$new_num "${encodings[@]}"
    ./run_encoding.sh ../examples/bigger_fish bigger_fish_sequence_$new_num "${encodings[@]}"
done
