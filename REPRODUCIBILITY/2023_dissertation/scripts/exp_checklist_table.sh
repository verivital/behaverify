#!/bin/bash

python3 ./build_table.py --folder_name bigger_fish --file_name bigger_fish_parallel bigger_fish_sequence --minV 9 --maxV 199 --step 10 --xLabel "Biggest Fish Check" --encodings "all" "internal" "core" "aut" "func"
