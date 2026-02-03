#!/bin/bash
sudo echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/"$1"
