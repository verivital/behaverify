#!/bin/bash

python3 ../../../src/func_behaverify_to_smv.py $1/behave/$2.behave --output_file $1/smv/func_$2.smv
