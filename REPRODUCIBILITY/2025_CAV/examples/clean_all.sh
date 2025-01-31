#!/bin/bash
folders=('bigger_fish' 'binary_tree' 'binary_tree_2')
sub_folders=('results' 'smv' 'tree' 'processed_data')

for folder in "${folders[@]}"; do
    for sub_folder in "${sub_folders[@]}"; do
	if test -e ./$folder/$sub_folder; then 
	    rm -r ./$folder/$sub_folder
	fi
    done
done
