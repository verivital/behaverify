#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "at least one argument (script location) is required. Exiting"
    exit
fi

this_script_location_arg=$1
python_behaverify=python3
python_results=python3
start_location=$(pwd)

if [[ $# -ge 3 ]]; then
    python_behaverify=$2
    python_results=$3
fi

cd "${this_script_location_arg}"
this_script_location=$(pwd)

# cd "${this_script_location}/examples"
# ./clean_all.sh

binary_tree_min=1
binary_tree_max=10
binary_tree_step=1

cd "${this_script_location}/scripts/build_scripts"
./exp_tool_comparisons_2025_FMCAD_create.sh $python_behaverify $binary_tree_min $binary_tree_max $binary_tree_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_tool_comparisons_2025_FMCAD_run.sh $binary_tree_min $binary_tree_max $binary_tree_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_table.sh $python_results $binary_tree_min $binary_tree_max $binary_tree_step

network_min=0
network_max=1
network_step=1
cd "${this_script_location}/scripts/build_scripts"
./exp_network_example_create.sh $python_behaverify $network_min $network_max $network_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_network_example_run.sh $network_min $network_max $network_step
# cd "${this_script_location}/scripts/process_results_scripts"
# ./exp_binary_tree_table.sh $python_results $binary_tree_min $binary_tree_max $binary_tree_step

cd "${this_script_location}/scripts/build_scripts"
./make_folder_structure.sh DrunkenDrone

cd "${this_script_location}"

$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_BT2BIP/MarsRover.tree ./examples/2025_FMCAD_BT2BIP/LaTeX/MarsRover.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_BT2BIP/TrainControl.tree ./examples/2025_FMCAD_BT2BIP/LaTeX/TrainControl.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_BT2Fiacre/drone3.tree ./examples/2025_FMCAD_BT2Fiacre/LaTeX/drone3.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_BT2Fiacre/droneNew.tree ./examples/2025_FMCAD_BT2Fiacre/LaTeX/droneNew.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/DrunkenDrone/DrunkenDrone.tree ./examples/DrunkenDrone/LaTeX/DrunkenDrone.tex --on_sides
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_MoVe4BT/tree/binary_tree_2.tree ./examples/2025_FMCAD_MoVe4BT/LaTeX/binary_tree_2.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx ./examples/NetworkExample/using1000.tree ./examples/NetworkExample/LaTeX/using1000.tex

$python_behaverify ./src/counter_trace.py ./metamodel/behaverify.tx ./examples/2025_FMCAD_BT2Fiacre/drone3.tree ./examples/2025_FMCAD_BT2Fiacre/results/INVAR_full_opt_drone3_2.txt ./examples/2025_FMCAD_BT2Fiacre/processed_data


cd $start_location
