#!/usr/bin/env python
#coding: utf-8  
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
mailto_list=["dawson.dong@bibenet.com"] 
mail_host="mail.bibenet.com"
mail_user="zabbix@bibenet.com"
mail_pass="s9v5h3j7"    

def send_mail(to_list,sub,content): 
    me="dawson.dong"+"<"+mail_user+">" 
    msg = MIMEMultipart('alternative') 
    att1 = MIMEText(open('test99.py', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="report.xlsx"'
    msg.attach(att1)
    html = """
    <!doctype html>
<html>
<head>
   <meta charset="utf-8">
    <style type="text/css">
			div{
			width:700px;
			height:500px;
			margin:0 auto;
			position:relative;
		}
		.bg{
			display:block;
			width:700px;
			height:400px;
			margin:0 auto;
		}
		.bg img{
			width:700px;
		}
		.btn{
			text-decoration:none;
			display:block;
			width:150px;
			height:50px;
			line-height:50px;
			text-align:center;
			background-color:#0e8edf;
			color:#fff;
			font-size:16px;
			font-weight:bold;
			border-radius:8px;
			position:absolute;
			top:450px;;
			right:273px;
		}	
    </style>
</head>
<body>
    <div>
    	<img src="cid:image1"/>
        <a class="btn" href="http://192.168.1.15/graph.html">点击进入</a>
    </div>
</body>
</html>
 """ 
    part1=MIMEText(html,'html','utf-8')
    msg.attach(part1)
    fp = open('chart.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())  
        s.close()  
        return True  
    except Exception:  
        #print (str(e))  
        return False  
#if __name__ == '__main__':  

if send_mail(mailto_list,u"服务器状态统计报告",str):  
    print ("ok")  
else:  
    print ("error")
