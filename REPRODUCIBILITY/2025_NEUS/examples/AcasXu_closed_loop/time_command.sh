#!/bin/bash
py=$1
"${py}" handle_360.py

echo "${py} ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx ./tree/acasxu_360.tree ./smv/acasxu_360.smv --no_checks --recursion_limit 10000" > command.sh

{ time ./command.sh ; } 2> "./results/timing_acasxu_360.txt"
