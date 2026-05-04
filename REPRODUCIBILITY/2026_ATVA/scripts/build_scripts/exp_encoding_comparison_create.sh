#!/bin/bash

python_command=python3
min_val=1
max_val=10
step_size=1

if [[ $# -ge 4 ]]; then
    python_command=$1
    min_val=$2
    max_val=$3
    step_size=$4
fi

path_name="../../examples/EncodingComparison"

# Create directory structure if needed
mkdir -p "${path_name}/tree"
mkdir -p "${path_name}/smv_fastforwarding"
mkdir -p "${path_name}/smv_naive"
mkdir -p "${path_name}/results"
mkdir -p "${path_name}/processed_data"

# Generate binary tree .tree files
$python_command "${path_name}/create_binary_tree.py" "${path_name}/tree" $min_val $max_val $step_size

# Clean old generated files
rm -rf "${path_name}/smv_fastforwarding/nuxmv"
rm -rf "${path_name}/smv_naive/nuxmv"

# Generate SMV models with both encodings
for (( num=min_val; num<=max_val; num=(num + step_size) )); do
    echo "Processing binary_tree_$num..."

    # Generate with fastforwarding encoding (default optimized encoding)
    echo "  Generating fastforwarding encoding..."
    $python_command -m behaverify nuxmv \
        "${path_name}/tree/binary_tree_${num}.tree" \
        "${path_name}/smv_fastforwarding/" \
        --generate --use_encoding fastforwarding \
        --recursion_limit 5000 --no_checks --overwrite

    # Generate with naive encoding
    echo "  Generating naive encoding..."
    $python_command -m behaverify nuxmv \
        "${path_name}/tree/binary_tree_${num}.tree" \
        "${path_name}/smv_naive/" \
        --generate --use_encoding naive \
        --recursion_limit 5000 --no_checks --overwrite
done

echo "Build complete. SMV files generated in smv_fastforwarding/ and smv_naive/"
