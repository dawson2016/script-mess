#!/usr/bin/env python
#coding:utf-8
#written by dawson @2016.06.22
import MySQLdb
import json
import re
regex = re.compile(r'\\(?![/u"])')  
conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="weblog_json",charset="utf8")  
cursor = conn.cursor()   
with open ('bitbidaccess.log','r+') as f:
	for i in f.readlines():
                #i="".join([i.strip().rsplit("}",1)[0],"}"])
                fixed = regex.sub(r"\\\\",i)
                jlog=json.loads(fixed)
       	        sql = "insert into weblog(clock,ip,referer,reqmethod,reqtime,website,status,bytes,agent,cookie,restime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"   
       		param = (jlog['time'],jlog['ipaddr'],jlog['referer'],jlog['reqmethod'],jlog['reqtime'],jlog['url'],jlog['status'], jlog['bytes'],jlog['agent'],jlog['cookie'],jlog['restime'])    
        	cursor.execute(sql,param)

conn.close()
