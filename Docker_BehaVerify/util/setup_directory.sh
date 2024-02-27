#!/bin/bash

USER=behaverify

input_name_only=$1

if test -e "/home/${USER}/user_files/${input_name_only}"; then
    rm -r "/home/${USER}/user_files/${input_name_only}"
fi

mkdir "/home/${USER}/user_files/${input_name_only}"
mkdir "/home/${USER}/user_files/${input_name_only}/app"
mkdir "/home/${USER}/user_files/${input_name_only}/output"
