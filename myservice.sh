#!/bin/bash
# Script to connect to any open port

MACHINE=$1
PORT=$2
exec 3>/dev/tcp/${MACHINE}/${PORT}
if [ $? -eq 0 ]
then
    echo "Telnet accepting connections"
else
    echo "Telnet connections not possible"
fi

