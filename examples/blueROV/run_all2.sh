#!/bin/bash

#folders=("./models_selector_mixed" "./models_selector_mixed2" "./models_selector_parallel"  "./models_selector_parallel2" "./models_selector_non_parallel" "./models_selector_non_parallel2" "./models_sequence" "./models_sequence2" "./models_ultimate")
folders=("./models_ultimate")
files=("blueROV_full" "blueROV_full_small" "blueROV_warnings_only")
#files=("blueROV_warnings_only")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	./run_tests2.sh $cur_folder $cur_file.smv
    done
done

