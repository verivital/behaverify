#!/bin/bash

# 1 -> path, 2-> file_name
path_name=$1
file_name=$2


python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/no_opt_${file_name}.smv" --keep_stage_0 --keep_last_stage
python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/last_opt_${file_name}.smv" --keep_stage_0
python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/first_opt_${file_name}.smv" --keep_last_stage
python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" --output_file "${path_name}/smv/full_opt_${file_name}.smv"
