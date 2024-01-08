#!/bin/bash

input_file=$1
input_name=$(basename "${input_file}")
input_name_only="${name%.*}"
output_location=$2
command=$3
command_flags=""
user_flags=$4

if ! test -d "${output_location}"; then
    echo "Output Location needs to be a directory. ${output_location} is not a directory. Exiting"
    exit 1
fi

if ! [[ "${output_location: -1}" != "/" ]]; then
    output_location="${output_location}/"
fi

if ! test -f "${input_file}"; then
    echo "${input_file} is not a file. Exiting"
    exit 2
fi

if [[ "${command}" == "nuXmv" ]]; then
    echo "generating nuXmv model"
    command="dsl_to_nuxmv"
    command_flags="/home/user/${input_name_only}/app/${input_name_only}.smv"
elif [[ "${command}" == "Python" ]]; then
    echo "generating Python code"
    mode="dsl_to_python"
    command_flags="/home/user/${input_name_only}/app/ ${input_name_only}"
elif [[ "${command}" == "Haskell" ]]; then
    echo "generating Haskell code"
    mode="dsl_to_haskell"
    command_flags="/home/user/${input_name_only}/ ${input_name_only}"
else
    echo "unknown command. Exiting"
    exit 3
fi


docker start behaverify
docker exec behaverify /home/user/behaverify/Docker_BehaVerify/setup_directory.sh "${input_name_only}"
docker cp "${input_file}" "behaverify:/home/user/${input_name_only}/${input_name}" 
docker exec behaverify python3 "home/user/behaverify/src/${command}.py" "/home/user/behaverify/metamodel/behaverify.tx" "/home/user/${input_name_only}/${input_name}" "${command_flags}" "${user_flags}"
docker cp "behaverify:/home/user/${input_name_only}" "${output_location}${input_name_only}"
docker stop behaverfiy
