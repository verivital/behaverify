#!/bin/bash

min_val=5
max_val=10
step_size=5


path_name="../../examples/ANSR_no_net"
exp_name="ANSR_no_net"

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    ../test_scripts/test_ctl.sh $path_name "${exp_name}_${num}" full_opt
    ../test_scripts/test_ctl_silent.sh $path_name "${exp_name}_${num}" full_opt
done
