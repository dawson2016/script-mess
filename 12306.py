#!/usr/bin/env python
#coding:utf-8
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def sendmail(data):
    message = MIMEText(data,'plain','utf-8')
    message['From'] = Header('Dawson','utf-8')
    message['To'] = Header('87075387@qq.com','utf-8')
    subject = '抢票'
    message['Subject'] = Header(subject,'utf-8')
    sender = '87075387@qq.com'  
    receiver = '87075387@qq.com'  
    subject = '12306'  
    smtpserver = 'smtp.qq.com'  
    username = '87075387@qq.com'  
    password = 'xhbocpgkubcabgbg'    
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.qq.com')  
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, message.as_string()) 
daytime=int(time.time())+86400
date=time.strftime('%Y-%m-%d', time.localtime(daytime))
checi='K868'
pattern = re.compile(checi)
URL = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station=TNV&leftTicketDTO.to_station=YPP&purpose_codes=ADULT"
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
res = requests.get(URL,verify=False)
resdic=json.loads(res.text)
reslist=resdic['data']['result']
print reslist['data']
for i in reslist:
	if re.findall(pattern,i):
		ticinfo = i.split('|')
		print ticinfo
		if ticinfo[11]=='Y':
			data='赶紧买！%s %s车次 一等座:%s,二等座:%s'%(date,checi,ticinfo[30],ticinfo[31])
                        #sendmail(data)
		else:
		    data=''
                    print 'no tickets',ticinfo[11]
