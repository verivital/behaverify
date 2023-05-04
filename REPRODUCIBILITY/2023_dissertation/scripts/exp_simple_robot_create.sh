#!/bin/bash

python3 ../examples/simple_robot/make_tree.py ../examples/simple_robot/

encodings=("aut_" "" "func_" "no_internal_" "s_var_")

for num in {2..20}; do
    ./generate_encoding.sh ../examples/simple_robot simple_robot_$num "${encodings[@]}"
done
