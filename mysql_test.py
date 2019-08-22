#!/usr/bin/env python
import MySQLdb
conn = MySQLdb.connect(host='localhost',user='zabbix',passwd='zabbix',db='zabbix')
cur = conn.cursor()
sql1="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
sql2="select from_unixtime(clock,'%%H:%%i:%%S'),value_avg from trends_uint where clock between unix_timestamp()-93600  and unix_timestamp() and itemid=%s"
loadlis=('23787','23674','23754','23667','23823')
memlis=('23660','23662','23663','23664','23820')
swaplis=('23680','23675','23679','23668','23824')
mysqlconlis=('23681','23806','23707','none','23815')
mysqlsellis=('23683','23804','23705','none','23813')
cpuidlelis=( '23787','23732','23745','23758','23830')
javaprolis=('none','23800','23799','23801','none')
num=5
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
print javapro
