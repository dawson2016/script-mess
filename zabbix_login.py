#!/usr/bin/env python
#coding:utf-8
import sys
import urllib
import cookielib
import urllib2
cookiejar=cookielib.CookieJar()
urlOpener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
url='http://192.168.1.15:83/zabbix/dashboard.php'
values={"name":'admin','password':'dawson','autologin':1,"enter":'Signin'}
data=urllib.urlencode(values)
request=urllib2.Request(url,data)
try:
    urlOpener.open(request,timeout=10)
except urllib2.HTTPError,e:
            print e
response=urllib2.urlopen(request)
print response.read()

