#!/bin/bash

this_script_location_arg=$1
start_location=$(pwd)

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi
use_haskell=1
to_gen=1
if [[ $# -ge 2 ]]; then
    use_haskell=$2
fi
if [[ $# -ge 3 ]]; then
    to_gen=$3
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)


cd "${this_script_location}/../build_scripts"
./differential_testing_create.sh "../../examples/differential_testing/array" $to_gen 2 5 $use_haskell 1
cd "${this_script_location}/../comparison_scripts"
./differential_testing_run.sh "../../examples/differential_testing/array" $to_gen $use_haskell 1 0


cd $start_location
