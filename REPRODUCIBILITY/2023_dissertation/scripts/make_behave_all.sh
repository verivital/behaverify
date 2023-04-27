#!/bin/bash

encodings=("aut_" "aut_s_" "depth_" "" "func_" "no_internal_" "s_var_")
# encodings=("")

for encoding in "${encodings[@]}"; do
    echo $encoding
    ./make_behave.sh $1 $2 $encoding
done

