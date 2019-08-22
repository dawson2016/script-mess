#!/usr/bin/env python 
#coding: utf-8  
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
  
sender = 'zabbix@bibenet.com'  
receiver = 'dawson.dong@bibenet.com'  
subject = 'zabbix report'  
smtpserver = 'mail.bibenet.com'  
username = 'zabbix@bibenet.com'  
password = 'Zabbix_@173163.com'    
msg = MIMEText('你好','text','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
msg['Subject'] = Header(subject, 'utf-8')  
smtp = smtplib.SMTP()  
smtp.connect('mail.bibenet.com')  
smtp.login(username, password)  
smtp.sendmail(sender, receiver, msg.as_string()) 
