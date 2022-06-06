#!/bin/bash

files=("serene_uc1")
#files=("example1")

versions=("double_path_clean" "double_path_cleaner")


for cur_file in ${files[@]}; do
    for cur_version in ${versions[@]}; do
	python3 behaverify_$cur_version.py $cur_file create_root --root_args True --output_file ../models_$cur_version/$cur_file.smv --overwrite
    done
done

