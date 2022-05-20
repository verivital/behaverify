#!/bin/bash

folders=("./models_selector_mixed" "./models_selector_mixed2" "./models_selector_parallel"  "./models_selector_parallel2" "./models_selector_non_parallel" "./models_selector_non_parallel2" "./models_sequence" "./models_sequence2" "./models_ultimate")
#folders=("./models_ultimate")
files=("example1" "example2" "example3" "example4" "example5" "example6" "example7" "example8")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	./run_tests.sh $cur_folder $cur_file.smv
    done
done

