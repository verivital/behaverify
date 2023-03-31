#!/bin/bash

encodings=("" "aut_" "aut_s_" "func_")

for encoding in ${encodings[@]}; do
    ./make_behave.sh $1 $2 $encoding
done

