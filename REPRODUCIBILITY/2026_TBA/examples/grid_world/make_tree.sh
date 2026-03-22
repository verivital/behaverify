#!/bin/bash

# Modes to iterate over
modes=("table" "fixed 140 48" "fixed 100 35" "float 140")
#modes=("fixed 100 35")

# Directory containing network files
network_dir="./networks"

# Template file
template="./template.tree"

# Output directory for generated files
output_dir="./tree"
mkdir -p "$output_dir"

# Iterate over each mode
for mode in "${modes[@]}"; do
    # Iterate over each file in the networks directory
    for file in "$network_dir"/*; do
        # Extract the base name of the file
        base_name=$(basename "$file")
        split_name="${base_name%%.*}"
        # Construct the output file name
        output_file="$output_dir/${mode// /_}_${split_name}.tree"
        
        # Replace placeholders and write to the output file
        sed -e "s/REPLACE_CONFIG/$mode/g" -e "s|REPLACE_SOURCE|$file|g" "$template" > "$output_file"

        echo "Generated: $output_file"
    done
done
