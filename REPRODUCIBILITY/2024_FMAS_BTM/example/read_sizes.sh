#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_types=("behaverify" "copilot" "nurv")

for category in "${categories[@]}"; do
    echo $category
    for mon_type in "${mon_types[@]}"; do
	rm -rf "${category}/collision_${mon_type}_sizes.txt"
	touch "${category}/collision_${mon_type}_sizes.txt"
    done
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
	for mon_type in "${mon_types[@]}"; do
	    file_ext=".c"
	    if [ "${mon_type}" = "behaverify" ]; then
		file_ext=".py"
	    fi
	    file_name="${category}/${tail_end}/${mon_type}/python/collision_monitor${file_ext}"
	    file_size=$(stat -c %s $file_name)
	    echo "${max_val} ::> ${file_size}" >> "${category}/collision_${mon_type}_sizes.txt"
	done
    done
done
