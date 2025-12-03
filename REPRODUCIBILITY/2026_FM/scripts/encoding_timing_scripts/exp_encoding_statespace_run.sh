#!/bin/bash

min_val=1
max_val=10
step_size=1
timeout_val="30s"  # Default 30s timeout for quick runs (use 5m for paper results)

if [[ $# -ge 3 ]]; then
    min_val=$1
    max_val=$2
    step_size=$3
fi

if [[ $# -ge 4 ]]; then
    timeout_val=$4
fi

path_name="../../examples/EncodingComparison"

# Clear previous results
> "${path_name}/States-Fastforwarding-Concise"
> "${path_name}/States-Naive-Concise"

echo "Using timeout: ${timeout_val}"
echo "Collecting state space information..."

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "Processing binary_tree_$num..."

    # Run state space computation for fastforwarding encoding
    echo "  Fastforwarding..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_states "${path_name}/smv_fastforwarding/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/STATES_FF_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/States-Fastforwarding-Concise"
    else
        # Extract reachable states count from output
        # Format is: "reachable states: 9 (2^3.16993) out of 24 (2^4.58496)"
        grep -oP 'reachable states: \K\d+' "${path_name}/results/STATES_FF_binary_tree_${num}.txt" | tail -1 >> "${path_name}/States-Fastforwarding-Concise"
    fi

    # Run state space computation for naive encoding
    echo "  Naive..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_states "${path_name}/smv_naive/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/STATES_NAIVE_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/States-Naive-Concise"
    else
        # Extract reachable states count from output
        grep -oP 'reachable states: \K\d+' "${path_name}/results/STATES_NAIVE_binary_tree_${num}.txt" | tail -1 >> "${path_name}/States-Naive-Concise"
    fi
done

echo ""
echo "State space computation complete. Results in:"
echo "  ${path_name}/States-Fastforwarding-Concise"
echo "  ${path_name}/States-Naive-Concise"
