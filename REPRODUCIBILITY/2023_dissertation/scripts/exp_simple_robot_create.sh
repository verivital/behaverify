#!/bin/bash

for num in {2..20}; do
    ./generate.sh ../examples/simple_robot simple_robot_$num
done
