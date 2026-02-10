#!/bin/bash
find / -type d -perm -0002 2>/dev/null
find / -type d -perm -0002 -exec chmod 755 {} + 2>/dev/null
