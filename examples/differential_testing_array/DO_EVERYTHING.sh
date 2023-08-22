#!/bin/bash
rm -r ./gen_files
rm -r ./results
./exp_random_haskell_create.sh $1 2 5
./exp_random_haskell_run.sh $1
