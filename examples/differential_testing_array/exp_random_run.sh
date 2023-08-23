#!/bin/bash

to_gen=1000
use_haskell=1
use_nuxmv=1

if [ "$#" == 3 ]; then
    to_gen=$1
    use_haskell=$2
    use_nuxmv=$3
fi

path_name="."

mkdir $path_name/results
rm $path_name/results/log.txt
touch $path_name/results/log.txt

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./run_comparison.sh $path_name "t$val" $use_haskell $use_nuxmv
done
