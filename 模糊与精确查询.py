#!/usr/bin/env python
#conding=utf-8
''' user.txt
zabbix zabbix  13333333
jay 123  13333333    admin
admin admin  1333333  admi
dawson 123   13333333  adm
'''
user={}
with open ('user.txt') as F:
    a=F.readlines()
    F.close()
    for i in a:
        b=i.split()
        user[b[0]]=b[1:]
time=0
while time<3:
#while 1:
    find=raw_input('please input the name you want to search :')
    time+=1
    info=0
    if len(find)<3:
        print 'please input lease 3 words'
        continue
    for i,j in user.items():
        if i.count(find)!=0 or j.count(find)!=0:
            print i,'-'.join(j)
            info+=1    
    break
if info!=0:
    print 'total ' +str(info)+' record'
else:
    print 'without any infomation'
#=========================  fuzzy query
    #g=user.get(find)
    #if g==None:continue
    #    print'this name is not exist,please try again! only '+str(3-time)+' chance'
   # else:
    #    break
#if g!=None and time>0:
   # value=user[find]
   # print 'this is the information of the '+ find +':'+str(value)
#===============precise query    
