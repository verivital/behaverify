#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_type="design_time"

for category in "${categories[@]}"; do
    echo $category
    rm -rf "${category}/timing_v4_${mon_type}.txt"
    touch "${category}/timing_v4_${mon_type}.txt"
    for folder in "${category}"/*; do
	if [ -f "${folder}" ]; then
	    continue
	fi
	echo "----------------------------"
	echo $folder
	tail_end=$(basename "${folder}")
	echo $tail_end
	max_val=$(echo $tail_end | cut -d'_' -f1)
	echo $max_val
	filename="${category}/${tail_end}/${mon_type}/safety.txt"
	matches=($(grep -oP 'elapse: \K[0-9]+\.[0-9]+(?= seconds)' "$filename"))
	if [ ${#matches[@]} -ge 3 ]; then
	    third_elapse_time=${matches[2]}
	    
	else
	    echo "There are not enough 'elapse' instances in the file."
	fi
	echo "${max_val} ::> ${third_elapse_time}" >> "${category}/timing_v4_${mon_type}.txt"
    done
done
