#!/bin/bash
echo "$1" -n | sha1sum > 0_hash.txt
