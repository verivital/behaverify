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

result_loc=$python_loc

if [[ $# -ge 3 ]]; then
    result_loc=$3
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh

cd "${this_script_location}"
"${python_loc}" ./src/dsl_to_nuxmv.py ./metamodel/behaverify.tx ./examples/small/table.tree ./examples/small/smv/table.smv --recursion_limit 50000 --no_checks

./nuXmv -source ./scripts/nuxmv_commands/command_simulate ./examples/small/smv/table.smv > ./examples/small/results/table_simulate.txt

"${result_loc}" ./examples/parse_nuxmv_output_stage_1.py ./examples/small/results/table_simulate.txt ./examples/small/images/table 10 10


cd $start_location
