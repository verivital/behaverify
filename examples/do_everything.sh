#!/bin/bash


./generate_all.sh
mkdir -p ./results/gcd/processed_data
mkdir -p ./results/basic/processed_data
mkdir -p ./results/blueROV/processed_data
mkdir -p ./results/auto_example/processed_data
mkdir -p ./results/robot/processed_data
mkdir -p ./processed_data/gcd
mkdir -p ./processed_data/basic
mkdir -p ./processed_data/blueROV
mkdir -p ./processed_data/auto_example
mkdir -p ./processed_data/robot
./run_all.sh
python3 build_table.py gcd
python3 build_table.py basic
python3 build_table.py blueROV
python3 build_table.py auto_example
python3 build_table.py robot
