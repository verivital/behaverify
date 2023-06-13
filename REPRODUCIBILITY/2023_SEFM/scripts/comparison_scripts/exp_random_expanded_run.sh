#!/bin/bash

to_gen=1000

if [ "$#" == 1 ]; then
    to_gen=$1
fi

path_name="../../examples/random_expanded"

mkdir $path_name/results
rm $path_name/results/log.txt
touch $path_name/results/log.txt

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./run_comparison.sh $path_name "t$val" 0
    # 0 means don't use haskell
done
