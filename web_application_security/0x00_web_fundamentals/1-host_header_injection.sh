#!/bin/bash
curl -s -H "Host: $1" -d "$2" "$3" -X "POST"
