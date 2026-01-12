#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 {xor}HASH"
    exit 1
fi

# Remove the {xor} prefix if present
encoded_string="${1#\{xor\}}"

# 1. Decode from Base64
# 2. Use 'tr' or a loop to XOR each byte with '_' (95)
# Using perl for a clean one-liner XOR operation
echo "$encoded_string" | base64 -d | perl -pe '$_ ^= "_" x length'
echo "" # Add a newline to match your output example
