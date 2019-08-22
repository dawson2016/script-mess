#!/usr/bin/env python
#coding=utf8
#w 文件内容：
'''admin admin
   dawson 123
   zabbix zabbi'''
f=file('w')
a=f.readlines()
f.close()
l=file('lock')
b=l.readlines()
l.close()
while 1:
    account=0
    name=raw_input('input your name ').strip()    
    for i in a:
        if name == i.split()[0] and name+'\n' not in b:
            account=1
            code=i.split()[1]
            break
    if account==1:
        break
    else:
        print 'this account is not exist or been locked,try again!'
level=0
while level<3:                
    account=0
    passwd=raw_input('input your passwd ').strip()    
    level+=1
    for i in a:
        if passwd == code:
            account=1
            print 'welcom %s login the system'% name
            break
    if account==1:
        break
    else:
        print 'you have '+str(3-level)+ ' chance'
if 3-level==0:
    lock=file('lock','a')
    lock.write(name+'\n')
    lock.close()
    #lock the name
    print 'this account has been locked!!!' 
