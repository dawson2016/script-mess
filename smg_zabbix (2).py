#!/usr/bin/env python
#coding:utf-8
##written by dawson @2016.03.30
#***********************************调用短信接口凭证和网址*****************
import sys
import urllib
import urllib2
postfix='【比比网络监控系统】'
uid,pwd='lizhijie','tdskj123'
status=sys.argv[2].decode('utf-8').encode('gb2312')
content=sys.argv[3].decode('utf-8').encode('gb2312')
postfix=postfix.decode('utf-8').encode('gb2312')
msg=status+' '+content+' '+postfix
phone_num=['13633445821','13111077788','13934572752']
mobile=phone_num[0]+';'+phone_num[1]+';'+phone_num[2]
#mobile=phone_num[0]
url = 'http://www.smsadmin.cn/smsmarketing/wwwroot/api/post_send/'
data ={'uid':uid,'pwd':pwd,'mobile':mobile,'msg':msg}	
data = urllib.urlencode(data)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
return_code = response.read()
print return_code
