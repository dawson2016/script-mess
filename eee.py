#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:dawson
import requests
import time,json
tt=int(time.time())*1000
print tt
myheaders = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

myheaders1 = {'Content-Type': 'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}
mysession = requests.Session()
siteurl='http://hdpx.webtrn.cn/center/'
resp = mysession.get(url=siteurl)
cookiejar=resp.request._cookies
cookiejar=mysession.cookies
mycookie={}
for i in cookiejar:
	mycookie[i.name]=i.value
print mycookie
loginurl='http://hdpx.webtrn.cn/center/center/login_login.action?d='+str(tt)+'&loginId=sxxy1601260&passwd=21218cca77804d2ba1922c33e0151105&auto=false&into=0'
resp = mysession.post(url=loginurl)
print resp.content
print mysession.cookies
#time.sleep(2)

#dataurl='http://hdpx.webtrn.cn/entity/first/userDefinedQuery_getBySql.action?'

dataurl='http://hdpx.webtrn.cn/entity/first/userDefinedQuery_getBySql.action?t='+str(tt)+'&jsoncallback=jQuery111305477290629707694_'+str(tt)+'&queryId=newWorkSpace_queryScore'
data={'classTempId':'ff808081577583e60157a399d67c668e'}
resp = mysession.post(url=dataurl,data=json.dumps(data),headers=myheaders)
print resp.content
print mysession.cookies