#!/bin/bash
iptables -A INPUT -p tcp --dport ssh -j ACCEPT
iptables -P INPUT -j DROP
