#!/bin/bash

categories=("./dense_fixed" "./sparse_random")
# categories=("./sparse_random")

python_behaverify=python3
python_results=python3

if [[ $# -ge 3 ]]; then
    python_behaverify=$2
    python_results=$3
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
	num_obs=$(echo $tail_end | cut -d'_' -f2)
	echo $num_obs
	echo "setting up directory"
	rm -rf "${category}/${tail_end}/copilot/"
	mkdir "${category}/${tail_end}/copilot/"
	echo "copying python code"
	cp -r "${category}/${tail_end}/behaverify/python/" "${category}/${tail_end}/copilot/python/"
	echo "ensuring clean extract location"
	rm -rf "${category}/${tail_end}/copilot/python/loop.tar"
	rm -rf "${category}/${tail_end}/copilot/python/collision.tar"
	echo "moving read_monitor"
	cp "./copilot/read_monitor_file.py" "${category}/${tail_end}/copilot/python/read_monitor_file.py"
	echo "generating .hs files"
	$python_behaverify ./copilot/make_copilot_hs.py "${max_val}" "${num_obs}" "${category}/${tail_end}/obstaclesFilled_${tail_end}.txt" "${category}/${tail_end}/copilot/python/"
	echo "generating copilot monitors"
	runhaskell "${category}/${tail_end}/copilot/python/CollisionMonitor.hs" "${category}/${tail_end}/copilot/python/collision"
	runhaskell "${category}/${tail_end}/copilot/python/LoopMonitor.hs" "${category}/${tail_end}/copilot/python/loop"
	echo "extracting and moving monitors"
	# tar -xf "${category}/${tail_end}/copilot/python/collision.tar" -C "${category}/${tail_end}/copilot/python/"
	# mv "${category}/${tail_end}/copilot/python/user_files/collision_monitor.c" "${category}/${tail_end}/copilot/python/collision_monitor.c"
	# mv "${category}/${tail_end}/copilot/python/user_files/collision_monitor.h" "${category}/${tail_end}/copilot/python/collision_monitor.h"
	# mv "${category}/${tail_end}/copilot/python/user_files/collision_monitor_types.h" "${category}/${tail_end}/copilot/python/collision_monitor_types.h"
	# rm -rf "${category}/${tail_end}/copilot/python/user_files"
	# tar -xf "${category}/${tail_end}/copilot/python/loop.tar" -C "${category}/${tail_end}/copilot/python/"
	# mv "${category}/${tail_end}/copilot/python/user_files/loop_monitor.c" "${category}/${tail_end}/copilot/python/loop_monitor.c"
	# mv "${category}/${tail_end}/copilot/python/user_files/loop_monitor.h" "${category}/${tail_end}/copilot/python/loop_monitor.h"
	# mv "${category}/${tail_end}/copilot/python/user_files/loop_monitor_types.h" "${category}/${tail_end}/copilot/python/loop_monitor_types.h"
	# rm -rf "${category}/${tail_end}/copilot/python/user_files"
	echo "adding user interface to monitors"
	./copilot/append_copilot_info.sh "${category}/${tail_end}/copilot/python"
	echo "compiling to shared library"
	gcc -shared -fPIC -o "${category}/${tail_end}/copilot/python/collision_monitor.so" "${category}/${tail_end}/copilot/python/collision_monitor.c"
	gcc -shared -fPIC -o "${category}/${tail_end}/copilot/python/loop_monitor.so" "${category}/${tail_end}/copilot/python/loop_monitor.c"
	sleep 1
	echo "running python code"
	$python_behaverify "${category}/${tail_end}/copilot/python/ANSR_runner.py" > "${category}/${tail_end}/copilot/python/trace.txt"
	echo "creating images"
	mkdir "${category}/${tail_end}/copilot/images"
	$python_results "../parse_python_output.py" "${category}/${tail_end}/copilot/python/trace.txt" "${category}/${tail_end}/copilot/images/monitor" $((max_val + 1)) $((max_val + 1))
    done
done
