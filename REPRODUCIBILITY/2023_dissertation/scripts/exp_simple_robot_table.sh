#!/bin/bash

python3 ./build_table.py --folder_name simple_robot --file_name simple_robot --minV 2 --maxV 20 --step 1 --xLabel "Grid Size" --encodings "all" "internal" "core" "aut" "func"
