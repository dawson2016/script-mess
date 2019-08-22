#!/usr/bin/env python
#coding:utf-8
import commands
import threading
import sys
import json
import smtplib  
import time
from email.mime.text import MIMEText  
from email.header import Header  
pingip="ping -c 4 "
pingurlpre="curl -so/dev/null "
pingurlpos=" -w '%{http_code}\n'"
datalist = []
lock=threading.Lock()
def ping_ip(x):
    global datalist
    d=commands.getoutput(pingip+'"'+str(x)+'"')
    #print d
    lock.acquire()
    datalist.append(d)
    lock.release()
def ping_url(x):
    global datalist
    d=commands.getoutput(pingurlpre+'"'+str(x)+'"'+pingurlpos)
    y=x+" status code: "+d
    #print y
    lock.acquire()
    datalist.append(y)
    lock.release()
threads = []
a=[('221.204.177.103',),('221.204.177.104',),('221.204.177.105',)]
b=[('http://ys.gqcgbb.com',),('http://192.168.1.9:9080/home/index.html',),('http://msop.bibefc.com',),('http://www.cbpma.org.cn/index.html',),('http://www.bibenet.com/index.html',),('http://www.bibefc.com',),('http://www.gqcgbb.com',),('http://kempinski.gqcgbb.com',),('https://cedp.gqcgbb.com/login.jsp?',),('https://fin.bibefc.com/login.jsp',),('http://www.bitbid.cn/user/toLogin/logintype_1.html',),('https://msop.gqcgbb.com/login.htm',),('http://www.bitbid.cn',),('https://cas.gqcgbb.com/login',)]
for i in range(len(a)):
    t = threading.Thread(target=ping_ip,args=a[i])
    threads.append(t)
for i in range(len(b)):
   t = threading.Thread(target=ping_url,args=b[i])
   threads.append(t)
for t in threads:
    t.start()
    t.join(10)
#print datalist

sender = 'zabbix@bibenet.com'  
#receiver = 'dawson.dong@bibenet.com';'zabbix@bibenet.com'  
to_list=["dawson.dong@bibenet.com","xinliang.tian@bibenet.com","junjun.hao@bibenet.com","jieqiang.chen@bibenet.com","jianguo.che@bibenet.com","494641724@qq.com"]
#to_list=["dawson.dong@bibenet.com"]
subject = 'zabbix report'  
smtpserver = 'mail.bibenet.com'  
username = 'zabbix@bibenet.com'  
password = 'Zabbix_@173163.com'    
msg = MIMEText('\n'.join(datalist),'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要  
msg['Subject'] = ('ip web test '+time.strftime("%Y-%m-%d,%H:%M:%S"))  
#msg['to'] = receiver  
msg['From'] = sender  
msg['To'] = ";".join(to_list)
smtp = smtplib.SMTP()  
smtp.connect('mail.bibenet.com')  
smtp.login(username, password)  
#smtp.sendmail(sender, receiver, msg.as_string()) 
smtp.sendmail(sender, to_list, msg.as_string()) 
