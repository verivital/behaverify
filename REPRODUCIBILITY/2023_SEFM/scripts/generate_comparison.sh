#!/bin/bash

all_args=( "$@" )
# echo "${all_args[*]}"
path_name="${all_args[0]}"
file_name="${all_args[1]}"

mkdir $path_name/gen_files
mkdir $path_name/gen_files/$file_name

python3 ../src/norm/dsl_to_behaverify.py ../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree --output_file $path_name/gen_files/$file_name/$file_name.smv --do_not_trim
python3 ../src/norm/dsl_to_pytree.py ../metamodel/behaverify.tx $path_name/gen_files/$file_name.tree $path_name/gen_files/$file_name/ $file_name --max_iter 10 --serene_print
