#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_types=("behaverify" "copilot" "monitorless" "nurv")

for category in "${categories[@]}"; do
    echo $category
    for mon_type in "${mon_types[@]}"; do
	rm -rf "${category}/timing_${mon_type}.txt"
	touch "${category}/timing_${mon_type}.txt"
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
	    echo "moving new timing .py file"
	    cp "./timing/ANSR_runner.py" "${category}/${tail_end}/${mon_type}/python/TIMING.py"
	    rm -rf "${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json"
	    hyperfine --warmup 3 --runs 25 --export-json="${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json" "python3 ${category}/${tail_end}/${mon_type}/python/TIMING.py"
	    median=$(jq -r '.results[0].median' "${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json")
	    echo "${max_val} ::> ${median}" >> "${category}/timing_${mon_type}.txt"
	    sleep 3
	done
    done
done
