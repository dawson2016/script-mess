#!/bin/bash
sudo kill  `ps aux|grep -iv grep|grep cedp|awk -F ' ' '{print $2}'`
cd ${WORKSPACE}
find . -name *.war -exec cp {} /home/zabbix/wars \;
sh /home/zabbix/cedp/bin/startup.sh

