#!/bin/bash

# 1 -> path, 2-> file_name, 3 -> encoding
path_name=$1
file_name=$2
encoding=$3

if [[ "$encoding" == "norm" ]]; then
    python3 "../../src/${encoding}/dsl_to_behaverify.py" "../../metamodel/behaverify.tx" "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/${encoding}_${file_name}.smv" --keep_last_stage
else
    python3 "../../src/${encoding}/dsl_to_behaverify.py" "../../metamodel/behaverify.tx" "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/${encoding}_${file_name}.smv"
fi
