#!/bin/bash

USER=behaverify

command=$1
input=$2
output=$3

"/home/${USER}/nuXmv" --source "${command}" "${input}" > "${output}"
