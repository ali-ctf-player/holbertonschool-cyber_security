#!/bin/bash
echo -n "$1" | sha256sum > 1_hash.txt
