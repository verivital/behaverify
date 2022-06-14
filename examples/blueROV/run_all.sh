#!/bin/bash

#folders=("./models_selector_mixed" "./models_selector_parallel"  "./models_selector_non_parallel" "./models_sequence" "./models_path" "./models_double_path")
#folders=("./models_selector_parallel" "./models_sequence")
#folders=("./models_selector_parallel" "./models_sequence" "./models_path" "./models_double_path")
files=("blueROV_full" "blueROV_full_small" "blueROV_warnings_only")
folders=("./models_double_path")
#folders=("./models_path")
#files=("blueROV_warnings_only")

for cur_folder in ${folders[@]}; do
    for cur_file in ${files[@]}; do
	#./run_states.sh $cur_folder $cur_file ltl_full
	./run_ltl.sh $cur_folder $cur_file ltl_battery_only
	./run_ltl.sh $cur_folder $cur_file ltl_full
	#./run_ltl_silent.sh $cur_folder $cur_file ltl_battery_only
	#./run_ltl_silent.sh $cur_folder $cur_file ltl_full
    done
done

