#!/bin/bash

echo "running for:"
echo $1 $2 $3

echo "ctl"
#./test_ctl.sh $1 $2 $3
timeout 3m ./test_ctl_silent.sh $1 $2 $3
echo "ltl"
#./test_ltl.sh $1 $2 $3
timeout 3m ./test_ltl_silent.sh $1 $2 $3
echo "states"
timeout 3m ./test_model.sh $1 $2 $3
timeout 3m ./test_states.sh $1 $2 $3
timeout 3m ./test_states_silent.sh $1 $2 $3
