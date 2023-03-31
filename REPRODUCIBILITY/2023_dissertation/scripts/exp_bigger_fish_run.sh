#!/bin/bash

for num in {0..99}; do
    echo $num
    ./run_all.sh ../examples/bigger_fish bigger_fish_parallel_$num
    ./run_all.sh ../examples/bigger_fish bigger_fish_sequence_$num
done
