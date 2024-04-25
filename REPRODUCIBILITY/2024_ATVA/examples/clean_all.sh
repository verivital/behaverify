#!/bin/bash
folders=('ISR' 'bigger_fish' 'simple_robot')
sub_folders=('results' 'smv' 'tree' 'processed_data' 'xml')

for folder in "${folder[@]}"; do
    for sub_folder in "${sub_folder[@]}"; do
	if test -e ./$folder/$sub_folder; then 
	    rm -r ./$folder/$sub_folder
	fi
    done
done
