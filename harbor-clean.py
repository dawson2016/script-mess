#!/usr/bin/env python
#coding:utf-8
import requests
url='https://xxx/api/repositories?project_id=5'
durl='https://xxx/api/repositories/'
postfix='/tags?detail=1'
response  = requests.get(url)
s = requests.session()
data = {'principal':'xxx','password':'xxx'}
loginres=s.post('https://xxx/login',data=data)
global null
null = ''
for i in eval(response.content):
	if i['tags_count']>3:
		response1  = requests.get(durl+i['name']+postfix)
		res1=response1.content
		resdata=[]
		for j in eval(res1):
			resdata.append(j['name'])
		resdata.sort()
		resdata.reverse()
		for k in resdata[3:]:
			delurl=durl+i['name']+'/tags/'+str(k)
			s.delete(delurl)

