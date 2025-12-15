#!/bin/bash
sha256sum -c <<< "$2  $1" 2>&1 | grep -q "OK" && echo "$1: OK" || echo "$1: FAIL"
