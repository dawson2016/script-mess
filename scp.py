#!/usr/bin/env python 
#coding:utf-8
import paramiko
import time
now = int(time.time())-86400
timearray=time.localtime(now)
prefix=time.strftime("%Y%m%d", timearray)
localpath='/home/zabbix/bitbidaccess.log'
t = paramiko.Transport(('221.204.173.165',23789))
t.connect(username='bitbidroot', password='xv$djw3964T{H\z3TpDo')
sftp=paramiko.SFTPClient.from_transport(t)
src= '/usr/local/nginx/logs/access'+prefix+'.log'
sftp.get(src,localpath)
t.close()
