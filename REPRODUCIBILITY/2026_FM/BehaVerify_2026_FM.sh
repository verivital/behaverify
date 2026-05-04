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

# Figure 1: DrunkenDrone BT diagram (Section 2)
#
# Generates the LaTeX/TikZ source used for Figure 1.
# Output: examples/DrunkenDrone/LaTeX/DrunkenDrone.tex

cd "${this_script_location}/scripts/build_scripts"
./make_folder_structure.sh DrunkenDrone

cd "${this_script_location}"
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/DrunkenDrone/DrunkenDrone.tree \
    ./examples/DrunkenDrone/LaTeX/DrunkenDrone.tex \
    --on_sides


# Table 2: Fastforwarding vs. Naive encoding ablation (Section 4.1)
#
# Generates binary trees at depths N=1–10, encodes them in both
# fastforwarding and naive nuXmv encodings, and runs CTL/LTL
# verification and state-space counting for each.
# Output: examples/EncodingComparison/results/

encoding_comparison_min=1
encoding_comparison_max=10
encoding_comparison_step=1

cd "${this_script_location}/scripts/build_scripts"
./exp_encoding_comparison_create.sh $python_behaverify $encoding_comparison_min $encoding_comparison_max $encoding_comparison_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_encoding_comparison_run.sh $encoding_comparison_min $encoding_comparison_max $encoding_comparison_step

# Table 3: BT2Fiacre drone comparison (Section 4.2)
# Section 4.3: BT2BIP MarsRover and TrainControl
#
# Generates SMV models and runs nuXmv verification for:
#   - drone3 and droneNew  (Table 3, BT2Fiacre comparison)
#   - MarsRover and TrainControl  (Section 4.3, BT2BIP comparison)
# Also generates LaTeX diagrams for all four trees.
# Output: examples/BT2Fiacre/results/, examples/BT2BIP/results/

tool_comparison_min=1
tool_comparison_max=10
tool_comparison_step=1

cd "${this_script_location}/scripts/build_scripts"
./exp_tool_comparisons_2026_FM_create.sh $python_behaverify $tool_comparison_min $tool_comparison_max $tool_comparison_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_tool_comparisons_2026_FM_run.sh $tool_comparison_min $tool_comparison_max $tool_comparison_step

cd "${this_script_location}"
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/BT2Fiacre/drone3.tree \
    ./examples/BT2Fiacre/LaTeX/drone3.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/BT2Fiacre/droneNew.tree \
    ./examples/BT2Fiacre/LaTeX/droneNew.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/BT2BIP/MarsRover.tree \
    ./examples/BT2BIP/LaTeX/MarsRover.tex
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/BT2BIP/TrainControl.tree \
    ./examples/BT2BIP/LaTeX/TrainControl.tex

# Section 4.2 footnote: Battery-invariant counterexample trace
#
# Visualizes the nuXmv counterexample for the battery-priority
# invariant on drone3 as a sequence of images.
# Depends on: Table 3 run having produced INVAR_full_opt_drone3_2.txt
# Output: examples/BT2Fiacre/processed_data/0_0.png, 0_1.png, 0_2.png

$python_behaverify ./src/counter_trace.py ./metamodel/behaverify.tx \
    ./examples/BT2Fiacre/drone3.tree \
    ./examples/BT2Fiacre/results/INVAR_full_opt_drone3_2.txt \
    ./examples/BT2Fiacre/processed_data

# ============================================================
# NSBT repository example — Neuro-Symbolic BT (Section 4 intro)
# ============================================================
# Verifies the drone-with-obstacles example using two trained networks
# (1.0 and 0.9995 accuracy) via INVAR and CTL specifications.
# Also generates a LaTeX diagram for the 1.0-accuracy tree.
# Output: examples/NetworkExample/results/

network_min=0
network_max=1
network_step=1

cd "${this_script_location}/scripts/build_scripts"
./exp_network_example_create.sh $python_behaverify $network_min $network_max $network_step
cd "${this_script_location}/scripts/encoding_timing_scripts"
./exp_network_example_run.sh $network_min $network_max $network_step

cd "${this_script_location}"
$python_behaverify ./src/dsl_to_latex.py ./metamodel/behaverify.tx \
    ./examples/NetworkExample/using1000.tree \
    ./examples/NetworkExample/LaTeX/using1000.tex

cd $start_location
