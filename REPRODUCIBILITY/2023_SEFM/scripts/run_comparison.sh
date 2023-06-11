#!/bin/bash

all_args=( "$@" )
path_name="${all_args[0]}"
file_name="${all_args[1]}"
real_path="${path_name}/gen_files/${file_name}"

python3 "${real_path}/${file_name}_runner.py" > "${real_path}/OUTPUT_PYTHON.txt"
../nuXmv -source command_simulate "${real_path}/${file_name}.smv" > "${real_path}/OUTPUT_NUXMV.txt"
../nuXmv -source command_simulate "${real_path}/OPT_${file_name}.smv" > "${real_path}/OUTPUT_OPT_NUXMV.txt"
python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_NUXMV.txt" "${real_path}/OUTPUT_OPT_NUXMV.txt" >> "${path_name}/results/log.txt"
