#!/bin/bash

python3 ../../../src/aut_behaverify_to_smv.py $1/behave/aut_$2.behave --output_file $1/smv/aut_$2.smv
