#!/bin/bash
nmap $1 --script http-vuln-cve2017-5638 -oN vuln_scan_results.txt
