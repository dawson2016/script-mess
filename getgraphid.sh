#!/bin/sh
#written by dawson @2016.01.06
#ip=`echo $2|awk -F : '{print $1}'`
#item=`echo $2|awk -F : '{print $2}'`
#conn_mysql="mysql -uzabbix -pzabbix zabbix"
#sql1="select hostid from interface where ip='$ip'"
#a=`echo "${sql1}"|${conn_mysql} 2>/dev/null` 
#hostid=`echo $a|awk '{print $2}'`
#sql2="select itemid from items where hostid='$hostid' and name='$item'"
#a=`echo "${sql2}"|${conn_mysql} 2>/dev/null`
#itemid=`echo $a|awk '{print $2}'`
#sql3="select graphid from graphs_items where itemid='$itemid'"
#graphid=`echo "${sql3}"|${conn_mysql} 2>/dev/null`
#graphid=`echo $graphid|awk '{print $2}'`
#echo $graphid
#curl -so /tmp/$itemid.png 192.168.1.15/zabbix/chart2.php?graphid=$graphid
ip=`echo $2|awk -F : '{print $1}'`
item=`echo $2|awk -F : '{print $2}'`
conn_mysql="mysql -uzabbix -pzabbix zabbix"
sql1="select hostid from interface where ip='$ip'"
mya1=`echo "${sql1}"|${conn_mysql} 2>/dev/null`
hostid=`echo $mya1|awk '{print $2}'`
sql2="select itemid from items where hostid='$hostid' and name='$item'"
mya2=`echo "${sql2}"|${conn_mysql} 2>/dev/null`
itemid=`echo $mya2|awk '{print $2}'`
sql3="select graphid from graphs_items where itemid='$itemid'"
gphid1=`echo "${sql3}"|${conn_mysql} 2>/dev/null`
gphid2=`echo $gphid1|awk '{print $2}'`
echo $ip
echo $item
echo $mya1
echo $mya2
echo $hostid
echo $itemid
echo $gphid1
echo $gphid2
