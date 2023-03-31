#!/bin/bash

for num in {2..20}; do
    echo $num
    ./run_all.sh ../examples/simple_robot simple_robot_$num
done
