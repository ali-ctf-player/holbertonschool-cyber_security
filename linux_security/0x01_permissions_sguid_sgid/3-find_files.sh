#!/bin/bash
find / -perm /6000 -exec ls -l {} + 2>/dev/null
