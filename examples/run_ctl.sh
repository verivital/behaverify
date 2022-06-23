#!/bin/bash

echo $1 $2 $3
~/nuXmv -source command_ctl $1/$2/$3.smv > ./results/$1/$2-CTL_$3.txt
