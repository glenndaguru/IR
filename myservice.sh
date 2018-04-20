#!/bin/bash
# Script to connect to any open port

MACHINE=$1
PORT=$2
nmap ${MACHINE} -p ${PORT}
	

