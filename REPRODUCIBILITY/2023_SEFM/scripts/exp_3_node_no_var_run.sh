#!/bin/bash

mkdir ../examples/3_node_no_var/results
rm ../examples/3_node_no_var/results/log.txt
touch ../examples/3_node_no_var/results/log.txt


root_name=("sel" "seq" "p_all" "p_one")
child=("f" "s" "r")

for r in "${root_name[@]}"; do
    for c1 in "${child[@]}"; do
	for c2 in "${child[@]}"; do
	    true_name="${r}_${c1}_${c2}"
	    echo $true_name
	    ./run_comparison.sh ../examples/3_node_no_var $true_name
	done
    done
done
