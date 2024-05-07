#!/bin/bash

for smv_file in smv/*.smv; do
    echo "${smv_file}"
    no_ext="${smv_file%.smv}"
    no_path="${no_ext##*/}"
    echo "${no_path}"
    ~/nuXmv -source command_all "${smv_file}" > "${no_ext}_all.txt"
done
