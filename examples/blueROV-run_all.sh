#!/bin/bash

folders=("models_leaf" "models_total" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child" "models_total_internal_status")
folders=("models_leaf" "models_leaf_no_IVAR" "models_total_no_IVAR_errorless_unique_child" "models_total_internal_status")
files=("blueROV_warnings_only" "blueROV_small" "blueROV_full")
ltls=("_battery" "_emergency" "_home_reached" "_obstacle" "_sensor")

for cur_folder in ${folders[@]}; do
    timeout_val=12m
    for cur_file in ${files[@]}; do
	for ltl in ${ltls[@]}; do
	    echo $cur_folder $cur_file$ltl
	    #timeout $timeout_val ./run_tests.sh blueROV $cur_folder $cur_file$ltl

	    echo "states"
	    timeout 1m ./run_states.sh blueROV $cur_folder $cur_file$ltl
	    echo "states_silent"
	    timeout 1m ./run_states_silent.sh blueROV $cur_folder $cur_file$ltl
	    echo "model"
	    timeout 1m ./run_model.sh blueROV $cur_folder $cur_file$ltl
	    echo "ltl_silent"
	    timeout 10m ./run_ltl_silent.sh blueROV $cur_folder $cur_file$ltl
	    echo "ltl"
	    timeout $timeout_val ./run_ltl.sh blueROV $cur_folder $cur_file$ltl
	    if [ $? == 124 ]; then
		timeout_val=3s
	    fi
	done
    done
done
