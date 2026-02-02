#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt "$1" --format=nt && john --show --format=nt "$1" | head -n -2 | cut -d: -f2 > 5-password.txt
