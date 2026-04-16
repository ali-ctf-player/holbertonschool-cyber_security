#!/bin/bash
cat dmesg | grep Linux | grep version | cut -d']' -f2
