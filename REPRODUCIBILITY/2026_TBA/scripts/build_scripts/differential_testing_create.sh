#!/bin/bash

path_name="../../examples/differential_testing/array"
to_gen=1000
min_val=1
max_val=15
use_haskell=1
use_nuxmv=1

if [[ $# -ge 6 ]]; then
    path_name=$1
    to_gen=$2
    min_val=$3
    max_val=$4
    use_haskell=$5
    use_nuxmv=$6
fi


if test -f "${path_name}/gen_files"; then
    rm "${path_name}/gen_files"
fi

if test -d "${path_name}/gen_files"; then
    rm -r "${path_name}/gen_files"
fi

mkdir "${path_name}/gen_files"

python3 "${path_name}/gen_all.py" "${path_name}/gen_files" $to_gen $min_val $max_val

for (( val=0; val<$to_gen; val++ )); do
    echo $val
    ./generate_comparison.sh $path_name "t${val}" $use_haskell $use_nuxmv
done
