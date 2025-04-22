#!/bin/bash

ulimit -s unlimited; ../../nuXmv -source ../nuxmv_commands/command_ctl $1/smv/$3_$2.smv > $1/results/CTL_$3_$2.txt
