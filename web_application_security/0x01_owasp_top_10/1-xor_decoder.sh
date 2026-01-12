#!/bin/bash

# XOR WebSphere Password Decoder
# WebSphere uses {xor} encoded passwords with a simple XOR operation

if [ $# -ne 1 ]; then
    echo "Usage: $0 <xor_hash>"
    echo "Example: $0 '{xor}KzosKw=='"
    exit 1
fi

# Extract the base64 part (remove {xor} prefix)
if [[ "$1" =~ ^{xor}(.+)$ ]]; then
    encoded="${BASH_REMATCH[1]}"
else
    echo "Error: Input must start with '{xor}' prefix"
    exit 1
fi

# Decode base64
base64_decoded=$(echo -n "$encoded" | base64 -d 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Invalid base64 encoding"
    exit 1
fi

# XOR each character with 0x5F (WebSphere's XOR key)
decoded=""
for (( i=0; i<${#base64_decoded}; i++ )); do
    char="${base64_decoded:$i:1}"
    # Get ASCII value, XOR with 0x5F, convert back to char
    ascii_val=$(printf "%d" "'$char")
    xor_val=$((ascii_val ^ 0x5F))
    decoded_char=$(printf "\\$(printf '%03o' "$xor_val")")
    decoded="${decoded}${decoded_char}"
done

# Output the decoded password
echo "$decoded"
