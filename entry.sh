#!/bin/sh

sleep 5
mv /tmp/* /config/

#sh /config/git_installer.sh

sleep 20
# run script
python /config/main.py -a

# start cron
/usr/sbin/crond -f -l 8

