#!/bin/bash


echo "states"
./run_states.sh $1 $2 $3
echo "states_silent"
./run_states_silent.sh $1 $2 $3
echo "model"
./run_model.sh $1 $2 $3
#echo "ctl_silent"
#./run_ctl_silent.sh $1 $2 $3
#echo "ctl"
#./run_ctl.sh $1 $2 $3
echo "ltl_silent"
./run_ltl_silent.sh $1 $2 $3
echo "ltl"
./run_ltl.sh $1 $2 $3
