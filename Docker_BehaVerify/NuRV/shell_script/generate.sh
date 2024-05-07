#!/bin/bash

USER=NuRV
CONTAINER=nurv

model=$1
model_file=$(basename "${model}")
model_name="${model_file%.*}"

trace=$2
trace_file=$(basename "${trace}")
trace_name="${trace_file%.*}"

output_location=$3

if [[ $# -lt 3 ]]; then
    echo "At least three arguments are needed. Exiting"
    exit 1
fi

if ! test -f "${model}"; then
    echo "${model} is not a file. Exiting"
    exit 1
fi

if ! test -f "${trace}"; then
    echo "${trace} is not a file. Exiting"
    exit 2
fi

if ! test -d "${output_location}"; then
    echo "Output Location needs to be a directory. ${output_location} is not a directory. Exiting"
    exit 3
fi
if ! [[ "${output_location: -1}" != "/" ]]; then
    output_location="${output_location}/"
fi


docker start "${CONTAINER}"
#docker exec "${CONTAINER}" "touch /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "echo go > /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "echo build_monitor -n 0 >> /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "echo read_trace /home/${USER}/user_files/${trace_file} >> /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "echo verify_property -n 0 1 >> /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "echo quit >> /home/${USER}/user_files/command"
docker exec "${CONTAINER}" bash -c "rm /home/${USER}/user_files/${model_file}"
docker exec "${CONTAINER}" bash -c "rm /home/${USER}/user_files/${trace_file}"
docker cp "${model}" "${CONTAINER}:/home/${USER}/user_files/${model_file}"
docker cp "${trace}" "${CONTAINER}:/home/${USER}/user_files/${trace_file}"
docker exec "${CONTAINER}" bash -c "/home/${USER}/NuRV/NuRV -quiet -source /home/${USER}/user_files/command /home/${USER}/user_files/${model_file} > /home/${USER}/user_files/${trace_name}.txt" 
docker cp "${CONTAINER}:/home/${USER}/user_files/${trace_name}.txt" "${output_location}${trace_name}.txt"
docker stop behaverify
