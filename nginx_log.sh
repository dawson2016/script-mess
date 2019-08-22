#!/bin/bash
LOGS_PATH=/usr/local/nginx/logs
YESTERDAY=$(date +%Y%m%d)
echo access${YESTERDAY}.log
mv ${LOGS_PATH}/access.log ${LOGS_PATH}/access${YESTERDAY}.log
kill -USR1 $(cat /usr/local/nginx/logs/nginx.pid)
