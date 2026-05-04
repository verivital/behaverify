#!/bin/bash

python_command=python3
min_val=1
max_val=10
step_size=1

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

./make_folder_structure.sh BT2BIP
./make_folder_structure.sh BT2Fiacre
./make_folder_structure.sh MoVe4BT

path_name="../../examples/MoVe4BT"

$python_command "${path_name}/create_binary_tree.py" "${path_name}/tree" $min_val $max_val $step_size
$python_command "${path_name}/create_binary_tree_MoVe4BT_xml.py" "${path_name}/xml" $min_val $max_val $step_size

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "now on iteration: "
    echo $num
    ./make_full_opt_smv.sh $python_command "${path_name}" binary_tree_$num
done

path_name="../../examples/BT2BIP"
cp "${path_name}/MarsRover.tree" "${path_name}/tree/MarsRover_0.tree"
cp "${path_name}/TrainControl.tree" "${path_name}/tree/TrainControl_0.tree"
./make_full_opt_smv.sh $python_command "${path_name}" MarsRover_0
./make_full_opt_smv.sh $python_command "${path_name}" TrainControl_0

path_name="../../examples/BT2Fiacre"
cp "${path_name}/drone3_height.tree" "${path_name}/tree/drone3_0.tree" 
cp "${path_name}/drone3_nodes.tree" "${path_name}/tree/drone3_1.tree" 
cp "${path_name}/drone3.tree" "${path_name}/tree/drone3_2.tree" 
cp "${path_name}/droneNew_height.tree" "${path_name}/tree/drone3_3.tree" 
cp "${path_name}/droneNew_nodes.tree" "${path_name}/tree/drone3_4.tree" 
cp "${path_name}/droneNew.tree" "${path_name}/tree/drone3_5.tree" 
cp "${path_name}/droneNew_interesting.tree" "${path_name}/tree/drone3_6.tree"
./make_full_opt_smv.sh $python_command "${path_name}" drone3_0
./make_full_opt_smv.sh $python_command "${path_name}" drone3_1
./make_full_opt_smv.sh $python_command "${path_name}" drone3_2
./make_full_opt_smv.sh $python_command "${path_name}" drone3_3
./make_full_opt_smv.sh $python_command "${path_name}" drone3_4
./make_full_opt_smv.sh $python_command "${path_name}" drone3_5
./make_full_opt_smv.sh $python_command "${path_name}" drone3_6
