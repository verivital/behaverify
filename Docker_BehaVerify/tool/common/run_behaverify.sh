#!/bin/bash

USER=behaverify


input_file=$1
input_name=$(basename "${input_file}")
input_name_only="${input_name%.*}"
network_folder=$2
output_location=$3
command=$4
command_flags=""
user_flags=$5

if [[ $# -lt 4 ]]; then
    echo "At least four arguments are needed. Exiting"
    exit 1
fi
if [[ $# -eq 4 ]]; then
    user_flags=""
fi
user_args=($user_flags)

if ! test -f "${input_file}"; then
    echo "${input_file} is not a file. Exiting"
    exit 1
fi

if [[ "${network_folder}" == "-" ]]; then
    network_folder=""
fi
if [[ -n "${network_folder}" ]]; then
    if ! test -d "${network_folder}"; then
	echo "Network Folder must either be - or a directory. ${network_folder} is neither. Exiting"
	exit 2
    fi
    if ! [[ "${network_folder: -1}" != "/" ]]; then
	network_folder="${network_folder}/"
    fi
    network_folder_name=$(basename "${network_folder}")
fi


if ! [[ "${output_location: -1}" != "/" ]]; then
    output_location="${output_location}/"
fi
if test -e "${output_location}"; then
    rm -rf "${output_location}"
fi



if ! test -f "${input_file}"; then
    echo "${input_file} is not a file (after ${output_location} was cleared). Exiting"
    exit 1
fi

if [[ "${network_folder}" == "-" ]]; then
    network_folder=""
fi
if [[ -n "${network_folder}" ]]; then
    if ! test -d "${network_folder}"; then
	echo "Network Folder must either be - or a directory. ${network_folder} is neither (after ${output_location} was cleared). Exiting"
	exit 2
    fi
fi

mkdir "${output_location}"
mkdir "${output_location}/app"


if [[ "${command}" == "nuXmv" ]]; then
    echo "generating nuXmv model"
    command="dsl_to_nuxmv"
    command_flags="${output_location}/app/${input_name_only}.smv"
elif [[ "${command}" == "Python" ]]; then
    echo "generating Python code"
    command="dsl_to_python"
    command_flags="${output_location}/app/ ${input_name_only}"
elif [[ "${command}" == "Haskell" ]]; then
    echo "generating Haskell code"
    command="dsl_to_haskell"
    command_flags="${output_location}/ ${input_name_only}"
else
    echo "unknown command. Exiting"
    exit 4
fi

command_args=($command_flags)

if [[ -z $user_flags ]]; then
    "/home/${USER}/behaverify_venv/bin/python3" "/home/${USER}/behaverify/src/${command}.py" "/home/${USER}/behaverify/metamodel/behaverify.tx" "${input_file}" "${command_args[@]}"
fi
if [[ -n $user_flags ]]; then
    "/home/${USER}/behaverify_venv/bin/python3" "/home/${USER}/behaverify/src/${command}.py" "/home/${USER}/behaverify/metamodel/behaverify.tx" "/home/${USER}/${input_name_only}/${input_name}" "${command_args[@]}" "${user_args[@]}"
fi
