#!/bin/bash
num_gen=$1
use_haskell=$2
use_nuxmv=$3
rm -r ./gen_files
rm -r ./results
./exp_random_create.sh $num_gen 2 5 $use_haskell $use_nuxmv
./exp_random_run.sh $num_gen $use_haskell $use_nuxmv
