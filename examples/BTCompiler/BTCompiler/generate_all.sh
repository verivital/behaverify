#!/bin/bash

files=("serene_uc1")
versions=("total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar")
#versions=("selector_mixed" "selector_parallel" "selector_non_parallel" "sequence" "path" "total" "double_path" "double_path_clean" "double_path_cleaner" "double_path_ivar")


for cur_file in ${files[@]}; do
    for cur_version in ${versions[@]}; do
	python3 behaverify_$cur_version.py $cur_file create_root --root_args False --output_file ../models_$cur_version/$cur_file.smv --overwrite
    done
done
