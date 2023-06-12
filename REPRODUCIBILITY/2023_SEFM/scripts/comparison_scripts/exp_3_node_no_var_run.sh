#!/bin/bash


path_name="../../examples/3_node_no_var"

mkdir "${path_name}/results"
rm "${path_name}/results/log.txt"
touch "${path_name}/results/log.txt"


root_name=("sel" "seq" "p_all" "p_one")
child=("f" "s" "r")

for r in "${root_name[@]}"; do
    for c1 in "${child[@]}"; do
	for c2 in "${child[@]}"; do
	    true_name="${r}_${c1}_${c2}"
	    echo $true_name
	    ./run_comparison.sh "${path_name}" $true_name
	done
    done
done
