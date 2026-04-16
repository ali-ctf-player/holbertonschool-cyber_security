#!/bin/bash
grep -oP 'pam_unix\(\K[^)]+' auth.log* 2>/dev/null | \
cut -d: -f1 | sort | uniq -c | sort -rn
