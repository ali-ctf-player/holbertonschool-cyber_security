#!/bin/bash

# Check arguments
if [ -z "$1" ]; then
    echo "Usage: ./0-whois.sh <domain>"
    exit 1
fi

DOMAIN=$1
OUTPUT_FILE="${DOMAIN}.csv"

# Run whois and pipe to awk
whois "$DOMAIN" | awk -F':' '
BEGIN {
    # Define prefixes (Rows)
    prefix[1]="Registrant"
    prefix[2]="Admin"
    prefix[3]="Tech"

    # Define suffixes (Fields)
    suffix[1]="Name"
    suffix[2]="Organization"
    suffix[3]="Street"
    suffix[4]="City"
    suffix[5]="State/Province"
    suffix[6]="Postal Code"
    suffix[7]="Country"
    suffix[8]="Phone"
    suffix[9]="Phone Ext"
    suffix[10]="Fax"
    suffix[11]="Fax Ext"
    suffix[12]="Email"
}

{
    # $1 is the key (e.g., "Registrant Name"), $2 is the value
    # Trim leading/trailing whitespace from key and value
    key = $1
    val = $2
    gsub(/^[ \t]+|[ \t]+$/, "", key)
    gsub(/^[ \t]+|[ \t]+$/, "", val)

    # Store in associative array
    # If a key exists multiple times, this takes the last occurrence
    if (key != "") {
        db[key] = val
    }
}

END {
    count = 0
    total_lines = 3 * 12 # 3 sections * 12 fields

    for (i = 1; i <= 3; i++) {
        for (j = 1; j <= 12; j++) {
            
            # Construct the key to look up in our database
            # Example: "Registrant" + " " + "Name"
            lookupKey = prefix[i] " " suffix[j]
            
            # Retrieve value
            value = db[lookupKey]

            # Formatting Rule 1: Add space after Street fields
            if (suffix[j] == "Street") {
                value = value " "
            }

            # Construct the display label
            displayLabel = lookupKey
            
            # Formatting Rule 2: Include colon in Ext fields
            if (suffix[j] ~ /Ext/) {
                displayLabel = displayLabel ":"
            }

            # Print the formatted line
            # logic to avoid newline at the very end of the file
            count++
            if (count == total_lines) {
                printf "%s,%s", displayLabel, value
            } else {
                printf "%s,%s\n", displayLabel, value
            }
        }
    }
}' > "$OUTPUT_FILE"
