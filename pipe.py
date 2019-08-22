#!/usr/bin/env python
#coding:utf-8
import subprocess  
import json
import urllib2 
import re
regex = re.compile(r'\\(?![/u"])')
def sinaip(ip):
        url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='+ip
        postdata = urllib2.urlopen(url).read()
        jsondata = json.loads(postdata)
        if jsondata['ret'] != -1:
            city = jsondata['city']
            if jsondata['city']=="":
                city=u'未知'
        else:
            city=u'北京'
        return  city

popen = subprocess.Popen('tail -f /usr/local/nginx/logs/access.log', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
while True:
    line=popen.stdout.readline().strip()
    line = regex.sub(r"\\\\",line)
    line=json.loads(line)
    print sinaip(line["ipaddr"])
