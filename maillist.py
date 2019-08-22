#!/usr/bin/env python
#coding:utf-8
import xlsxwriter
import time
import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
file_dic={'hostip':['192.168.1.15','192.168.1.17','192.168.1.18','192.168.1.14','192.168.1.13','192.168.10.11','192.168.10.12','192.168.10.14','192.168.10.16','192.168.10.17','192.168.10.18','192.168.10.19'],
'items':['cpuidlelist','cpuloadlist','memusedlist','swapusedlist','ioopslist','iomslist','mysqlconlist','mysqlqpslist','javaprolist','diskfreelist','usernumlist','netinlist','netoutlist'],
'192.168.1.15':['24030','24040','24055','24052','24060','24061','24043','24044','24435','24073','24070','24068','24069'],
'192.168.1.17':['24077','24086','24094','24091','24346','24347','23689','23690','24477','24110','24109','24107','24108'],
'192.168.1.18':['24114','24123','24131','24128','24358','24359','23707','23705','24482','24147','24146','24144','24145'],
'192.168.1.14':['24151','24160','24168','24165','24370','24371','none','none','24487','24184','24183','24181','24182'],
'192.168.1.13':['24188','24196','24205','24202','24382','24383','23815','23813','24472','24221','24220','24218','24219'],
'192.168.10.11':['24225','24234','24242','24239','24394','24395','23856','23852','23946','24258','24257','24255','24256'],
'192.168.10.12':['24262','24271','24279','24276','24406','24407','24738','24739','24732','24295','24294','24292','24293'],
'192.168.10.14':['24299','24308','24316','24313','24418','24419','23874','23870','24737','24332','24331','24329','24330'],
'192.168.10.16':['24557','24566','24711','24571','24576','24577','24531','24532','24594','24527','24586','24584','24585'],
'192.168.10.17':['24595','24604','24714','24609','24614','24615','24538','24539','24632','24528','24624','24622','24623'],
'192.168.10.18':['24633','24642','24717','24647','24652','24653','none','none','24670','24529','24662','24660','24661'],
'192.168.10.19':['24671','24680','24720','24685','24690','24691','none','none','24708','24530','24700','24698','24699'],
'web_url':['bitbid.cn/login','gqcgbb.com/login','up.bibefc.com','bibefc.com','bibenet.com','gqcgbb.com','bitbid.cn'],
'web_itemid':['24520','24505','24526','24511','24523','24508','24514','24758','24755','24752']
}
#主机以及WEB监控项ID写在字典里
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
sql1="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
sql2="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends_uint where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
with xlsxwriter.Workbook('server_report_daily.xlsx') as workbook:
#定义excel单元格以及字体格式
    date_format=workbook.add_format({'num_format':'hh:mm:ss'})
    okcolor_format=workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','bg_color':'98FB98'})
    errcolor_format=workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter','bg_color':'CD2626'})
    merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
    merge_web_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '98FB98'})
    bold=workbook.add_format({'bold':True})
#开始编写web工作表
    worksheet = workbook.add_worksheet('web_status')
    worksheet.set_column('A:U', 12)
    worksheet.set_row(0,30)
    for i in range(1,28):
        worksheet.set_row(i,19)
    #worksheet.set_row(1,20)
    worksheet.merge_range('A1:U1', date_time+u'网站状况数据（24小时）', merge_web_format)
    worksheet.write('A2',u'网址', merge_web_format)
    worksheet.write('A3',u'采集时间', merge_web_format)
    worksheet.merge_range('B2:C2',u'bitbid首页',merge_web_format)
    worksheet.write('B3',u'状态码', merge_web_format)
    worksheet.write('C3',u'响应时间S', merge_web_format)
    worksheet.merge_range('D2:E2',u'bitbid登录页',merge_web_format)
    worksheet.write('D3',u'状态码', merge_web_format)
    worksheet.write('E3',u'响应时间S', merge_web_format)
    worksheet.merge_range('F2:G2',u'bibefc首页',merge_web_format)
    worksheet.write('F3',u'状态码', merge_web_format)
    worksheet.write('G3',u'响应时间S', merge_web_format)
    worksheet.merge_range('H2:I2',u'bibefc登录页',merge_web_format)
    worksheet.write('H3',u'状态码', merge_web_format)
    worksheet.write('I3',u'响应时间S', merge_web_format)
    worksheet.merge_range('J2:K2',u'gqcgbb首页',merge_web_format)
    worksheet.write('J3',u'状态码', merge_web_format)
    worksheet.write('K3',u'响应时间S', merge_web_format)
    worksheet.merge_range('L2:M2',u'gqcgbb登录页',merge_web_format)
    worksheet.write('L3',u'状态码', merge_web_format)
    worksheet.write('M3',u'响应时间S', merge_web_format)
    worksheet.merge_range('N2:O2',u'bibenet首页',merge_web_format)
    worksheet.write('N3',u'状态码', merge_web_format)
    worksheet.write('O3',u'响应时间S', merge_web_format)
    worksheet.merge_range('P2:Q2',u'kempinski首页',merge_web_format)
    worksheet.write('P3',u'状态码', merge_web_format)
    worksheet.write('Q3',u'响应时间S', merge_web_format)
    worksheet.merge_range('R2:S2',u'msop登录页',merge_web_format)
    worksheet.write('R3',u'状态码', merge_web_format)
    worksheet.write('S3',u'响应时间S', merge_web_format)
    worksheet.merge_range('T2:U2',u'cbpma首页',merge_web_format)
    worksheet.write('T3',u'状态码', merge_web_format)
    worksheet.write('U3',u'响应时间S', merge_web_format)
