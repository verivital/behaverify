#!/bin/bash

num=$1

~/nuXmv -source command_counterexample "ANSR_ONNX_${num}cd.smv" > "counterexample_${num}cd.txt"
