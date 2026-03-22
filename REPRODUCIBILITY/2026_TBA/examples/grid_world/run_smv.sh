#!/bin/bash

MAX_TIME=1000
network=$1
command=$2
thing=$3
middle="_1000__6_18_0__0"
end="0_1.smv"

res="0_1.txt"
for num in {10..30..5}; do
    name="./smv/${network}${middle}${num}${end}"
    echo "$name  $command"
    nres="./results/${thing}_${network}${middle}${num}${res}"
    echo "$name  $command  $nres"
    timeout $MAX_TIME $command $name > $nres
    if [[ $? -eq 124 ]]; then
	exit 1
    fi
done

