#!/bin/sh

sleep 20
# run script
 python /config/main.py

# start cron
/usr/sbin/crond -f -l 8

