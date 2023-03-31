#!/bin/bash

for num in {0..99}; do
    ./generate.sh ../examples/bigger_fish bigger_fish_parallel_$num
    ./generate.sh ../examples/bigger_fish bigger_fish_sequence_$num
done
