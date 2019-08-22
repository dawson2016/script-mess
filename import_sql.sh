#!/bin/bash
#cd ${WORKSPACE}
cd /home/zabbix/.jenkins/workspace/maven_test/
dir=`find . -name '*.api'`
rm -rf /home/zabbix/db/*
for i in $dir
  do
  #rm -rf /home/zabbix/db/*
  cp   $i/src/main/resources/dbscript*/*  /home/zabbix/db  
done
cd /home/zabbix/db
for j in `ls`
  do
  echo 'import',$j 
  mysql -uroot -p123456 -e "source $j"
  done

