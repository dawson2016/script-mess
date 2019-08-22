#!/bin/bash
#预先过滤
cat bitbidaccess.log |egrep 'HTTP/1.1\" 200|HTTP/1.1\" 301|HTTP/1.1\" 302'|grep -iEv 'css|manager|png|upload|author|asp|js|php|admin|shtml|slurp|211.103.255.87|HEAD|spider|bot|getTZ|roleid'>111111.log &&
#去掉重复80
for i in  `awk '{acc[$1]++}END{for (i in acc) {print acc[i],i}}' 111111.log|awk -F ' ' '$1>=80{print $2}'`; do  sed -i /$i/d 111111.log; done &&
#生成ip 时间戳 访问路径
cat 111111.log |awk -F [' '[]+  '{print $1,$4,$7}'>222222.log &&
#转时间格式
sed -i -e 's/\//-/' -e 's/\//-/' -e 's/:/ /'  222222.log &&
#转换时间戳
cat 222222.log|cut -d ' ' -f 2,3|while read i; do a=`date +%s -d "${i}"`;sed -i "s/$i/$a/g"  222222.log; done &&
#数据入库
mysql -uroot  -p123456 -e "LOAD DATA LOCAL INFILE '/home/zabbix/222222.log' INTO TABLE log_analysis. web_access FIELDS TERMINATED BY ' ';"



