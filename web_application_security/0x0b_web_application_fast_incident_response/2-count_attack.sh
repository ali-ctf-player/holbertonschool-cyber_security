#!/bin/bash
cat logs.txt | cut -d' ' -f1 | grep '[.]' | sort | uniq -c | tail -1 | cut -d' ' -f4
