#!/bin/bash
folders=('BT2BIP' 'BT2Fiacre' 'MoVe4BT' 'DrunkenDrone' 'NetworkExample')
sub_folders=('results' 'smv' 'tree' 'processed_data' 'xml' 'LaTeX')

for folder in "${folders[@]}"; do
    for sub_folder in "${sub_folders[@]}"; do
	if test -e ./$folder/$sub_folder; then 
	    rm -r ./$folder/$sub_folder
	fi
    done
done
