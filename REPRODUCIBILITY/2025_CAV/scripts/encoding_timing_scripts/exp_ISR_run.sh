#!/bin/bash

min_val=5
max_val=10
step_size=5

path_name="../../examples/ISR"
exp_name="ISR"
for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    ../test_scripts/test_ctl.sh $path_name "${exp_name}_${num}" full_opt
done
