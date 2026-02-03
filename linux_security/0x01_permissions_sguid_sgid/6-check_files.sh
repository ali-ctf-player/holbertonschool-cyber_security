#!/bin/bash
find "$1" -perm /6000 -mtime 0 -exec ls -la {} + 2>/dev/null
