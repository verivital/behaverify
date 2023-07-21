#!/bin/bash

to_gen=1000
min_val=1
max_val=15
use_haskell=1

if [ "$#" -ge 3 ]; then
    to_gen=$1
    min_val=$2
    max_val=$3
    no_haskell=$4
    if [[ "$no_haskell" == "no_haskell" ]]; then
	use_haskell=0
    fi
fi

path_name="../../examples/random_haskell"

mkdir $path_name/gen_files

python3 $path_name/gen_all.py $path_name/gen_files $to_gen $min_val $max_val

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./generate_comparison.sh $path_name "t$val" $use_haskell
    # 1 means use haskell
done
