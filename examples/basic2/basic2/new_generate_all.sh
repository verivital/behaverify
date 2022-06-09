#!/bin/bash

#files=("serene_uc1")
#files=("example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")
files=("example0")
#files=("example1")

#versions=("double_path_clean" "double_path_cleaner")
versions=("total")


for cur_file in ${files[@]}; do
    for cur_version in ${versions[@]}; do
	python3 behaverify_$cur_version.py $cur_file create_root --root_args False --output_file ../models_$cur_version/$cur_file.smv --overwrite
    done
done

