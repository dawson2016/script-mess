#!/usr/bin/env python
#coding:utf-8
#realtime time log
import time
import redis
import json
import urllib2
rc = redis.Redis(host='192.168.1.15',port=6379) 
def ipool(ip):
        url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='+ip
        postdata = urllib2.urlopen(url).read()
        jsondata = json.loads(postdata)
        if jsondata['ret'] != -1:
            city = jsondata['city']
        else:
            city=u'局域网' 
        return  city
f = open("/var/log/nginx/access.log", "r")
f.seek(0, 2)
while True:
    offset = f.tell()
    line = f.readline()
    if not line:
        f.seek(offset)
        time.sleep(0.1)
    else:
        #ip = re.search(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',line).group()
        ip=line.split(' ')[0]
        actime=line.split(' ')[3].split('/')[2].split(':',1)[1]
        web=line.split(' ')[6]
        res=line.split('"')[3]
        client=line.split('"')[5]
        #print ip,actime,web 
        rc.publish("fm110",[ipool(ip),actime,web,res,client])
f.close()
