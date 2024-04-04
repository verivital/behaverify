#!/bin/bash

for file_name in *.tree; do
    echo $file_name 
    base_file_name="${file_name%.tree}"
    echo "${base_file_name}.smv"
    python3 /home/serene/git_repos/behaverify/src/dsl_to_nuxmv.py /home/serene/git_repos/behaverify/metamodel/behaverify.tx "${file_name}" "${base_file_name}.smv" 
done
