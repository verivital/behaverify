#!/bin/bash

python3 ../../../src/behaverify_to_smv.py $1/behave/$2.behave --output_file $1/smv/$2.smv