#从数据库取值
    conn = MySQLdb.connect(host='localhost',user='zabbix',passwd='zabbix',db='zabbix')
    cur = conn.cursor()
    row_num=65
    poll_time=[]
    for id in file_dic.get('web_itemid'):
        code=[]
        restime=[]
        row_num+=1
        cur.execute(sql2,id)
        for t,d in cur.fetchall():
            if len(poll_time)<=24:
                poll_time.append(t)
            code.append(d)
        worksheet.write_column(chr(row_num)+'4',code)
        rowid=chr(row_num)+'4'+':'+chr(row_num)+'28'
        worksheet.conditional_format(rowid,{'type':'data_bar'})
        worksheet.conditional_format(rowid,{'type':'cell','criteria': '>','value': 200, 'format': errcolor_format})
        row_num+=1
        cur.execute(sql1,str(int(id)-1))
        for t,r in cur.fetchall():
            restime.append(round(r,2))
        worksheet.write_column(chr(row_num)+'4',restime)
        rowid=chr(row_num)+'4'+':'+chr(row_num)+'28'
        worksheet.conditional_format(rowid,{'type':'data_bar'})
    worksheet.write_column('A4',poll_time ,date_format)
#编写服务器表，循环从监控ID中取值并加入数组
    for i in range(0,len(file_dic.get('hostip'))):
        ip=file_dic.get('hostip')[i]
        worksheet = workbook.add_worksheet(ip)
        worksheet.set_column('A:N', 13)
        worksheet.set_row(0, 30)
        for i in range(1,27):
            worksheet.set_row(i,19)
        #worksheet.set_row(1, 20)
        worksheet.merge_range('A1:N1', date_time+u' 服务器状况数据（24小时）', merge_format)
        worksheet.write('A2', u'采集时间', merge_format)
        worksheet.write_column('A3',poll_time ,date_format)
        worksheet.write('B2', u'CPU空闲率%',merge_format)
        worksheet.write('C2', u'CPU负载值',merge_format)
        worksheet.write('D2', u'内存使用率%',merge_format)
        worksheet.write('E2', u'SWAP使用率%',merge_format)
        worksheet.write('F2', u'磁盘IO操作数',merge_format)
        worksheet.write('G2', u'磁盘IO时间s',merge_format)
        worksheet.write('H2', u'MYSQL连接数',merge_format)
        worksheet.write('I2', u'MYSQL每秒查询',merge_format)
        worksheet.write('J2', u'TOMCAT进程数',merge_format)
        worksheet.write('K2', u'HOME剩余%',merge_format)
        worksheet.write('L2', u'当前登录用户数',merge_format)
        worksheet.write('M2', u'网卡进流量G',merge_format)
        worksheet.write('N2', u'网卡出流量G',merge_format)
#从数据库获取数据
        row_num=65
        for j in file_dic.get(ip):
            data=[]
            row_num+=1
            if cur.execute(sql1,j)==0:
                cur.execute(sql2,j)
            for t,d in cur.fetchall():
                if row_num in [66,67,68,69,75]:
                    data.append(round(d,2))
                elif row_num in [77,78]:
                    data.append(d/1024/1024/1024)
                elif row_num in [71]:
                    data.append(d/1000)
                else:
                    data.append(d)
            worksheet.write_column(chr(row_num)+'3',data)
#指定条件格式范围3-27
            rowid=chr(row_num)+'3'+':'+chr(row_num)+'27'
            worksheet.conditional_format(rowid,{'type':'data_bar'})
workbook.close()
cur.close()
conn.close()
#from email.mime.text import MIMEText
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
mailto_list=["dawson.dong@bibenet.com","liuxiaoping@bibenet.com","shijy@bibenet.com"] 
#mailto_list=["dawson.dong@bibenet.com"] 
mail_host="mail.bibenet.com"
mail_user="zabbix@bibenet.com"
mail_pass="s9v5h3j7"    

def send_mail(to_list,sub,content): 
    me="dawson.dong"+"<"+mail_user+">" 
    msg = MIMEMultipart() 
    fo=open('server_report_daily.xlsx', 'rb')
    #att1 = MIMEText(open('server_report_daily.xlsx', 'rb').read(), 'base64', 'gb2312')
    att1 = MIMEText(fo.read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="server_report_daily.xlsx"'
    msg.attach(att1)
    fo.close()
    html="""
<html lang="en">
<head>
    <style type="text/css">
		div{
			width:700px;
			height:400px;
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
			top:357px;;
			right:273px;
		}
    </style>
</head>
<body>
    <div>
    	<a  href="http://192.168.1.15/graph.html"><img src="cid:image1"/></a>
        <a class="btn" href="http://192.168.1.15/graph.html">点击进入</a>
    </div>
</body>
</html>
    """
    part1=MIMEText(html,'html','utf-8')
    msg.attach(part1)
    #fp = open('chart.png','rb')
    #msgImage = MIMEImage(fp.read())
    #fp.close()
    #msgImage.add_header('Content-ID', '<image1>')
    #msg.attach(msgImage)
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
        return False  
if send_mail(mailto_list,date_time+u"网站及服务器状态统计报告",str):  
    print ("ok")  
else:  
    print ("error")
