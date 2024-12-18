#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

this_script_location_arg=$1
python_loc=python3
start_location=$(pwd)

if [[ $# -ge 2 ]]; then
    python_loc=$2
fi


cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh

cd "${this_script_location}"
"${python_loc}" ./src/dsl_to_nuxmv.py ./metamodel/behaverify.tx ./examples/small/table.tree ./examples/small/smv/table.smv --recursion_limit 50000 --no_checks
"${python_loc}" ./src/dsl_to_nuxmv.py ./metamodel/behaverify.tx ./examples/small/fixed.tree ./examples/small/smv/fixed.smv --recursion_limit 50000 --no_checks
"${python_loc}" ./src/dsl_to_nuxmv.py ./metamodel/behaverify.tx ./examples/small/float.tree ./examples/small/smv/float.smv --recursion_limit 50000 --no_checks
"${python_loc}" ./src/dsl_to_nuxmv.py ./metamodel/behaverify.tx ./examples/big/pre_table.tree ./examples/big/smv/pre_table.smv --recursion_limit 50000 --no_checks

echo "------------------------------------"
echo "finished making smv"
echo "------------------------------------"

ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_simulate_random_1 ./examples/small/smv/table.smv > ./examples/small/results/table_simulate.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_simulate_random_1 ./examples/small/smv/fixed.smv > ./examples/small/results/fixed_simulate.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_simulate_random_1 ./examples/small/smv/float.smv > ./examples/small/results/float_simulate.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_simulate_random_2 ./examples/big/smv/pre_table.smv > ./examples/big/results/pre_table_simulate.txt

echo "------------------------------------"
echo "finished simulations"
echo "------------------------------------"

ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar ./examples/small/smv/table.smv > ./examples/small/results/table_imvar.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar ./examples/small/smv/fixed.smv > ./examples/small/results/fixed_invar.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar ./examples/small/smv/float.smv > ./examples/small/results/float_invar.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar ./examples/big/smv/pre_table.smv > ./examples/big/results/pre_table_invar.txt

echo "------------------------------------"
echo "finished invar checking"
echo "------------------------------------"

ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar_silent ./examples/small/smv/table.smv > ./examples/small/results/table_invar_silent.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar_silent ./examples/small/smv/fixed.smv > ./examples/small/results/fixed_invar_silent.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar_silent ./examples/small/smv/float.smv > ./examples/small/results/float_invar_silent.txt
ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_invar_silent ./examples/big/smv/pre_table.smv > ./examples/big/results/pre_table_invar_silent.txt

echo "------------------------------------"
echo "finished invar timing"
echo "------------------------------------"

ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl ./examples/small/smv/table.smv > ./examples/small/results/table_ctl.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl ./examples/small/smv/fixed.smv > ./examples/small/results/fixed_ctl.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl ./examples/small/smv/float.smv > ./examples/small/results/float_ctl.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl ./examples/big/smv/pre_table.smv > ./examples/big/results/pre_table_ctl.txt

echo "------------------------------------"
echo "finished checking ctl"
echo "------------------------------------"

ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl_silent ./examples/small/smv/table.smv > ./examples/small/results/table_ctl_silent.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl_silent ./examples/small/smv/fixed.smv > ./examples/small/results/fixed_ctl_silent.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl_silent ./examples/small/smv/float.smv > ./examples/small/results/float_ctl_silent.txt
# ulimit -s unlimited; ./nuXmv -source ./scripts/nuxmv_commands/command_ctl_silent ./examples/big/smv/pre_table.smv > ./examples/big/results/pre_table_ctl_silent.txt

echo "------------------------------------"
echo "finished timing ctl"
echo "------------------------------------"

"${python_loc}" ./examples/parse_nuxmv_output_stage_1.py ./examples/small/results/table_simulate.txt ./examples/small/images/table 10 10
"${python_loc}" ./examples/parse_nuxmv_output_stage_1.py ./examples/small/results/fixed_simulate.txt ./examples/small/images/fixed 10 10
# "${python_loc}" ./examples/parse_nuxmv_output_stage_1.py ./examples/small/results/float_simulate.txt ./examples/small/images/float 10 10
"${python_loc}" ./examples/parse_nuxmv_output_stage_1.py ./examples/big/results/pre_table_simulate.txt ./examples/big/images/pre_table 50 50

echo "------------------------------------"
echo "finished making images"
echo "------------------------------------"




cd $start_location
