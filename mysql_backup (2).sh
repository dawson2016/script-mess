#!/bin/sh
# mysql data backup script
# by liuxiaoping
# 2016-04-01
#
# use mysqldump --help ,get more detail.
#
#Sqllist=`more /usr/mysqljiaoben/mysql.list`
BakDir=/opt/mysql/mysql-5.6.24-linux-glibc2.5-x86_64/bin/
username=root
password=pw1234

DATE=`date +%Y%m%d`
#n=()
#m=0
for sql in $(cat "/home/mysql/mysql.list")
  
    do
        #Path="/usr/data/db_backup/$sql"
           if [ ! -d "/usr/local/data/db_backup/$sql" ];then
              mkdir -p "/usr/local/data/db_backup/$sql"
           fi
        LogFile=/usr/local/data/db_backup/log/log.log 
        echo " " >> $LogFile
        echo " " >> $LogFile
        echo "-------------------------------------------" >> $LogFile
        echo $(date +"%y-%m-%d %H:%M:%S") >> $LogFile


        cd $BakDir

        DumpFile=${sql}_$DATE.sql

        ./mysqldump -h127.0.0.1  -u$username -p$password ${sql} > /usr/local/data/db_backup/$sql/$DumpFile 
         
             #if [ $? -ne 0 ];then
             #  echo "$sql backup error" >> $LogFile
             #  /usr/mysqljiaoben/smg_zabbix.py 
                   
             #fi
           
        echo "$sql Dump Done" >> $LogFile
        echo "-------------------------------------------" >> $LogFile
    done
