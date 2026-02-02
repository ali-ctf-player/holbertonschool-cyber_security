#!/bin/bash
hashcat -m 0 "$1" /usr/share/wordlists/rockyou.txt --force && hashcat -m 0 "$1" --show | cut -d: -f2 > 7-password.txt

