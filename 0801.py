#!/usr/bin/env python
#coding:utf-8
import xlsxwriter
import time
import MySQLdb
#主机以及WEB监控项ID写在字典里
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
sql1="select clock,data  from dyti "
with xlsxwriter.Workbook('maillist'+date_time+'.csv') as workbook:
#定义excel单元格以及字体格式
#开始编写web工作表
    worksheet = workbook.add_worksheet('bibiwang.cn')
    worksheet.write('A1',u'name')
    worksheet.write('B1',u'mail')
#从数据库取值
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='server')
    cur = conn.cursor()
    row_num=65
    cur.execute(sql1)
    name=[]
    data=[]
    user=[]
    for t,d in cur.fetchall():
        name.append(t)
        data.append(d)
    user.append(name)
    user.append(data)
    worksheet.write_column('A2',user[0])
    worksheet.write_column('B2',user[1])
workbook.close()
cur.close()
conn.close()
