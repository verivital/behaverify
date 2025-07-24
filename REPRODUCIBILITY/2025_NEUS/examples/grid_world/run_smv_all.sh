#!/bin/bash

networks=( 'fixed_100_35' 'fixed_140_48' 'float_140' 'table' )
# networks=( 'fixed_100_35' )
commands=( 'command_all_invar' 'command_all_ctl' )

for network in "${networks[@]}"; do
    for command in "${commands[@]}"; do
	./run_smv.sh $network "/home/serena/Tools/nuXmv -source ../../scripts/nuxmv_commands/${command}" "${command}"
    done
done
