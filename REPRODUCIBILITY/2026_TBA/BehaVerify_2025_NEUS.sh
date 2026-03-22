#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

this_script_location_arg=$1
python_behaverify=python3
start_location=$(pwd)

if [[ $# -ge 2 ]]; then
    python_behaverify=$2
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

cd "${this_script_location}/examples"
./clean_all.sh

cd "${this_script_location}/examples/grid_world"
./make_tree.sh
./time_make_smv.sh $python_behaverify
./run_smv_all.sh

cp obstacles_6_18_0.txt ./images/obstacles_6_18_0.txt
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/0995__6_18_0__200_1.onnx 4 5 7 7
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/0995__6_18_0__200_1.onnx 4 4 7 7
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/0996__6_18_0__200_1.onnx 4 5 7 7
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/0996__6_18_0__200_1.onnx 4 4 7 7
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/1000__6_18_0__0200_1.onnx 4 5 7 7
$python_behaverify ../draw_network.py ./images/obstacles_6_18_0.txt ./networks/1000__6_18_0__0200_1.onnx 4 4 7 7

../../nuXmv -source ../../scripts/nuxmv_commands/command_invar ./smv/table_0995__6_18_0__200_1.smv > ./results/counter_invar.txt
../../nuXmv -source ../../scripts/nuxmv_commands/command_ctl ./smv/table_0995__6_18_0__200_1.smv > ./results/counter_ctl.txt
mkdir ./images/counter_invar
$python_behaverify ../parse_SIMPLE_nuxmv_output_stage_LAST.py ./results/counter_invar.txt ./images/counter_invar/counter_invar 7 7
mkdir ./images/counter_ctl
$python_behaverify ../parse_SIMPLE_nuxmv_output_stage_LAST.py ./results/counter_ctl.txt ./images/counter_ctl/counter_ctl 7 7


cd "${this_script_location}/examples/grid_world_big"
./time_command.sh $python_behaverify
timeout 10000 ../../nuXmv -source ../../scripts/nuxmv_commands/command_all_invar ./smv/grid_world_big.smv > ./results/invar.txt

cd "${this_script_location}/examples/AcasXu"
./time_command.sh $python_behaverify
ulimit -s unlimited;
echo "Running ACAS Xu 1"
timeout 10000 ../../nuXmv -source ../../scripts/nuxmv_commands/command_all_invar  ./smv/acasxu_SINGLE.smv > ./results/invar_acasxu_SINGLE.txt
echo "Running ACAS Xu 2"
timeout 10000 ../../nuXmv -source ../../scripts/nuxmv_commands/command_all_invar  ./smv/acasxu_SINGLE_2.smv > ./results/invar_acasxu_SINGLE_2.txt
echo "Running ACAS Xu 3"
timeout 10000 ../../nuXmv -source ../../scripts/nuxmv_commands/command_all_invar  ./smv/acasxu_SINGLE_3.smv > ./results/invar_acasxu_SINGLE_3.txt

cd "${this_script_location}/examples/AcasXu_closed_loop"
./time_command.sh $python_behaverify
echo "Running ACAS Xu Loop"
timeout 10000 ../../nuXmv -source ../../scripts/nuxmv_commands/command_all_invar ./smv/acasxu_360.smv > ./results/acasxu_360.txt

cd $start_location
