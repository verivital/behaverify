#!/bin/bash

python3 ../src/$3/dsl_to_behaverify.py ../metamodel/behaverify.tx $1/$2.tree --output_file $1/smv/$3_$2.smv
