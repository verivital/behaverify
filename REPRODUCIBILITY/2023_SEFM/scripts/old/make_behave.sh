#!/bin/bash

python3 ../../../src/dsl_to_behaverify.py ../../../metamodel/behaverify.tx $1/$2.tree  --output_file $1/behave/$2.behave
