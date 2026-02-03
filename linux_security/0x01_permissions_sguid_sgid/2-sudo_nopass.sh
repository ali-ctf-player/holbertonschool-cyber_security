#!/bin/bash
tee /etc/sudoers.d/"$1" <<< "$1 ALL=(ALL) NOPASSWD: ALL"
