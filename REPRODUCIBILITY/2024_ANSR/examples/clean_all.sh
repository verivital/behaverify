#!/bin/bash
folders=('small' 'big')
sub_folders=('results' 'smv' 'tree' 'images')

echo "um..."

for folder in "${folders[@]}"; do
    for sub_folder in "${sub_folders[@]}"; do
	if test -e ./$folder/$sub_folder; then 
	    rm -r ./$folder/$sub_folder
	fi
	mkdir ./$folder/$sub_folder
    done
done
