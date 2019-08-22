#!/usr/bin/env python 
#coding:utf-8
import paramiko
import time
#now = int(time.time())-86400
now = int(time.time())
#now = int(time.time())
timearray=time.localtime(now)
prefix=time.strftime("%Y%m%d", timearray)
localpath='/usr/local/data/enterprise_bidding.sql'
t = paramiko.Transport(('192.168.10.6',22))
t.connect(username='root', password='M(;RQ[S*FyY&A(rCwHl5')
sftp=paramiko.SFTPClient.from_transport(t)
src= '/data/db_backup/enterprise_bidding/enterprise_bidding_'+prefix+'.sql'
sftp.get(src,localpath)
t.close()
