#!/bin/bash

path_name=$1
file_name=$2
use_haskell=$3  # 1 means yes, 0 means no.
real_path="${path_name}/gen_files/${file_name}"



python3 "${real_path}/${file_name}_runner.py" > "${real_path}/OUTPUT_PYTHON.txt"
../../nuXmv -source ../nuxmv_commands/command_simulate "${real_path}/${file_name}.smv" > "${real_path}/OUTPUT_NUXMV.txt"
../../nuXmv -source ../nuxmv_commands/command_simulate "${real_path}/OPT_${file_name}.smv" > "${real_path}/OUTPUT_OPT_NUXMV.txt"

if [[ $use_haskell == 1 ]]; then
    cur_loc=$(pwd)
    cd $real_path
    cabal run -v0 > ./OUTPUT_HASKELL.txt
    cd $cur_loc
    python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_NUXMV.txt" "${real_path}/OUTPUT_OPT_NUXMV.txt" "${real_path}/OUTPUT_HASKELL.txt" >> "${path_name}/results/log.txt"
else
    python3 compare.py "${file_name}" "${real_path}/OUTPUT_PYTHON.txt" "${real_path}/OUTPUT_NUXMV.txt" "${real_path}/OUTPUT_OPT_NUXMV.txt" >> "${path_name}/results/log.txt"
fi


