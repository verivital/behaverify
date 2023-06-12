#!/bin/bash

#./make_comparison_folder_structure.sh 3_node_no_var

path_name="../../examples/random_expanded"

to_gen=1000
min_val=2
max_val=7

if [ "$#" == 3 ]; then
    to_gen=$1
    min_val=$2
    max_val=$3
fi

mkdir $path_name/gen_files

python3 $path_name/gen_all.py $path_name/gen_files $to_gen $min_val $max_val

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./generate_comparison.sh $path_name "t$val"
done
