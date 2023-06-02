#!/bin/bash

python3 ./build_table.py --folder_name checklist_invar --file_name checklist_parallel checklist_sequence --minV 1 --maxV 50 --step 1 --xLabel "Number of Checks" --encodings "invar" "internal" "func"
