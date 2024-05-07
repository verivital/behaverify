#!/bin/bash

cur_user=$(whoami)

input_name_only=$1

if test -e "/home/${cur_user}/user_files/${input_name_only}"; then
    rm -r "/home/${cur_user}/user_files/${input_name_only}"
fi

mkdir "/home/${cur_user}/user_files/${input_name_only}"
mkdir "/home/${cur_user}/user_files/${input_name_only}/app"
mkdir "/home/${cur_user}/user_files/${input_name_only}/output"
