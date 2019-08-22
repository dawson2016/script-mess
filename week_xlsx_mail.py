#!/usr/bin/env python
#coding:utf-8
import xlsxwriter
import time
import MySQLdb
import smtplib
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
sql1="select from_unixtime(clock,'%%Y-%%m-%%d'),value_avg from trends where clock between unix_timestamp()-604800  and unix_timestamp()  and  itemid=%s and (from_unixtime(clock,'%%H:%%i:%%S')='10:00:00' or from_unixtime(clock,'%%H:%%i:%%S')='16:00:00');"
sql2="select from_unixtime(clock,'%%Y-%%m-%%d'),value_avg from trends_uint where clock between unix_timestamp()-604800  and unix_timestamp()  and  itemid=%s and (from_unixtime(clock,'%%H:%%i:%%S')='10:00:00' or from_unixtime(clock,'%%H:%%i:%%S')='16:00:00');"
with xlsxwriter.Workbook('server_report_weekly.xlsx') as workbook:
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
    for i in range(1,17):
        worksheet.set_row(i,19)
    worksheet.merge_range('A1:U1', date_time+u'网站状况数据（一周）', merge_web_format)
    worksheet.write('A2',u'网址', merge_web_format)
    worksheet.write('A3',u'日期', merge_web_format)
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
            if len(poll_time)<14:
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
#绘制图表
    chart = workbook.add_chart({'type':'line'})
    chart.add_series({'values': '='+'web_status'+'!$C$4:$C$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'bitbid.home'})
    chart.add_series({'values': '='+'web_status'+'!$E$4:$E$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'bitbid.login'})
    chart.set_x_axis({'name':'bitbid-response time'})
    worksheet.insert_chart('A18', chart)
    chart1 = workbook.add_chart({'type':'line'})
    chart1.add_series({'values': '='+'web_status'+'!$G$4:$G$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'bibefc.home'})
    chart1.add_series({'values': '='+'web_status'+'!$I$4:$I$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'bibefc.login'})
    chart1.set_x_axis({'name':'bibefc-response time'})
    worksheet.insert_chart('G18', chart1)
    chart2 = workbook.add_chart({'type':'line'})
    chart2.add_series({'values': '='+'web_status'+'!$K$4:$K$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'gqcgbb.home'})
    chart2.add_series({'values': '='+'web_status'+'!$M$4:$M$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'gqcgbb.login'})
    chart2.set_x_axis({'name':'gqcgbb-response time'})
    worksheet.insert_chart('A33', chart2)
    chart3 = workbook.add_chart({'type':'line'})
    chart3.add_series({'values': '='+'web_status'+'!$O$4:$O$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'bibenet.home'})
    chart3.add_series({'values': '='+'web_status'+'!$S$4:$S$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'msop.bibefc'})
    chart3.set_x_axis({'name':'bibenet-response time'})
    worksheet.insert_chart('G33', chart3)
    chart4 = workbook.add_chart({'type':'line'})
    chart4.add_series({'values': '='+'web_status'+'!$Q$4:$Q$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'kempinski'})
    chart4.add_series({'values': '='+'web_status'+'!$U$4:$U$17','categories':'='+'web_status'+'!$A$4:$A$17','name':'cbpma.org.cn'})
    chart4.set_x_axis({'name':'kempinski-cbpma-response time'})
    worksheet.insert_chart('M18', chart4)

#编写服务器表，循环从监控ID中取值并加入数组
    for i in range(0,len(file_dic.get('hostip'))):
        ip=file_dic.get('hostip')[i]
        worksheet = workbook.add_worksheet(ip)
        worksheet.set_column('A:N', 13)
        worksheet.set_row(0, 30)
        for i in range(1,16):
            worksheet.set_row(i,19)
        #worksheet.set_row(1, 20)
        worksheet.merge_range('A1:N1', date_time+u' 服务器状况数据（一周）', merge_format)
        worksheet.write('A2', u'日期', merge_format)
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
#绘制图表
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({'values': '='+ip+'!$B$3:$B$16','categories':'='+ip+'!$A$3:$A$16','name':'cpu idle '})
        chart.add_series({'values': '='+ip+'!$D$3:$D$16','categories':'='+ip+'!$A$3:$A$16','name':'mem pused'})
        chart.add_series({'values': '='+ip+'!$E$3:$E$16','categories':'='+ip+'!$A$3:$A$16','name':'swap pused'})
        chart.add_series({'values': '='+ip+'!$K$3:$K$16','categories':'='+ip+'!$A$3:$A$16','name':'home free'})
        chart.set_x_axis({'name':'free cpu,/home& used mem,swap'})
        worksheet.insert_chart('A18', chart)
        chart1 = workbook.add_chart({'type': 'scatter','subtype':'straight_with_markers'})
        chart1.add_series({'values': '='+ip+'!$H$3:$H$16','categories':'='+ip+'!$A$3:$A$16','name':'mysql connect'})
        chart1.add_series({'values': '='+ip+'!$I$3:$I$16','categories':'='+ip+'!$A$3:$A$16','name':'mysql select pers'})
        chart1.add_series({'values': '='+ip+'!$J$3:$J$16','categories':'='+ip+'!$A$3:$A$16','name':'java process num'})
        chart1.set_x_axis({'name':'mysql & tomcat'})
        chart1.set_style(13)
        worksheet.insert_chart('A33', chart1) 
        chart2 = workbook.add_chart({'type': 'column'})
        chart2.add_series({'values': '='+ip+'!$M$3:$M$16','categories':'='+ip+'!$A$3:$A$16','name':'traffic-in'})
        chart2.add_series({'values': '='+ip+'!$N$3:$N$16','categories':'='+ip+'!$A$3:$A$16','name':'traffic-out'})
        chart2.set_x_axis({'name':'net-in/out'})
        worksheet.insert_chart('G18', chart2)
        chart3 = workbook.add_chart({'type': 'line'})
        chart3.add_series({'values': '='+ip+'!$C$3:$C$16','categories':'='+ip+'!$A$3:$A$16','name':'cpu load '})
        chart3.add_series({'values': '='+ip+'!$G$3:$G$16','categories':'='+ip+'!$A$3:$A$16','name':'disk io ops'})
        chart3.add_series({'values': '='+ip+'!$H$3:$H$16','categories':'='+ip+'!$A$3:$A$16','name':'disk io time'})
        chart3.set_x_axis({'name':'cpu load,disk ops&time'})
        worksheet.insert_chart('G33', chart3)

workbook.close()
cur.close()
conn.close()
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
    att1 = MIMEText(open('server_report_weekly.xlsx', 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="server_report_weekly.xlsx"'
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
        return False  
if send_mail(mailto_list,date_time+u"网站及服务器状态统计报告",str):  
    print ("ok")  
else:  
    print ("error")
