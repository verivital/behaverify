#!/bin/bash

USER=behaverify

input=$1
output=$2

"/home/${USER}/behaverify_venv/bin/python3" "${input}" > "${output}"
