#!/bin/bash
all_args=( "$@" )
# echo "${all_args[*]}"
path_name="${all_args[0]}"
file_name="${all_args[1]}"
encodings=("${all_args[@]:2}")

for encoding in "${encodings[@]}"; do
    # echo $encoding
    # echo $file_name
    # echo $path_name
    # ./make_behave.sh $path_name $file_name $encoding
    ./make_smv.sh $path_name $file_name $encoding
done
