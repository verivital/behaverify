#!/bin/bash

#1-> python, 2 -> path, 3-> file_name

python_command=$1
path_name=$2
file_name=$3


$python_command ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" "${path_name}/smv/no_opt_${file_name}.smv" --keep_stage_0 --keep_last_stage --recursion_limit 5000
$python_command ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" "${path_name}/smv/last_opt_${file_name}.smv" --keep_stage_0 --recursion_limit 5000
$python_command ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" "${path_name}/smv/first_opt_${file_name}.smv" --keep_last_stage --recursion_limit 5000
$python_command ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx "${path_name}/tree/${file_name}.tree" "${path_name}/smv/full_opt_${file_name}.smv" --recursion_limit 5000
