#!/bin/bash

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for num in {2..20}; do
    echo $num
    ./run_encoding.sh ../examples/simple_robot simple_robot_$num "${encodings[@]}"
done
