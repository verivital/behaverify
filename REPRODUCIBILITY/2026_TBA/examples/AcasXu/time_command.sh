#!/bin/bash

py=$1
files=("acasxu_SINGLE" "acasxu_SINGLE_2" "acasxu_SINGLE_3")

for cur in "${files[@]}"; do
    echo "${py} ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx ${cur}.tree ./smv/${cur}.smv --no_checks --recursion_limit 10000" > command.sh

    { time ./command.sh ; } 2> "./results/timing_${cur}.txt"
done
