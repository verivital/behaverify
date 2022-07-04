#!/bin/bash

versions=("BTCompiler" "leaf_v2" "total_v2" "total_v3")
versions=("total_v3")

node=("sel" "seq" "par")
mem=("True" "False")

for cur_version in ${versions[@]}; do
    mkdir -p ../models_$cur_version
    for node1 in ${node[@]}; do
	for mem1 in ${mem[@]}; do
	    for node2 in ${node[@]}; do
		for mem2 in ${mem[@]}; do
		    python3 behaverify_$cur_version.py all_ver.py create_root --root_args $mem1 $mem2 --string_args $node1 $node2 --specs_input_file ../modules_and_specs/$cur_version.smv --output_file ../models_$cur_version/$node1-$mem1-$node2-$mem2.smv --overwrite
		done
	    done
	done
    done
done
