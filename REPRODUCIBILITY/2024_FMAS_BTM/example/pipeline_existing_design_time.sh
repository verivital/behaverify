#!/bin/bash

categories=("./sparse_random" "./dense_fixed")
ulimit -s unlimited

python_behaverify=python3
python_results=python3

if [[ $# -ge 2 ]]; then
    python_behaverify=$1
    python_results=$2
fi

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
	mkdir "${category}/${tail_end}/design_time/smv/"
	echo "generating smv model"
	$python_behaverify ../src/dsl_to_nuxmv.py ../metamodel/behaverify.tx "${category}/${tail_end}/design_time/ANSRtFilled_${tail_end}.tree" "${category}/${tail_end}/design_time/smv/ANSRtFilled_${tail_end}.smv" --recursion_limit 10000 --no_checks
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
	echo "running safety"
	../nuXmv -source ../scripts/nuxmv_commands/command_all_invar "${category}/${tail_end}/design_time/smv/ANSRtFilled_${tail_end}.smv" > "${category}/${tail_end}/design_time/safety.txt" 
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
	../nuXmv -source ../scripts/nuxmv_commands/command_all_ltl "${category}/${tail_end}/design_time/smv/ANSRtFilled_${tail_end}.smv" > "${category}/${tail_end}/design_time/ltl.txt" 
	sleep 3
    done
done
