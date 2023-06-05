#!/bin/bash


file_name=$1
mkdir "$file_name"
python3 ../../src/dsl_to_behaverify.py ../../metamodel/behaverify.tx "$file_name".tree --output_file ./"$file_name"/"$file_name.smv"
python3 ../../src/dsl_to_pytree.py ../../metamodel/behaverify.tx "$file_name".tree ./"$file_name"/ "$file_name"
