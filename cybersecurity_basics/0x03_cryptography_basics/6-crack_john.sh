#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-SHA256 "$1" && john --show --format=Raw-SHA256 "$1" | head -n -2 | cut -d: -f2 > 6-password.txt
