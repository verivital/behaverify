#!/bin/bash

memtime ~/nuXmv -source command_states $1/$2 > $1/results/$2_states.txt
memtime ~/nuXmv -source command_ltl $1/$2 > $1/results/$2_ltl_full_suite.txt
