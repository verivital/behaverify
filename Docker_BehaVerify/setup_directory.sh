#!/bin/bash

input_name_only=$1

if test -e "/home/user/${input_name_only}"; then
    rm -r "/home/user/${input_name_only}"
fi

mkdir "/home/user/${input_name_only}"
mkdir "/home/user/${input_name_only}/app"
