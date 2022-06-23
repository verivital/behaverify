#!/bin/bash


./generate_all.sh
mkdir -p ./results/gcd
mkdir -p ./results/basic
mkdir -p ./results/blueROV
mkdir -p ./results/auto_example
mkdir -p ./results/robot
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
