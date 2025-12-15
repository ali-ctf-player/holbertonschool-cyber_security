#!/bin/bash
sha256sum -c <<< "$2  $1" >/dev/null 2>&1 && echo "$1: OK" || echo "$1: FAIL"
