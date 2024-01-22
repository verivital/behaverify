#!/bin/bash

mode="generate"
if [[ $# -eq 0 ]]; then
    echo "This script is being run with no arguments (which is fine). Installing generate only."
elif [[ $# -gt 1 ]]; then
    echo "This script takes either 0 or 1 arguments. Please try again."
    exit
elif [[ $# -eq 1 ]]; then
    mode=$1
    if [[ "${mode}" == "generate" ]]; then
	echo "This script is being run with the argument generate. Installing generate only."
    elif [[ "${mode}" == "full" ]]; then
	echo "This script is being run with the argument full. Performing Full Installation."
    else
	echo "This script takes either 0 or 1 arguments and it received 1 argument."
	echo "However, that argument must either be generate or full. Received: ${mode}"
	echo "Exiting"
	exit
    fi
fi


current_location=$(pwd)
if [[ "${mode}" == "generate" ]]; then
    cd "./Generation_Only"
elif [[ "${mode}" == "full" ]]; then
    echo "Just kidding. That's not supported yet. Exiting."
    exit
    # cd "./Full"
fi

./docker_build_script.sh
cd $current_location
./docker_behaverify_clone.sh
