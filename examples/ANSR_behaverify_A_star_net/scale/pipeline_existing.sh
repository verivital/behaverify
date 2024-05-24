#!/bin/bash

for folder in ./*; do
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
    mkdir "../scale/${tail_end}/python/"
    echo "generating python code"
    python3 ../../../src/dsl_to_python.py ../../../metamodel/behaverify.tx "../scale/${tail_end}/ANSRtFilled_${tail_end}.tree" "../scale/${tail_end}/python/" ANSR --recursion_limit 10000 --no_checks
    echo "moving read_monitor"
    cp "./read_monitor_file.py" "../scale/${tail_end}/python/read_monitor_file.py"
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
done


