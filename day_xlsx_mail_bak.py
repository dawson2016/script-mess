#!/usr/bin/env python
#coding:utf-8
import xlsxwriter
import time
import MySQLdb
import smtplib
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
sql1="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
sql2="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends_uint where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
loadlis=['23671','23674','23754','23667','23823']
memlis=('23660','23662','23663','23664','23820')
swaplis=('23680','23675','23679','23668','23824')
mysqlconlis=('23681','23806','23707','none','23815')
mysqlsellis=('23683','23804','23705','none','23813')
cpuidlelis=('23787','23732','23745','23758','23830')
javaprolis=('none','23800','23799','23801','none')
with xlsxwriter.Workbook('server_report_daily.xlsx') as workbook:
    conn = MySQLdb.connect(host='localhost',user='zabbix',passwd='zabbix',db='zabbix')
    cur = conn.cursor()
    ip=['192.168.1.15','192.168.1.17','192.168.1.18','192.168.1.14','192.168.1.13','192.168.10.11','192.168.10.12','192.168.10.14','192.168.10.16','192.168.10.17','192.168.10.18','192.168.10.19']
    for num  in range(0,5):     
        worksheet = workbook.add_worksheet(ip[num])
        bold=workbook.add_format({'bold':True})
        worksheet.set_column('A:H', 12)
        worksheet.set_row(0, 60)
        date_format=workbook.add_format({'num_format':'hh:mm:ss'})
        okcolor_format=workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','bg_color':'66FF66'})
        errcolor_format=workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','bg_color':'FF3333'})
        merge_format = workbook.add_format({
        'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
        worksheet.merge_range('A1:H1', date_time+u' 服务器状况数据（24小时）', merge_format)
        worksheet.write('A2', u'时间', merge_format)
        worksheet.write('B2', u'CPU15负载',merge_format)
        worksheet.write('C2', u'内存空间(M)',merge_format)
        worksheet.write('D2', u'SWAP空间(M)',merge_format)
        worksheet.write('E2', u'数据库连接',merge_format)
        worksheet.write('F2', u'每秒查询数',merge_format)
        worksheet.write('G2', u'CPU空闲率%',merge_format)
        worksheet.write('H2', u'java进程数',merge_format)
        time=[]
        cpu=[]
        cur.execute(sql1,loadlis[num])
        for i,j in cur.fetchall():
        	time.append(i)
                cpu.append(j)
        mem=[]
 	cur.execute(sql2,memlis[num])
	for i,j in cur.fetchall():
  		mem.append(j/1024/1024)
	swap=[]
	cur.execute(sql2,swaplis[num])
	for i,j in cur.fetchall():
  		swap.append(j/1024/1024)
	mysqlcon=[]
	cur.execute(sql2,mysqlconlis[num])
	for i,j in cur.fetchall():
  		mysqlcon.append(j)
	mysqlsel=[]
	cur.execute(sql2,mysqlsellis[num])
	for i,j in cur.fetchall():
  		mysqlsel.append(j)
	cpuidle=[]
	cur.execute(sql1,cpuidlelis[num])
	for i,j in cur.fetchall():
  		cpuidle.append(j)
	javapro=[]
	cur.execute(sql2,javaprolis[num])
	for i,j in cur.fetchall():
  		javapro.append(j)

        worksheet.write_column('A3',time ,date_format)
        worksheet.write_column('B3',cpu)
        worksheet.conditional_format('B3:B27',{'type':'cell','criteria': 'greater than','value': 5,'format': errcolor_format}) 
        worksheet.conditional_format('B3:B27',{'type':'cell','criteria': 'less than','value': 5,'format': okcolor_format}) 
        worksheet.write_column('C3',mem)
        worksheet.conditional_format('C3:C27',{'type':'cell','criteria': 'greater than','value': 3200,'format': okcolor_format}) 
        worksheet.conditional_format('C3:C27',{'type':'cell','criteria': 'less than','value': 3200,'format': errcolor_format}) 
        worksheet.write_column('D3',swap)
        worksheet.conditional_format('D3:D27',{'type':'cell','criteria': 'greater than','value': 6400,'format': okcolor_format}) 
        worksheet.conditional_format('D3:D27',{'type':'cell','criteria': 'less than','value': 6400,'format': errcolor_format}) 
        worksheet.write_column('E3',mysqlcon)
        worksheet.conditional_format('E3:E27',{'type':'cell','criteria': 'greater than','value': 500,'format': errcolor_format}) 
        worksheet.conditional_format('E3:E27',{'type':'cell','criteria': 'less than','value': 500,'format': okcolor_format}) 
        worksheet.write_column('F3',mysqlsel)
        worksheet.conditional_format('F3:F27',{'type':'cell','criteria': 'greater than','value': 100,'format': errcolor_format}) 
        worksheet.conditional_format('F3:F27',{'type':'cell','criteria': 'less than','value': 100,'format': okcolor_format}) 
        worksheet.write_column('G3',cpuidle)
        worksheet.conditional_format('G3:G27',{'type':'cell','criteria': 'greater than','value': 20,'format': okcolor_format}) 
        worksheet.conditional_format('G3:G27',{'type':'cell','criteria': 'less than','value': 20,'format': errcolor_format}) 
        worksheet.write_column('H3',javapro)
        '''worksheet.conditional_format('H3:H27',{'type':'cell','criteria': 'greater than','value': 0,'format': okcolor_format}) 
        worksheet.conditional_format('H3:H27',{'type':'cell','criteria': 'less than','value': 1,'format': errcolor_format})''' 
    '''chart = workbook.add_chart({'type': 'line'})
    chart.add_series({'values': '=192.168.1.15!$B$3:$B$25',
     'categories':'=192.168.1.15!$A$3:$A$25','name':'cpu load 15min'})
    chart.set_x_axis({'name':'cpu load 15min'})
    worksheet.insert_chart('G3', chart)'''

workbook.close()
cur.close()
conn.close()
'''
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
mailto_list=["dawson.dong@bibenet.com","xp.liu@bibenet.com"] 
mail_host="mail.bibenet.com"
mail_user="zabbix@bibenet.com"
mail_pass="s9v5h3j7"    

def send_mail(to_list,sub,content): 
    me="dawson.dong"+"<"+mail_user+">" 
    msg = MIMEMultipart() 
    att1 = MIMEText(open('server_report_daily.xlsx', 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="server_report_daily.xlsx"'
    msg.attach(att1)
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
if send_mail(mailto_list,date_time+u"服务器状态统计报告",str):  
    print ("ok")  
else:  
    print ("error")
'''
