#!/bin/sh

sleep 20
# run script
 python3 /config/vaccine_script.py

# start cron
/usr/sbin/crond -f -l 8

