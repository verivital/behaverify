#!/bin/bash

python3 ../../../src/aut_dsl_to_behaverify.py ../../../metamodel/behaverify.tx $1/$2.tree --output_file $1/behave/aut_$2.behave
