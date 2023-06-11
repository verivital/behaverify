#!/bin/bash

#./make_comparison_folder_structure.sh 3_node_no_var

path_name="../examples/random_expanded"

to_gen=5
min_val=2
max_val=15

mkdir $path_name/gen_files

python3 $path_name/gen_all.py $path_name/gen_files/ $to_gen $min_val $max_val

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./generate_comparison.sh $path_name "t$val"
done
