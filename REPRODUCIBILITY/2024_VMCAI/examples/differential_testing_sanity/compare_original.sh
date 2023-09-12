#!/bin/bash

if test -e ./results_original/log.txt; then
    rm -r ./results_original/log.txt
fi

touch ./results_original/log.txt

for (( val=0; val<10; val++ )); do
    echo $val
    folder="./original/t${val}/"
    python3 ../../scripts/comparison_scripts/compare.py "t${val}" "${folder}OUTPUT_PYTHON.txt" "${folder}OUTPUT_NUXMV.txt" "${folder}OUTPUT_OPT_NUXMV.txt" "${folder}OUTPUT_HASKELL.txt" >> ./results_original/log.txt
done
