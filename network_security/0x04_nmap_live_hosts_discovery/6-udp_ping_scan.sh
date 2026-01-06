#!/bin/bash
sudo nmap $1 -PU53,161,162 -sn
