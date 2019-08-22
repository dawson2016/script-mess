#!/bin/sh
# mysql data backup script
# by liuxiaoping
# 2016-04-01
#
# use mysqldump --help ,get more detail.
#
BakDir=/data/db_backup
username=root
password=pw1234

DATE=`date +%Y%m%d`
for sql in $(cat "/home/bitbid/mysql.list")
  
    do
           if [ ! -d "/data/db_backup/$sql" ];then
              mkdir -p "/data/db_backup/$sql"
           fi
        LogFile=/data/db_backup/log/log.log 
        echo " " >> $LogFile
        echo " " >> $LogFile
        echo "-------------------------------------------" >> $LogFile
        echo $(date +"%y-%m-%d %H:%M:%S") >> $LogFile


        cd $BakDir

        DumpFile=${sql}_$DATE.sql

        mysqldump -h127.0.0.1  -u$username -p$password ${sql} > /data/db_backup/$sql/$DumpFile 
           
        echo "$sql Dump Done" >> $LogFile
        echo "-------------------------------------------" >> $LogFile
    done
