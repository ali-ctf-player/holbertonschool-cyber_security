#!/bin/bash
ps -u "$1" -o pid,user,comm,vsz,rss | grep -v "     0      0"
