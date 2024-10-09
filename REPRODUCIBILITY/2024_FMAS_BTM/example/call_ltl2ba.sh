#!/bin/bash

formula=$1
output=$2

$HOME/ltl2ba/ltl2ba -f "${formula}" > "${output}"
