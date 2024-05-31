#!/bin/bash

#categories=("./sparse_random" "./dense_fixed")
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
	rm -rf "${category}/${tail_end}/behaverify/"
	mkdir "${category}/${tail_end}/behaverify/"
	mkdir "${category}/${tail_end}/behaverify/python/"
	echo "generating python code"
	python3 ../../../src/dsl_to_python.py ../../../metamodel/behaverify.tx "${category}/${tail_end}/ANSRtFilled_${tail_end}.tree" "${category}/${tail_end}/behaverify/python/" ANSR --recursion_limit 10000 --no_checks
	echo "moving read_monitor"
	cp "./behaverify/read_monitor_file_c.py" "${category}/${tail_end}/behaverify/python/read_monitor_file.py"
	echo "generating ltl commands"
	python3 ../../../src/create_c_monitor.py make_ltl2ba ../../../metamodel/behaverify.tx "${category}/${tail_end}/ANSRtFilled_${tail_end}.tree" "${category}/${tail_end}/behaverify/python/" --recursion_limit 10000 --no_checks
	echo "reading ltl commands"
	collision_command=$(cat "${category}/${tail_end}/behaverify/python/collision_monitor.txt")
	loop_command=$(cat "${category}/${tail_end}/behaverify/python/loop_monitor.txt")
	echo "generating ba"
	python3 ../../../Docker_BehaVerify/LTL2BA/python_script/generate.py "$collision_command" "${category}/${tail_end}/behaverify/python/collision"
	python3 ../../../Docker_BehaVerify/LTL2BA/python_script/generate.py "$loop_command" "${category}/${tail_end}/behaverify/python/loop"
	echo "extracting and moving ba"
	tar -xf "${category}/${tail_end}/behaverify/python/collision.tar" -C "${category}/${tail_end}/behaverify/python/"
	mv "${category}/${tail_end}/behaverify/python/user_files/collision" "${category}/${tail_end}/behaverify/python/collision.ba"
	rm -rf "${category}/${tail_end}/behaverify/python/user_files"
	tar -xf "${category}/${tail_end}/behaverify/python/loop.tar" -C "${category}/${tail_end}/behaverify/python/"
	mv "${category}/${tail_end}/behaverify/python/user_files/loop" "${category}/${tail_end}/behaverify/python/loop.ba"
	rm -rf "${category}/${tail_end}/behaverify/python/user_files"
	echo "generating monitors"
	python3 ../../../src/create_c_monitor.py ba_to_monitor "${category}/${tail_end}/behaverify/python/collision.ba" "${category}/${tail_end}/behaverify/python/collision_monitor.c" "${category}/${tail_end}/behaverify/python/collision_monitor.h"
	python3 ../../../src/create_c_monitor.py ba_to_monitor "${category}/${tail_end}/behaverify/python/loop.ba" "${category}/${tail_end}/behaverify/python/loop_monitor.c" "${category}/${tail_end}/behaverify/python/loop_monitor.h"
	echo "compiling to shared library"
	gcc -shared -fPIC -o "${category}/${tail_end}/behaverify/python/collision_monitor.so" "${category}/${tail_end}/behaverify/python/collision_monitor.c"
	gcc -shared -fPIC -o "${category}/${tail_end}/behaverify/python/loop_monitor.so" "${category}/${tail_end}/behaverify/python/loop_monitor.c"
	echo "running python code"
	python3 "${category}/${tail_end}/behaverify/python/ANSR_runner.py" > "${category}/${tail_end}/behaverify/python/trace.txt"
	echo "creating images"
	mkdir "${category}/${tail_end}/behaverify/images"
	python3 "../parse_python_output.py" "${category}/${tail_end}/behaverify/python/trace.txt" "${category}/${tail_end}/behaverify/images/monitor" $((max_val + 1)) $((max_val + 1))
    done
done
