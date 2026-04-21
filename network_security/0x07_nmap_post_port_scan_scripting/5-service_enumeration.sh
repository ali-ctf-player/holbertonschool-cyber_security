#!/bin/bash
nmap -A -sV --script banner default ssl-enum-ciphers smb-enum-domains $1 -oN service_enumeration_results.txt
