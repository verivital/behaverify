#!/bin/bash

folders=("models_leaf" "models_total" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child")
files=("blueROV_warnings_only" "blueROV_small" "blueROV_full")
ltls=("_battery" "_emergency" "_home_reached" "_obstacle" "_sensor")

for cur_folder in ${folders[@]}; do
    timeout_val=1h
    for ltl in ${ltls[@]}; do
	for cur_file in ${files[@]}; do
	    echo $cur_folder $cur_file$ltl
	    timeout $timeout_val ./run_tests.sh blueROV $cur_folder $cur_file$ltl
	    if [ $? == 0 ]; then
		timeout_val=4m
	    fi
	done
    done
done
