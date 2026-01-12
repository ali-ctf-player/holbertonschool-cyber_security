#!/bin/bash

NEW_HOST=$1
TARGET_URL=$2
FORM_DATA=$3

curl -s -H "Host: $NEW_HOST" -d "$FORM_DATA" "$TARGET_URL" -X "POST"
