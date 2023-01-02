#!/bin/bash

folders=("models_total_v3")

node=("sel" "seq" "par")
mem=("True" "False")

for cur_folder in ${folders[@]}; do
    timeout_val=1m
    timeout_val_silent=5m
    fail_count=3
    fail_count_silent=3
    
    for node1 in ${node[@]}; do
	for mem1 in ${mem[@]}; do
	    for node2 in ${node[@]}; do
		for mem2 in ${mem[@]}; do
		    echo $node1-$mem1-$node2-$mem2 $cur_folder
		    #timeout $timeout_val ./run_tests.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    echo "states"
		    timeout 7s ./run_states.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    echo "states_silent"
		    timeout 7s ./run_states_silent.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    echo "model"
		    timeout 7s ./run_model.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    echo "ltl_silent"
		    timeout $timeout_val_silent ./run_ltl_silent.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    if [ $? == 124 ]; then
			fail_count_silent=$(($fail_count_silent-1))
			if [ $fail_count_silent == 0 ]; then
			    timeout_val_silent=1s
			fi
		    fi
		    echo "ltl"
		    timeout $timeout_val ./run_ltl.sh basic2 $cur_folder $node1-$mem1-$node2-$mem2
		    if [ $? == 124 ]; then
			fail_count=$(($fail_count-1))
			if [ $fail_count == 0 ]; then
			    timeout_val=1s
			fi
		    fi
		done
	    done
	done
    done
done
