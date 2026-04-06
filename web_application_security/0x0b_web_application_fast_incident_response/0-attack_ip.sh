#!/bin/bash
cat forensic.txt | cut -d' ' -f1 | grep '[.]' | sort | uniq -c | tail -1 | cut -d' ' -f5
