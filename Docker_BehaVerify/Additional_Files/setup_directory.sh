#!/bin/bash

input_name_only=$1

if test -e "/home/behaverify/${input_name_only}"; then
    rm -r "/home/behaverify/${input_name_only}"
fi

mkdir "/home/behaverify/${input_name_only}"
mkdir "/home/behaverify/${input_name_only}/app"
