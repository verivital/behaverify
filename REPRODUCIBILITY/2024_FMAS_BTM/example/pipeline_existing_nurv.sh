#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
# categories=("./dense_fixed")
# categories=("./sparse_random")

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
	num_obs=$(echo $tail_end | cut -d'_' -f2)
	echo $num_obs
	# if [ "${max_val}" -lt 47 ]; then
	#     continue
	# fi
	# if [ "${max_val}" -gt 10 ]; then
	#      continue
	# fi
	echo "setting up directory"
	rm -rf "${category}/${tail_end}/nurv/"
	mkdir "${category}/${tail_end}/nurv/"
	echo "copying python code"
	cp -r "${category}/${tail_end}/behaverify/python/" "${category}/${tail_end}/nurv/python/"
	echo "ensuring clean extract location"
	rm -rf "${category}/${tail_end}/nurv/python/loop.tar"
	rm -rf "${category}/${tail_end}/nurv/python/collision.tar"
	echo "moving read_monitor"
	cp "./nurv/read_monitor_file.py" "${category}/${tail_end}/nurv/python/read_monitor_file.py"
	echo "generating smv files"
	python3 ./nurv/make_nurv_smv.py "${max_val}" "${num_obs}" "${category}/${tail_end}/obstaclesFilled_${tail_end}.txt" "${category}/${tail_end}/nurv/python/"
	echo "generating nurv monitors"
	python3 ../../../Docker_BehaVerify/NuRV/python_script/generate.py "${category}/${tail_end}/nurv/python/nurv_collision.smv" "${category}/${tail_end}/nurv/python/collision" --generate_monitor --l 3 --L c --m "monitor" --o "monitor"
	python3 ../../../Docker_BehaVerify/NuRV/python_script/generate.py "${category}/${tail_end}/nurv/python/nurv_loop.smv" "${category}/${tail_end}/nurv/python/loop" --generate_monitor --l 3 --L c --m "monitor" --o "monitor"
	echo "extracting and moving monitors"
	tar -xf "${category}/${tail_end}/nurv/python/collision.tar" -C "${category}/${tail_end}/nurv/python/"
	mv "${category}/${tail_end}/nurv/python/user_files/monitor.c" "${category}/${tail_end}/nurv/python/collision_monitor.c"
	mv "${category}/${tail_end}/nurv/python/user_files/monitor.h" "${category}/${tail_end}/nurv/python/collision_monitor.h"
	rm -rf "${category}/${tail_end}/nurv/python/user_files"
	tar -xf "${category}/${tail_end}/nurv/python/loop.tar" -C "${category}/${tail_end}/nurv/python/"
	mv "${category}/${tail_end}/nurv/python/user_files/monitor.c" "${category}/${tail_end}/nurv/python/loop_monitor.c"
	mv "${category}/${tail_end}/nurv/python/user_files/monitor.h" "${category}/${tail_end}/nurv/python/loop_monitor.h"
	rm -rf "${category}/${tail_end}/nurv/python/user_files"
	echo "adding user interface to monitors"
	./nurv/append_nurv_info.sh "${category}/${tail_end}/nurv/python"
	echo "compiling to shared library"
	gcc -shared -fPIC -o "${category}/${tail_end}/nurv/python/collision_monitor.so" "${category}/${tail_end}/nurv/python/collision_monitor.c"
	gcc -shared -fPIC -o "${category}/${tail_end}/nurv/python/loop_monitor.so" "${category}/${tail_end}/nurv/python/loop_monitor.c"
	sleep 1
	echo "running python code"
	python3 "${category}/${tail_end}/nurv/python/ANSR_runner.py" > "${category}/${tail_end}/nurv/python/trace.txt"
	echo "creating images"
	mkdir "${category}/${tail_end}/nurv/images"
	python3 "../parse_python_output.py" "${category}/${tail_end}/nurv/python/trace.txt" "${category}/${tail_end}/nurv/images/monitor" $((max_val + 1)) $((max_val + 1))
    done
done
