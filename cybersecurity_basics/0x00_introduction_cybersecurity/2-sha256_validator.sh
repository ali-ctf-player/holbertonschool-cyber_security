#!/bin/bash
hash=$(sha256sum $1 | awk '{print $1}');[ "$hash" = "$2" ] && echo "$1: OK" || echo "$1: FAIL"
