#!/bin/bash
ps aux -u "$1" -o pid,user,comm,vsz,rss | grep -v "     0      0"
