#!/bin/bash
# Script to do a ping sweep of a given target IP range

COUNTER=1

while [ $COUNTER -lt 254 ]
do
 ping 10.0.5.$COUNTER -c 1 | grep "bytes from" | cut -d " " -f 4 | cut -d ":" -f 1 &
 COUNTER=$(( $COUNTER + 1 ))
done
