#!/bin/bash

files=("example0" "example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")
versions=("BTCompiler" "leaf" "leaf_no_IVAR" "total" "total_no_IVAR_errorless_unique_child")


for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for cur_file in ${files[@]}; do
	python3 behaverify_$cur_version.py $cur_file create_root --root_args False --output_file ../models_$cur_version/$cur_file.smv --overwrite
    done
done
