#!/bin/bash

for tree_file in tree/*; do
    echo "${tree_file}"
    no_ext="${tree_file%.tree}"
    no_path="${no_ext##*/}"
    echo "${no_path}"
    python3 ../../../src/dsl_to_nuxmv.py ../../../metamodel/behaverify.tx "${tree_file}" "./smv/${no_path}.smv"
done
