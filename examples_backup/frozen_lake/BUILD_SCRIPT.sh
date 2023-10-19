#!/bin/bash

dots="../../../../"
file_name=$1
rm -r "$file_name"
mkdir "$file_name"
python3 "$dots"src/dsl_to_behaverify.py "$dots"metamodel/behaverify.tx "$file_name".tree --output_file ./"$file_name"/"$file_name.smv"
python3 "$dots"src/dsl_to_pytree.py "$dots"metamodel/behaverify.tx "$file_name".tree ./"$file_name"/ "$file_name" --max_iter 5
