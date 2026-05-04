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
> "${path_name}/CTL-Fastforwarding-Concise"
> "${path_name}/CTL-Naive-Concise"
> "${path_name}/LTL-Fastforwarding-Concise"
> "${path_name}/LTL-Naive-Concise"

echo "Using timeout: ${timeout_val}"

for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "Running verification for binary_tree_$num..."

    # Run CTL verification for fastforwarding encoding
    echo "  CTL Fastforwarding..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_ctl_silent "${path_name}/smv_fastforwarding/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/CTL_FF_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/CTL-Fastforwarding-Concise"
    else
        grep -oP 'elapse: \K[\d.]+(?= seconds)' "${path_name}/results/CTL_FF_binary_tree_${num}.txt" | tail -1 >> "${path_name}/CTL-Fastforwarding-Concise"
    fi

    # Run CTL verification for naive encoding
    echo "  CTL Naive..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_ctl_silent "${path_name}/smv_naive/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/CTL_NAIVE_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/CTL-Naive-Concise"
    else
        grep -oP 'elapse: \K[\d.]+(?= seconds)' "${path_name}/results/CTL_NAIVE_binary_tree_${num}.txt" | tail -1 >> "${path_name}/CTL-Naive-Concise"
    fi

    # Run LTL verification for fastforwarding encoding
    echo "  LTL Fastforwarding..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_ltl_silent "${path_name}/smv_fastforwarding/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/LTL_FF_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/LTL-Fastforwarding-Concise"
    else
        grep -oP 'elapse: \K[\d.]+(?= seconds)' "${path_name}/results/LTL_FF_binary_tree_${num}.txt" | tail -1 >> "${path_name}/LTL-Fastforwarding-Concise"
    fi

    # Run LTL verification for naive encoding
    echo "  LTL Naive..."
    timeout ${timeout_val} ../../nuXmv -source ../nuxmv_commands/command_ltl_silent "${path_name}/smv_naive/nuxmv/binary_tree_${num}.smv" > "${path_name}/results/LTL_NAIVE_binary_tree_${num}.txt" 2>&1
    if [[ $? -eq 124 ]]; then
        echo "TIMEOUT" >> "${path_name}/LTL-Naive-Concise"
    else
        grep -oP 'elapse: \K[\d.]+(?= seconds)' "${path_name}/results/LTL_NAIVE_binary_tree_${num}.txt" | tail -1 >> "${path_name}/LTL-Naive-Concise"
    fi
done

echo ""
echo "Timing complete. Results in:"
echo "  ${path_name}/CTL-Fastforwarding-Concise"
echo "  ${path_name}/CTL-Naive-Concise"
echo "  ${path_name}/LTL-Fastforwarding-Concise"
echo "  ${path_name}/LTL-Naive-Concise"
