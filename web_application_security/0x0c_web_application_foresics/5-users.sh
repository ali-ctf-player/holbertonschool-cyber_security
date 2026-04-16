#!/bin/bash
grep "iptables" auth.log | grep "INPUT" | wc -l
