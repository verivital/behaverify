#!/bin/bash

path_name=$1
file_name=$2
use_haskell=$3  # 1 means yes, 0 means no.
use_nuxmv=$4  # 1 means yes, 0 means no. 2 is set to 1.
use_msat=$5  # 1 means yes, 0 means no. if no, uses go.
real_path="${path_name}/gen_files/${file_name}"

if [[ $use_nuxmv == 2 ]]; then
    use_nuxmv=1
fi

nuxmv_command=../nuxmv_commands/command_simulate
if [[ $use_msat == 1 ]]; then
    nuxmv_command=../nuxmv_commands/command_simulate_msat
fi

echo "running python"
python3 "${real_path}/${file_name}_runner.py" > "${real_path}/OUTPUT_PYTHON.txt"
if [[ $use_nuxmv == 1 ]]; then
    echo "running nuxmv"
    ../../nuXmv -source $nuxmv_command "${real_path}/${file_name}.smv" > "${real_path}/OUTPUT_NUXMV.txt"
    echo "running nuxmv_opt"
    ../../nuXmv -source $nuxmv_command "${real_path}/OPT_${file_name}.smv" > "${real_path}/OUTPUT_OPT_NUXMV.txt"
fi

if [[ $use_haskell == 1 ]]; then
    echo "running haskell"
    cur_loc=$(pwd)
    cd $real_path
    cabal run -v0 > ./OUTPUT_HASKELL.txt
    cd $cur_loc
fi

if [[ $use_haskell == 1 ]]; then
    if [[ $use_nuxmv == 1 ]]; then
	python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_NUXMV.txt" "${real_path}/OUTPUT_OPT_NUXMV.txt" "${real_path}/OUTPUT_HASKELL.txt" >> "${path_name}/results/log.txt"
    else
	python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_HASKELL.txt" >> "${path_name}/results/log.txt"
    fi
else
    if [[ $use_nuxmv == 1 ]]; then
	python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_NUXMV.txt" "${real_path}/OUTPUT_OPT_NUXMV.txt" >> "${path_name}/results/log.txt"
    else
	python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" >> "${path_name}/results/log.txt"
    fi
fi
