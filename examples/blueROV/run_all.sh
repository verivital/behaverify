#!/bin/bash

folders=("./models_selector_mixed" "./models_selector_mixed2" "./models_selector_parallel"  "./models_selector_parallel2" "./models_selector_non_parallel" "./models_selector_non_parallel2" "./models_sequence" "./models_sequence2")
files=("blueROV_full" "blueROV_full_small" "blueROV_warnings_only")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	./run_tests.sh $cur_folder $cur_file.smv
    done
done

