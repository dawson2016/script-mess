#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:dawson
import requests
import time,json,sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def getrank():
	a=requests.get('http://xf.faxuan.net/pss/service/getdomainpoint?domainCode=100013003005122')
	data=a.content
	if len(data)<=10:
		title='get rank failed!!'
		return title
	l=[]
	#return data[5:].split('{')[i].split(',')[1:4]
	title='历史积分排名 \n'
	for i in range(1,11):
		a=data[5:].split('{')[i].split(',')[:4]
		#print a
		b = unicode(a[0], "UTF-8")
		c = unicode(a[2], "UTF-8")
		d = unicode(a[3], "UTF-8")
		#print b,c,d
		#l.append(c[11:]+' '+b[13:]+' '+d[10:].replace('}',''))
		l.append(b[9:].strip('"')+' '+c[11:]+' '+d[8:].replace('}',''))
		#print l
	for i in l:
		data=i+'\n'
		title+=data
	return title
print getrank()