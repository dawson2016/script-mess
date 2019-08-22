#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
db = MySQLdb.connect("","","","" )
cursor = db.cursor()
cursor.execute("show tables")
count=0
data = cursor.fetchall()
for i in list(data):
    #print list(i)
    cursor.execute("select count(*) from "+list(i)[0])
    a=int(list(cursor.fetchone())[0])
    count+=a
print count 
db.close()
