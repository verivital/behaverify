#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_types=("behaverify" "copilot" "monitorless" "nurv")

for category in "${categories[@]}"; do
    echo $category
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
	    echo "creating new obstacle file"
	    python3 create_new_obstacle_file.py "${max_val}" "${category}/${tail_end}/${mon_type}/python/ANSR_environment.py" "${category}/${tail_end}/${mon_type}/python/obstacle_file.py"
	done
    done
done
