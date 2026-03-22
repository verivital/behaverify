#!/bin/bash

rm -r ../../examples/$1/smv
rm -r ../../examples/$1/results
rm -r ../../examples/$1/tree
rm -r ../../examples/$1/processed_data

mkdir ../../examples/$1/smv
mkdir ../../examples/$1/results
mkdir ../../examples/$1/tree
mkdir ../../examples/$1/processed_data
# mkdir ../../examples/$1/processed_data/all
# mkdir ../../examples/$1/processed_data/aut
# mkdir ../../examples/$1/processed_data/core
# mkdir ../../examples/$1/processed_data/func
# mkdir ../../examples/$1/processed_data/internal
