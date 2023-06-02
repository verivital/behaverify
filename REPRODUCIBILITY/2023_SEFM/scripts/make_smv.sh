#!/bin/bash

python3 ../../../src/$3behaverify_to_smv.py $1/behave/$3$2.behave --output_file $1/smv/$3$2.smv
