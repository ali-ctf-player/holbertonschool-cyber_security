#!/bin/bash
len=${1}
tr -dc '[:alnum:]' < /dev/urandom | head -c "$len"
