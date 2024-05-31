#!/bin/bash


categories=("./dense_fixed" "./sparse_random")

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
	echo "assembling tree"
	mkdir "${category}/${tail_end}/design_time/"
	cp "${category}/${tail_end}/obstaclesFilled_${tail_end}.txt" "${category}/${tail_end}/design_time/obstaclesFilled_${tail_end}.txt"
	python3 ../a_star_files/assemble_tree_existing_obs.py "${category}/${tail_end}/design_time/obstaclesFilled_${tail_end}.txt" "../a_star_files/template_monitor_design_time.tree"
    done
done
