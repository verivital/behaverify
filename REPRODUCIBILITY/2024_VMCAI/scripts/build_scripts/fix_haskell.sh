#!/bin/bash

path_name=$1
file_name=$2

cat ../cabal_template_files/template_part1.cabal > "${path_name}/${file_name}.cabal"
echo "name:  ${file_name}" >> "${path_name}/${file_name}.cabal"
cat ../cabal_template_files/template_part2.cabal >> "${path_name}/${file_name}.cabal"
echo "${file_name^^}" >> "${path_name}/${file_name}.cabal"
cat ../cabal_template_files/template_part3.cabal >> "${path_name}/${file_name}.cabal"
