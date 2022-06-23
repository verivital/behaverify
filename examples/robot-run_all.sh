#!/bin/bash
#                 0              1           2                   3                        4                   5                           6                                7
folders=("models_BTCompiler" "models_leaf" "models_total" "models_total_errorless" "models_leaf_no_IVAR" "models_total_no_IVAR" "models_total_no_IVAR_errorless" "models_total_no_IVAR_errorless_unique_child")
folders=("models_total")
#        0  1  2 3 4  5 6  7
#max_val=(50 50 4 5 50 6 8 50)
#max_val=(0 0 0 0 0 0 0 25)

for cur_val in {0..7}; do
    cur_folder=${folders[$cur_val]}
    timeout_val=300s
    #cur_max=${max_val[$cur_val]}
    #echo $cur_folder $cur_max
    #for ((sel_num=1;sel_num<=$cur_max;sel_num++)); do
    for sel_num in {1..50}; do
	echo $sel_num $cur_folder
	timeout $timeout_val ./run_tests.sh robot $cur_folder $sel_num
	if [ $? == 0 ]; then
	    timeout_val=15s
	fi
    done
done
