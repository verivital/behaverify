#!/bin/bash

encodings=("aut_" "aut_s_" "depth_" "" "func_" "no_internal_" "s_var_")

for num in {2..20}; do
    echo $num
    ./run_all.sh ../examples/simple_robot simple_robot_$num "${encodings[@]}"
done
