#!/bin/bash
grep -vE '^#|^$' /etc/ssh/sshd_config
