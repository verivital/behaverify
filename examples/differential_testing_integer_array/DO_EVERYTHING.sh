#!/bin/bash
rm -r ./gen_files
rm -r ./results
./exp_random_create.sh $1 2 5 $2 $3
./exp_random_run.sh $1 $2 $3
