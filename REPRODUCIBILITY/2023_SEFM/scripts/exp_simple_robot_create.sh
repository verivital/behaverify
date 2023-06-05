#!/bin/bash

./make_folder_structure.sh simple_robot

python3 ../examples/simple_robot/make_tree.py ../examples/simple_robot/

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")

for num in {2..20}; do
    echo $num
    ./generate_encoding.sh ../examples/simple_robot simple_robot_$num "${encodings[@]}"
done
