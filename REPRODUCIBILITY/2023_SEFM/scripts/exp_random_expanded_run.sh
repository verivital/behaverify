#!/bin/bash

path_name="../examples/random_expanded"

to_gen=200

mkdir $path_name/results
rm $path_name/results/log.txt
touch $path_name/results/log.txt


root_name=("sel" "seq" "p_all" "p_one")
child=("f" "s" "r")

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./run_comparison.sh $path_name "t$val"
done
