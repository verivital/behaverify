#!/bin/bash


max_val=9
num_obs=2
max_size=1

for (( i==1; i<10; i++ )); do
    echo "generating obstacles"
    python3 generate_obstacles.py "${num_obs}" 0 "${max_val}" "${max_size}"
    echo "filling holes"
    python3 fill_holes.py "./ignore/obstacles_${max_val}_${num_obs}_${max_size}.txt"
    echo "computing new sizes"
    file=$(ls "./ignore" | grep "obstaclesFilled_${max_val}_[^_]*_[^.]*.txt")
    filename=$(basename $file)
    tail_end_with_ext=${filename#obstaclesFilled_}
    tail_end=${tail_end_with_ext%.txt}
    echo "----------------------------"
    echo $file
    echo $filename
    echo $tail_end_with_ext
    echo $tail_end
    # for file in "./ignore/obstaclesFilled_${max_val}*"; do
    # 	filename=$(basename $file)
    # 	tail_end_with_ext=${filename#obstaclesFilled_}
    # 	tail_end=${tail_end_with_ext%.txt}
    # 	echo "----------------------------"
    # 	echo $file
    # 	echo $filename
    # 	echo $tail_end_with_ext
    # 	echo $tail_end
    # done
    echo "assembling tree"
    python3 assemble_tree_existing_obs.py "./ignore/obstaclesFilled_${tail_end}.txt"
    echo "setting up directory"
    mkdir "../scale/${tail_end}/"
    echo "moving .tree"
    mv "./ignore/ANSRtFilled_${tail_end}.tree" "../scale/${tail_end}/ANSRtFilled_${tail_end}.tree"
    echo "setting up directory"
    mkdir "../scale/${tail_end}/python/"
    echo "generating python code"
    python3 ../../../src/dsl_to_python.py ../../../metamodel/behaverify.tx "../scale/${tail_end}/ANSRtFilled_${tail_end}.tree" "../scale/${tail_end}/python/" ANSR --recursion_limit 10000 --no_checks
    echo "moving read_monitor"
    cp "../6_2_1/python/read_monitor_file.py" "../scale/${tail_end}/python/read_monitor_file.py"
    echo "generating ltl commands"
    python3 ../../../src/create_monitor.py command ../../../metamodel/behaverify.tx "../scale/${tail_end}/ANSRtFilled_${tail_end}.tree" "../scale/${tail_end}/python/" --recursion_limit 10000 --no_checks
    echo "reading ltl commands"
    collision_command=$(cat "../scale/${tail_end}/python/collision_monitor.txt")
    loop_command=$(cat "../scale/${tail_end}/python/loop_monitor.txt")
    echo "generating ba"
    python3 ../../../Docker_BehaVerify/LTL2BA/python_script/generate.py "$collision_command" "../scale/${tail_end}/python/collision"
    python3 ../../../Docker_BehaVerify/LTL2BA/python_script/generate.py "$loop_command" "../scale/${tail_end}/python/loop"
    echo "extracting and moving ba"
    tar -xf "../scale/${tail_end}/python/collision.tar" -C "../scale/${tail_end}/python/"
    mv "../scale/${tail_end}/python/user_files/collision" "../scale/${tail_end}/python/collision.ba"
    rm -rf "../scale/${tail_end}/python/user_files"
    tar -xf "../scale/${tail_end}/python/loop.tar" -C "../scale/${tail_end}/python/"
    mv "../scale/${tail_end}/python/user_files/loop" "../scale/${tail_end}/python/loop.ba"
    rm -rf "../scale/${tail_end}/python/user_files"
    echo "generating monitors"
    python3 ../../../src/create_monitor.py mode "../scale/${tail_end}/python/collision.ba" "../scale/${tail_end}/python/collision_monitor.py"
    python3 ../../../src/create_monitor.py mode "../scale/${tail_end}/python/loop.ba" "../scale/${tail_end}/python/loop_monitor.py"
    echo "running python code"
    python3 "../scale/${tail_end}/python/ANSR_runner.py" > "../scale/${tail_end}/python/trace.txt"
    echo "creating images"
    mkdir "../scale/${tail_end}/images"
    python3 "../parse_python_output.py" "../scale/${tail_end}/python/trace.txt" "../scale/${tail_end}/images/monitor" $((max_val + 1)) $((max_val + 1))
    max_val=$((max_val + 5))
    num_obs=$((num_obs + 1))
    max_size=$((max_size + 1))
done


