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
	echo "setting up directory"
	rm -rf "${category}/${tail_end}/monitorless/"
	mkdir "${category}/${tail_end}/monitorless/"
	echo "copying python code"
	cp -r "${category}/${tail_end}/behaverify/python/" "${category}/${tail_end}/monitorless/python/"
	echo "moving read_monitor"
	cp "./monitorless/read_monitor_file.py" "${category}/${tail_end}/monitorless/python/read_monitor_file.py"
    done
done
