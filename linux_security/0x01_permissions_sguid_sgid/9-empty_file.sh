#!/bin/bash
find "$1" -size 0 -type f -exec chmod 777 2>/dev/null
