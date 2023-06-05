#!/bin/bash

./make_folder_structure.sh bigger_fish

python3 ../examples/bigger_fish/create_bigger_fish.py ../examples/bigger_fish/

encodings=("aut" "aut_s" "depth" "norm" "func" "no_internal" "s_var")
#encodings=("norm" "norm")
echo $encodings

for num in {1..20}; do
    echo $num
    new_num=$((10*$num-1))
    ./generate_encoding.sh ../examples/bigger_fish bigger_fish_parallel_$new_num "${encodings[@]}"
    ./generate_encoding.sh ../examples/bigger_fish bigger_fish_sequence_$new_num "${encodings[@]}"
done
