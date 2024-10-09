#!/bin/bash

categories=("./sparse_random" "./dense_fixed")
ulimit -s unlimited
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
	echo "running safety"
	~/tools/nuXmv -source ../../../scripts/nuxmv_commands/command_all_invar "${category}/${tail_end}/design_time/smv/ANSRtFilled_${tail_end}.smv" > "${category}/${tail_end}/design_time/safety.txt" 
	sleep 3
    done
done

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
	echo "running ltl"
	~/tools/nuXmv -source ../../../scripts/nuxmv_commands/command_all_ltl "${category}/${tail_end}/design_time/smv/ANSRtFilled_${tail_end}.smv" > "${category}/${tail_end}/design_time/ltl.txt" 
	sleep 3
    done
done
