#!/bin/bash
addgroup -f "$1"
chown :"$1" "$2"
chmod g=rx "$2"
