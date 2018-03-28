#!/bin/bash
# Script to connect to mysql

echo "Connecting to mysql"
mysql -u myuser -p1234 -h 10.0.5.33 ir_db << EOF
SELECT * FROM action
EOF


