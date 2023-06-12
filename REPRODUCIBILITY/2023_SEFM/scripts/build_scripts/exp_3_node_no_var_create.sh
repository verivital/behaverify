#!/bin/bash

#./make_comparison_folder_structure.sh 3_node_no_var

path_name="../../examples/3_node_no_var"

mkdir "${path_name}/gen_files"

python3 "${path_name}/gen_all.py" "${path_name}/gen_files" "${path_name}"

root_name=("sel" "seq" "p_all" "p_one")
child=("f" "s" "r")

for r in "${root_name[@]}"; do
    for c1 in "${child[@]}"; do
	for c2 in "${child[@]}"; do
	    true_name="${r}_${c1}_${c2}"
	    echo $true_name
	    ./generate_comparison.sh "${path_name}" $true_name
	done
    done
done
