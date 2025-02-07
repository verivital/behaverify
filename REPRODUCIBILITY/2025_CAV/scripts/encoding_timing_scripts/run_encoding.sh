#!/bin/bash

file_with_experiment_info=$1  # this is assumed to be a single line with path_name experiment_name
file_with_experiment_range=$2  # this is assumed to be a single line with the range of file_name extensions. e.g., if we re running f1, f2, f3, f4, f5, then f is the experiment name, and this should have 1 2 3 4 5
file_with_encodings=$3  # this is assumed to be a single line with each encoding seperated by a space
file_with_tests=$4  # this is assumed to be a single line with each test seperated by a space

temp=$(cat "$file_with_experiment_info")
experiment_info=($temp)
path_name="${experiment_info[0]}"
experiment_name="${experiment_info[1]}"

temp=$(cat "$file_with_experiment_range")
range_info=($temp)

temp=$(cat "$file_with_encodings")
encodings=($temp)

temp=$(cat "$file_with_tests")
tests=($temp)
    
num_encodings="${#encodings[@]}"
num_tests="${#tests[@]}"

timeout_array=()
timeout_length=$((num_encodings * num_tests))

for (( i=0; i<timeout_length; i++ )); do
    timeout_array[$i]=2
done

for range_val in "${range_info[@]}"; do
    file_name="${experiment_name}_${range_val}"
    encoding_index=0
    test_index=0
    for encoding_val in "${encodings[@]}"; do
	for test_val in "${tests[@]}"; do
	    echo "running ${test_val} for:"
	    echo $path_name $file_name $encoding_val
	    array_index=$((encoding_index * num_tests + test_index))
	    echo $array_index
	    cur_val=${timeout_array[$array_index]}
	    if [[ "$cur_val" -le 1 ]]; then
		echo "too many timeouts. skipping test"
	    else
		timeout 3m "../test_scripts/${test_val}.sh" $path_name $file_name $encoding_val
		if [[ $? -eq 124 ]]; then
		    timeout_array[$array_index]=$((cur_val - 1))
		fi
	    fi
	    test_index=$((test_index + 1))
	done
	test_index=0
	encoding_index=$((encoding_index + 1))
    done
done
