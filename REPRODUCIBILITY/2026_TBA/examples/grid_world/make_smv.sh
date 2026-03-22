#!/bin/bash

tree_dir="./tree"
output_dir="./smv"
python=$1

mkdir -p "$output_dir"

for file in "$tree_dir"/*; do
    base_name=$(basename "$file")
    split_name="${base_name%%.*}"
    echo $file
    echo "${output_dir}/${split_name}.smv"
    $python ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx $file "${output_dir}/${split_name}.smv" --no_checks --recursion_limit 10000
done
