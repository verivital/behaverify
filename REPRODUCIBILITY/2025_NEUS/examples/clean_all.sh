#!/bin/bash
folders=('AcasXu' 'AcasXu_closed_loop' 'grid_world' 'grid_world_big')
sub_folders=('results' 'smv' 'tree' 'processed_data' 'xml' 'LaTeX' 'images')

for folder in "${folders[@]}"; do
    for sub_folder in "${sub_folders[@]}"; do
	if test -e ./$folder/$sub_folder; then 
	    rm -r ./$folder/$sub_folder
	fi
	mkdir ./$folder/$sub_folder
    done
done
