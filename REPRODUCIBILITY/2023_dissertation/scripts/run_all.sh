#!/bin/bash

encodings=("" "aut_" "aut_s_" "func_")
#encodings=("aut_s_")

for encoding in ${encodings[@]}; do
    ./run_encoding.sh $1 $2 $encoding
done
