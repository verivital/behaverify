#!/bin/bash

user=behaverify

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


if ! test -d "${output_location}"; then
    echo "Output Location needs to be a directory. ${output_location} is not a directory. Exiting"
    exit 3
fi
if ! [[ "${output_location: -1}" != "/" ]]; then
    output_location="${output_location}/"
fi


if [[ "${command}" == "nuXmv" ]]; then
    echo "generating nuXmv model"
    command="dsl_to_nuxmv"
    command_flags="/home/${user}/${input_name_only}/app/${input_name_only}.smv"
elif [[ "${command}" == "Python" ]]; then
    echo "generating Python code"
    command="dsl_to_python"
    command_flags="/home/${user}/${input_name_only}/app/ ${input_name_only}"
elif [[ "${command}" == "Haskell" ]]; then
    echo "generating Haskell code"
    command="dsl_to_haskell"
    command_flags="/home/${user}/${input_name_only}/ ${input_name_only}"
else
    echo "unknown command. Exiting"
    exit 4
fi

command_args=($command_flags)
echo "/home/${user}/${input_name_only}/${input_name}"

docker start behaverify
docker exec behaverify "/home/${user}/behaverify/Docker_BehaVerify/Additional_Files/setup_directory.sh" "${input_name_only}"
docker cp "${input_file}" "behaverify:/home/${user}/${input_name_only}/${input_name}"
if [[ -n "${network_folder}" ]]; then
    docker cp "${network_folder}" "behaverify:/home/${user}/${input_name_only}/${network_folder_name}"
fi
if [[ -z $user_flags ]]; then
    docker exec behaverify "/home/${user}/behaverify_venv/bin/python3" "/home/${user}/behaverify/src/${command}.py" "/home/${user}/behaverify/metamodel/behaverify.tx" "/home/${user}/${input_name_only}/${input_name}" "${command_args[@]}"
fi
if [[ -n $user_flags ]]; then
    docker exec behaverify "/home/${user}/behaverify_venv/bin/python3" "/home/${user}/behaverify/src/${command}.py" "/home/${user}/behaverify/metamodel/behaverify.tx" "/home/${user}/${input_name_only}/${input_name}" "${command_args[@]}" "${user_args[@]}"
fi
docker cp "behaverify:/home/${user}/${input_name_only}" "${output_location}${input_name_only}"
docker stop behaverify
