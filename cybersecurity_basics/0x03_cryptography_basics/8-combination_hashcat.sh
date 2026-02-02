#!/bin/bash
hashcat -a 1 "$1" "$2" --stdout
