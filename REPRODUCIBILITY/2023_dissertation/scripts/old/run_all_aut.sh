#!/bin/bash

echo "running for:"
echo $1 $2

echo "ctl"
./run_ctl.sh $1 aut_$2
./run_ctl_silent.sh $1 aut_$2
echo "ltl"
./run_ltl.sh $1 aut_$2
./run_ltl_silent.sh $1 aut_$2
echo "states"
./run_model.sh $1 aut_$2
./run_states.sh $1 aut_$2
./run_states_silent.sh $1 aut_$2
