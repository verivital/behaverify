#!/bin/bash


mkdir -p ./results/blueROV
mkdir -p ./results/checklist
mkdir -p ./results/parallel-checklist
mkdir -p ./processed_data/blueROV
mkdir -p ./processed_data/checklist
mkdir -p ./processed_data/parallel-checklist
./generate_memtime.sh
python3 memtime_table.py blueROV True
python3 memtime_table.py checklist True
python3 memtime_table.py parallel-checklist True
