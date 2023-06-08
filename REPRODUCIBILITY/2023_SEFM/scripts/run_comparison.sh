#!/bin/bash

all_args=( "$@" )
path_name="${all_args[0]}"
file_name="${all_args[1]}"

python3 $path_name/gen_files/$file_name/"$file_name"_runner.py > $path_name/gen_files/$file_name/PYTHON_OUTPUT.txt
../nuXmv -source command_simulate $path_name/gen_files/$file_name/"$file_name".smv > $path_name/gen_files/$file_name/NUXMV_OUTPUT.txt
python3 compare.py $file_name $path_name/gen_files/$file_name/PYTHON_OUTPUT.txt $path_name/gen_files/$file_name/NUXMV_OUTPUT.txt >> $path_name/results/log.txt
