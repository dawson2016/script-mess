#!/usr/bin/env python
#coding:utf-8
from gevent import monkey; monkey.patch_all()
import sys
import requests
import time 
import random
import json
import hashlib
import gevent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ReadTimeout,ConnectionError,RequestException
import smtplib
from email.mime.text import MIMEText
from email.header import Header
default_encoding = 'utf-8'
MAIL_FROM = 'xxx@qq.com'
def smg(info):
    ran=random.randint(100000, 999999)
    sh=hashlib.sha256()
    smgurl='https://yun.tim.qq.com/v5/tlssmssvr/sendmultisms2?sdkappid=1400036582&random='+str(ran)
    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    ak='c37cb436ee7a250512c3ab47d54509cb'
    telnum="xxx"
    tel=["xxx"]
    mytime=int(time.time())
    mydata='appkey=dawc37cb436ee7a250512c3ab47d54509cbson&random='+str(ran)+'&time='+str(mytime)+'&mobile='+str(telnum)
    sh.update(mydata)
    mysig=sh.hexdigest()
    values = {"ext":"","extend":"","params": info,"sign": "短信签名","tel":[{"nationcode":"86", "mobile": pn} for pn in tel], "sig":mysig,"tpl_id": 231832,"time":mytime}
    myheaders = {"Content-Type": "application/json","User-Agent":user_agent }
    r = requests.post(url=smgurl,data=json.dumps(values),headers=myheaders)
    print r.content
def mysendmail(data,towho):
    message = MIMEText(data,'plain','utf-8')
    message['From'] = Header('huanshuo-URL-alert','utf-8')
    #message['To'] = Header(towho,'utf-8')
    subject = 'URL info'
    message['Subject'] = Header(subject,'utf-8')
    sender = 'xxx@qq.com'
    receiver = towho
    smtpserver = 'smtp.qq.com'
    username = '87075387@qq.com'
    password = 'dawdwienqivqfbxbifason'
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, message.as_string())
#data='\n'+str(sys.argv[1])+'\n'+str(sys.argv[2])
towho=['xxx@qq.com']
#mysendmail(data,towho)
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
IP='x.x.x.x'
urllist=['https://www.qq.com','https://www.baidu.com']
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def probe(URL):
    	try:
        	res = requests.get(URL,verify=False,timeout=10)
        	rescode = res.status_code
        	mytime=time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(time.time()))
        	print URL+' '+str(rescode)
        	if rescode > 500 :
            		data=str(URL)+' has down !! 返回码:'+str(rescode)
            		mysendmail(data,towho)
            		smg([URL,data,mytime,''])
            		print URL+' has down !!'
    	except Exception, e:
        	mytime=time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(time.time()))
        	data=str(URL)+' connection timeout !! 5S未响应'
        	mysendmail(data,towho)
        	print URL+' connection error !!'
async_time_start = time.time()
tasklist=[]
for i in urllist:
	tasklist.append(gevent.spawn(probe,i)
) 
gevent.joinall(tasklist)
print("异步cost",time.time()-async_time_start)
