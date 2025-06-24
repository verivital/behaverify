#!/bin/bash

# Fail on any error
set -e

# Check if argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <path>"
    exit 1
fi

TARGET_PATH="$1"
PARENT_DIR="$(dirname "$TARGET_PATH")"

# Expand tilde (~) to home directory
PARENT_DIR="${PARENT_DIR/#\~/$HOME}"

# Check if TARGET_PATH exists
if [ -e "$TARGET_PATH" ]; then
    echo "Error: '$TARGET_PATH' already exists."
    exit 1
fi

# Check if parent directory exists and is a directory
if [ -e "$PARENT_DIR" ]; then
    if [ ! -d "$PARENT_DIR" ]; then
        echo "Error: Parent '$PARENT_DIR' exists but is not a directory."
        exit 1
    fi
else
    # Create parent directories
    mkdir -p "$PARENT_DIR"
fi

# Create python virtual environment
python3 -m venv "${TARGET_PATH}"
"${TARGET_PATH}/bin/python3" -m pip install -r ./requirements/all.txt


