#!/bin/bash

files=("example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")
#files=("example1")


for cur_file in ${files[@]}; do
    python3 behaverify_double_path.py $cur_file create_root --output_file ../models_double_path/$cur_file.smv --overwrite
done

