#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
mon_types=("behaverify" "copilot" "monitorless")

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
	    echo "moving new timing c file"
	    main_file="main.c"
	    cp "./${mon_type}/${main_file}" "${category}/${tail_end}/${mon_type}/python/main.c"
	    rm -rf "${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json"
	    if [ "${mon_type}" = "monitorless" ]; then
		gcc -o "${category}/${tail_end}/${mon_type}/python/timing" "${category}/${tail_end}/${mon_type}/python/main.c" "${category}/${tail_end}/${mon_type}/python/obstacle_file.c"
		hyperfine -N --warmup 200 --runs 10000 --export-json="${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json" "${category}/${tail_end}/${mon_type}/python/timing 1000 ${max_val}"
	    else
		gcc -o "${category}/${tail_end}/${mon_type}/python/timing" "${category}/${tail_end}/${mon_type}/python/main.c" "${category}/${tail_end}/${mon_type}/python/loop_monitor.c" "${category}/${tail_end}/${mon_type}/python/collision_monitor.c" "${category}/${tail_end}/${mon_type}/python/obstacle_file.c"
		hyperfine -N --warmup 200 --runs 10000 --export-json="${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json" "${category}/${tail_end}/${mon_type}/python/timing 1000 ${max_val}"
	    fi
	    median=$(jq -r '.results[0].median' "${category}/${tail_end}/${mon_type}/python/TIMING_RESULT.json")
	    echo "${max_val} ::> ${median}" >> "${category}/timing_${mon_type}.txt"
	    sleep 1
	done
    done
done
