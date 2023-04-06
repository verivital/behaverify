#!/bin/bash

for num in {1..20}; do
    echo $num
    new_num=$((10*$num-1))
    ./run_all.sh ../examples/bigger_fish bigger_fish_parallel_$new_num
    ./run_all.sh ../examples/bigger_fish bigger_fish_sequence_$new_num
done
