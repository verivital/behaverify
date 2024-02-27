#!/bin/bash

USER=behaverify


input_file=$1
input_name=$(basename "${input_file}")
input_name_only="${input_name%.*}"
network_folder=$2
output_location=$3
command=$4
command_2=$5
command_flags=""
user_flags=$6

if [[ $# -lt 5 ]]; then
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
    command_flags="/home/${USER}/user_files/${input_name_only}/app/${input_name_only}.smv"
elif [[ "${command}" == "Python" ]]; then
    echo "generating Python code"
    command="dsl_to_python"
    command_flags="/home/${USER}/user_files/${input_name_only}/app/ ${input_name_only}"
elif [[ "${command}" == "Haskell" ]]; then
    echo "generating Haskell code"
    command="dsl_to_haskell"
    command_flags="/home/${USER}/user_files/${input_name_only}/ ${input_name_only}"
else
    echo "unknown command. Exiting"
    exit 4
fi

if [[ "${commmand_2}" == "generate" ]]; then
    echo "generate selected!"
elif [[ "${commmand_2}" == "simulate" ]]; then
    echo "simulate selected! Please ensure you installed with the simulate option."
else
    if [[ "${command}" != "dsl_to_nuxmv" ]]; then
	echo "Command was not nuXmv, but did not select 'generate' or 'simulate'. Invalid configuration. Exiting."
	exit 5
    fi
    if [[ "${commmand_2}" == "ctl" ]]; then
	echo "ctl selected!"
    elif [[ "${commmand_2}" == "ltl" ]]; then
	echo "ltl selected!"
    elif [[ "${commmand_2}" == "invar" ]]; then
	echo "invar selected!"
    else
	echo "Second command was not 'generate', 'simulate', 'ctl', 'ltl', or 'invar'. Unrecognized option! Exiting."
	exit 6
    fi
fi

command_args=($command_flags)
echo "/home/${USER}/user_files/${input_name_only}/${input_name}"

docker start behaverify
docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/setup_directory.sh" "${input_name_only}"
docker cp "${input_file}" "behaverify:/home/${USER}/user_files/${input_name_only}/${input_name}"
if [[ -n "${network_folder}" ]]; then
    docker cp "${network_folder}" "behaverify:/home/${USER}/user_files/${input_name_only}/${network_folder_name}"
fi
if [[ -z $user_flags ]]; then
    docker exec behaverify "/home/${USER}/behaverify_venv/bin/python3" "/home/${USER}/behaverify/src/${command}.py" "/home/${USER}/behaverify/metamodel/behaverify.tx" "/home/${USER}/user_files/${input_name_only}/${input_name}" "${command_args[@]}"
fi
if [[ -n $user_flags ]]; then
    docker exec behaverify "/home/${USER}/behaverify_venv/bin/python3" "/home/${USER}/behaverify/src/${command}.py" "/home/${USER}/behaverify/metamodel/behaverify.tx" "/home/${USER}/user_files/${input_name_only}/${input_name}" "${command_args[@]}" "${user_args[@]}"
fi
if [[ "${commmand_2}" == "generate" ]]; then
    true
elif [[ "${commmand_2}" == "simulate" ]]; then
    if [[ "${command}" == "dsl_to_nuxmv" ]]; then
	echo "Attempting to simulate using nuXmv. Please ensure you added nuXmv."
	docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/run_nuxmv.sh" "/home/${USER}/behaverify/scripts/nuxmv_commands/command_simulate" "/home/${USER}/user_files/${input_name_only}/app/${input_name_only}.smv" "/home/${USER}/user_files/${input_name_only}/output/simulation.txt"
    elif [[ "${command}" == "dsl_to_python" ]]; then
	echo "Attempting to simulate using Python."
	docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/run_python.sh" "/home/${USER}/user_files/${input_name_only}/app/${input_name_only}_runner.py" "/home/${USER}/user_files/${input_name_only}/output/simulation.txt"
    else
	echo "Haskell simulation not yet implemented. Sorry."
    fi
else
    if [[ "${commmand_2}" == "ctl" ]]; then
	echo "Attempting to check CTL using nuXmv. Please ensure you added nuXmv."
	docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/run_nuxmv.sh" "/home/${USER}/behaverify/scripts/nuxmv_commands/command_ctl" "/home/${USER}/user_files/${input_name_only}/app/${input_name_only}.smv" "/home/${USER}/user_files/${input_name_only}/output/ctl_results.txt"
    elif [[ "${commmand_2}" == "ltl" ]]; then
	echo "Attempting to check LTL using nuXmv. Please ensure you added nuXmv."
	docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/run_nuxmv.sh" "/home/${USER}/behaverify/scripts/nuxmv_commands/command_ltl" "/home/${USER}/user_files/${input_name_only}/app/${input_name_only}.smv" "/home/${USER}/user_files/${input_name_only}/output/ctl_results.txt"
    elif [[ "${commmand_2}" == "invar" ]]; then
	echo "Attempting to check INVAR using nuXmv. Please ensure you added nuXmv."
	docker exec behaverify "/home/${USER}/behaverify/Docker_BehaVerify/tool/common/run_nuxmv.sh" "/home/${USER}/behaverify/scripts/nuxmv_commands/command_invar" "/home/${USER}/user_files/${input_name_only}/app/${input_name_only}.smv" "/home/${USER}/user_files/${input_name_only}/output/invar_results.txt"
    fi
fi
docker cp "behaverify:/home/${USER}/user_files/${input_name_only}" "${output_location}${input_name_only}"
docker stop behaverify
