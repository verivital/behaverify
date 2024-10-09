#!/bin/bash

if [ -f "./extra_files/ignore" ]; then
    rm -rf "./extra_files/ignore"
fi
mkdir "./extra_files/ignore"

categories=("./dense_fixed" "./sparse_random")
for category in "${categories[@]}"; do
    if [ -f "$category" ]; then
	rm -rf "$category"
    fi
    mkdir "$category"
done

