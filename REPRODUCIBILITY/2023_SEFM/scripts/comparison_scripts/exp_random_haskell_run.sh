#!/bin/bash

to_gen=1000
use_haskell=1

if [ "$#" -ge 1 ]; then
    to_gen=$1
    no_haskell=$2
    if [[ "$no_haskell" == "no_haskell" ]]; then
	use_haskell=0
    fi
fi

path_name="../../examples/random_haskell"

mkdir $path_name/results
rm $path_name/results/log.txt
touch $path_name/results/log.txt

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./run_comparison.sh $path_name "t$val" $use_haskell
    # 0 means don't use haskell
done
