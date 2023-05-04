#!/bin/bash


all_args=( "$@" )
path_name="${all_args[0]}"
file_name="${all_args[1]}"
encodings=("${all_args[@]:2}")

for encoding in "${encodings[@]}"; do
    echo "running for:"
    echo $path_name $file_name $encoding
    
    echo "ctl"
    #./test_ctl.sh $path_name $file_name $encoding
    timeout 3m ./test_ctl_silent.sh $path_name $file_name $encoding
    echo "ltl"
    #./test_ltl.sh $path_name $file_name $encoding
    timeout 3m ./test_ltl_silent.sh $path_name $file_name $encoding
    echo "invar"
    #./test_ltl.sh $path_name $file_name $encoding
    timeout 3m ./test_invar_silent.sh $path_name $file_name $encoding
    echo "states"
    timeout 3m ./test_model.sh $path_name $file_name $encoding
    timeout 3m ./test_states.sh $path_name $file_name $encoding
    timeout 3m ./test_states_silent.sh $path_name $file_name $encoding
done
