#!/bin/bash
curl -s -H "Host: $1" -d "$3" "$2" -X "POST"
