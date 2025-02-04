#!/bin/bash

password=$(cat /run/secrets/remote_server_password)
echo "root:${password}" | chpasswd
/usr/sbin/sshd -D
tail -f /dev/null
