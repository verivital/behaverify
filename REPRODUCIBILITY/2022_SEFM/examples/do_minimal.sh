#!/bin/bash


./generate_minimal.sh
mkdir -p ./results/blueROV
mkdir -p ./results/checklist
mkdir -p ./results/parallel-checklist
mkdir -p ./processed_data/blueROV
mkdir -p ./processed_data/checklist
mkdir -p ./processed_data/parallel-checklist
./run_minimal.sh
python3 build_table.py blueROV True
python3 build_table.py checklist True
python3 build_table.py parallel-checklist True
