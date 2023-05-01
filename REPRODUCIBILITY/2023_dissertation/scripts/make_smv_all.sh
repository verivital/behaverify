#!/bin/bash

encodings=("aut_" "aut_s_" "depth_" "" "func_" "no_internal_" "s_var_")
#encodings=("")

for encoding in "${encodings[@]}"; do
    ./make_smv.sh $1 $2 $encoding
done

