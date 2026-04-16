#!/bin/bash
grep "useradd" auth.log | grep -o 'name=[^ ]*' | awk -F'[=,]' '{print $2}' | sort | uniq | tr '\n' ',' | sed 's/,$/\n/'
