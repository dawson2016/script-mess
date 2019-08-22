#!/usr/bin/env python
#coding:utf-8
#author:dawson@2018-04-27
import requests
import time
import json
import random
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#from PIL import Image
#from pytesseract import *
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
	
#def getyzm(pic):
#	image = Image.open(pic)
#	a=pytesseract.image_to_string(image)
#	b=a.replace(' ', '')
#	return b
	
def sendmail(data,towho):
	message = MIMEText(data,'plain','utf-8')
	message['From'] = Header('法宣小助手','utf-8')
	subject = '法宣自动学习软件进度报告'
	message['Subject'] = Header(subject,'utf-8')
	sender = '87075387@qq.com'
	receiver = towho
	smtpserver = 'smtp.qq.com'
	username = '87075387@qq.com'
	password = 'ndfcrppadodqbjie'
	smtp = smtplib.SMTP()
	smtp.connect('smtp.qq.com')
	smtp.ehlo()
	smtp.starttls()
	smtp.login(username, password)
	smtp.sendmail(sender, receiver, message.as_string())
	
def getrank():
	a=requests.get('http://xf.faxuan.net/pss/service/getdomainpoint?domainCode=100013003005122_1_10')
	data=a.content
	if len(data)<=10:
		title='get rank failed!!'
		return title
	l=[]
	title='历史积分排名 \n'
	for i in range(1,11):
		a=data[5:].split('{')[i].split(',')[1:4]
		b = unicode(a[0], "UTF-8")
		c = unicode(a[1], "UTF-8")
		d = unicode(a[2], "UTF-8")
		l.append(c[11:]+' '+b[13:]+' '+d[10:].replace('}',''))
	for i in l:
		data=i+'\n'
		title+=data
	return title

def getcookie():	
	resp = mysession.get(url=siteurl)
	cookiejar=resp.request._cookies
	mycookie={}
	for i in cookiejar:
		mycookie[i.name]=i.value 
	return mycookie

def myocr():
	time.sleep(3)
	r = mysession.get(codeurl,headers=myheaders)
	f = open('valcode.png', 'wb')
	f.write(r.content+"\n")
	f.close()
	#code=getyzm('/tmp/valcode.png')
	code=raw_input('yzm:')
	return code

	
tt=int(time.time())*1000
Stime=str(random.randint(10,20))
eScore=str(random.randint(30,80))
towho='87075387@qq.com','734630093@qq.com'
#towho='87075387@qq.com'
username='1403221220026'
password='1234qwer'
myheaders = {'Content-Type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

myheaders1 = {'Content-Type': 'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

mytimestamp=time.strftime('%a-%b-%d-%Y-%H:%M:%S', time.localtime()).replace('-','%20')+'%20GMT+0800'

mytimestamp_e=mytimestamp+'%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'

mysession = requests.Session()

siteurl='http://www.faxuan.net/bps/site/14/03/22.html'
codeurl='http://xf.faxuan.net/service/gc.html?tt='+str(tt)
#loginurl='http://www.faxuan.net/shop/api/xf_login?'
loginurl='http://www.faxuan.net/bss/xfservice/userService!doUserLogin.do?'
purl='http://xf.faxuan.net/pss/service/postPoint?'
mycookie=getcookie()
code=myocr()
loginurl='http://www.faxuan.net/bss/xfservice/userService!doUserLogin.do?userAccount=1403221220026&userPassword=1234qwer&code='+str(code)+'&rid='+str(mycookie['rid'])
data={'user_name':username,'user_pass':password,'code':code,'rid':mycookie['rid']}
r = mysession.get(loginurl,headers=myheaders1)
print r.text
sid=r.json()['data']['sid']
did=r.json()['data']['id']
dcode=r.json()['data']['domainCode']
ttpoint=r.json()['data']['todaytpoint']
tlpoint=r.json()['data']['todaylpoint']
tspoint=r.json()['data']['todayspoint']
tepoint=r.json()['data']['todayepoint']
mystatus='今天个人总积分情况: '+ttpoint+' 登陆积分: '+tlpoint+' 学习积分: '+tspoint+' 做题积分: '+tepoint+'\n'+getrank()
checkurl='http://www.faxuan.net/shop/api/add_use_lpoint?userAccount='+username+'&domainCode='+dcode+'&sid='+str(sid)
r= mysession.post(checkurl,headers=myheaders)
r= mysession.post(checkurl,headers=myheaders)
print r.content
def getpoint():	
	cookies={}
	cookies['loginUser']='%7B%22sid%22%3A%22'+str(sid)+'%22%2C%22id%22%3A%22'+str(did)+'%22%7D'
	sdata={'operateType':'spoint','userAccount':username,'domainCode':dcode,'ssid':str(sid),'stime':Stime,'timestamp':mytimestamp}
	
	edata={'operateType':'epoint','userAccount':username,'domainCode':dcode,'ssid':str(sid),'exerScore':eScore,'timestamp':mytimestamp_e,'expointValue':'0'}
	
	r = requests.get(purl,headers=myheaders,cookies=cookies,params=sdata)
	r = requests.get(purl,headers=myheaders,cookies=cookies,params=edata)
getpoint()
getpoint()
getpoint()
sendmail(mystatus,towho)