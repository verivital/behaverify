#!/bin/bash
folders=("smv" "results" "tree" "processed_data" "xml")
for folder in "${folders[@]}"; do
    cur_folder=../../examples/$1/$folder
    if test -e $cur_folder; then
	rm -r $cur_folder
    fi
    mkdir $cur_folder
done
