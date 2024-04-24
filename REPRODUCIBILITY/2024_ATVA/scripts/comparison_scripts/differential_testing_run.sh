#!/bin/bash

path_name="../../examples/differential_testing/array"
to_gen=1000
use_haskell=1
use_nuxmv=1
use_msat=1 #1 means yes, else no. If no, uses go.

if [[ $# -ge 5 ]]; then
    path_name=$1
    to_gen=$2
    use_haskell=$3
    use_nuxmv=$4
    use_msat=$5
fi


if test -f "${path_name}/results"; then
    rm "${path_name}/results"
fi

if test -d "${path_name}/results"; then
    rm  -r "${path_name}/results"
fi

mkdir $path_name/results
touch $path_name/results/log.txt

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./run_comparison.sh $path_name "t${val}" $use_haskell $use_nuxmv $use_msat
done
