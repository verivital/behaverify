#!/bin/bash

memtime ~/nuXmv -source command_states $1 > ./results/$1_states.txt
memtime ~/nuXmv -source command_ltl $1 > ./results/$1_ltl_full_suite.txt
