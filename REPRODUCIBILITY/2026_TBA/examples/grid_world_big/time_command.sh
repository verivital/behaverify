#!/bin/bash

py=$1

echo "${py} ../../src/dsl_to_nuxmv.py ../../metamodel/behaverify.tx ./grid_world_big.tree ./smv/grid_world_big.smv --no_checks --recursion_limit 10000" > command.sh

{ time ./command.sh ; } 2> "./results/timing_grid_world_big.txt"
