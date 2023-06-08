#!/bin/bash

#./make_comparison_folder_structure.sh 3_node_no_var

mkdir ../examples/3_node_no_var/gen_files

python3 ../examples/3_node_no_var/gen_all.py ../examples/3_node_no_var/gen_files/ ../examples/3_node_no_var/

root_name=("sel" "seq" "p_all" "p_one")
child=("f" "s" "r")

for r in "${root_name[@]}"; do
    for c1 in "${child[@]}"; do
	for c2 in "${child[@]}"; do
	    true_name="${r}_${c1}_${c2}"
	    echo $true_name
	    ./generate_comparison.sh ../examples/3_node_no_var $true_name
	done
    done
done
