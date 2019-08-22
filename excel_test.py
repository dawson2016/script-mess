#!/usr/bin/python
#coding: utf-8
'''from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import easyxf
import os
excel=r'test.xls'
rb=open_workbook(excel,formatting_info=True)
wb=copy(rb)
sheet=wb.get_sheet(0)
sheet.write(6,2,15)
os.remove(excel)
wb.save(excel)
'''
import time
import MySQLdb
import smtplib
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
sql1="select from_unixtime(clock,'%%H:%%i:%%S'),value_max from trends where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
sql2="select from_unixtime(clock,'%%H:%%i:%%S'),value_max from trends_uint where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"

filedic={'hostip':['192.168.1.15','192.168.1.17','192.168.1.18','192.168.1.14','192.168.1.13','192.168.10.11','192.168.10.12','192.168.10.14','192.168.10.16','192.168.10.17','192.168.10.18','192.168.10.19'],
'items':['cpuidlelist','cpuloadlist','memusedlist','swapusedlist','ioopslist','iomslist','mysqlconlist','mysqlqpslist','javaprolist','diskfreelist','usernumlist','netinlist','netoutlist'],
'192.168.1.15':['24030','24040','24055','24052','24060','24061','24043','24044','24435','24073','24070','24068','24069'],
'192.168.1.17':['24077','24086','24094','24091','24346','24347','23689','23690','24477','24110','24109','24107','24108'],
'192.168.1.18':['24114','24123','24131','24128','24358','24359','23707','23705','24482','24147','24146','24144','24145'],
'192.168.1.13':['24151','24160','24168','24165','24370','24371','none','none','24487','24184','24183','24181','24182'],
'192.168.1.14':['24188','24196','24205','24202','24382','24383','23815','23813','24472','24221','24220','24218','24219'],
'192.168.10.11':['24225','24234','24242','24239','24394','24395','23856','23852','23946','24258','24257','24255','24256'],
'192.168.10.12':['24262','24271','24279','24276','24406','24407','24738','24739','24732','24295','24294','24292','24293'],
'192.168.10.14':['24299','24308','24316','24313','24418','24419','23874','23870','24737','24332','24331','24329','24330'],
'192.168.10.16':['24557','24566','24711','24571','24576','24577','24531','24532','24594','24527','24586','24584','24585'],
'192.168.10.17':['24595','24604','24714','24609','24614','24615','24538','24539','24632','24528','24624','24622','24623'],
'192.168.10.18':['24633','24642','24717','24647','24652','24653','none','none','24670','24529','24662','24660','24661'],
'192.168.10.19':['24671','24680','24720','24685','24690','24691','none','none','24708','24530','24700','24698','24699']}
#print filedic.get('hostip')
#for i in range(0,len(filedic.get('hostip'))):
for i in range(0,1):
    ip=filedic.get('hostip')[i]
    #print filedic.get('hostip')[i]
    conn = MySQLdb.connect(host='localhost',user='zabbix',passwd='zabbix',db='zabbix')
    cur = conn.cursor()
    row_num=65
    poll_time=[]
    for j in filedic.get('192.168.1.15'):
        data=[] 
        if cur.execute(sql1,j)==0:
            cur.execute(sql2,j)
        for t,d in cur.fetchall():
            if len(poll_time)<24:
                poll_time.append(t)
            if isinstance(d,long):
                data.append(d/1024/1024)
            else:
                data.append(d)
        row_num+=1
        print chr(row_num)
        print data 
    print poll_time 
