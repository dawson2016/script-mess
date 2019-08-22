#!/usr/bin/env python
#coding:utf-8
import subprocess 
import threading
import sys
import json
shellcmd="cat 201606031.log |egrep 'HTTP/1.1\" 200|HTTP/1.1\" 301|HTTP/1.1\" 302'|grep -iEv 'HEAD|spider|bot|getTZ|roleid'|awk '{acc[$1]++}END{for (i in acc) {print i,acc[i]}}'"
datalist = []
def log():
    d=subprocess.Popen(shellcmd,shell=False)
    #print y,d
    #datadic={}
    #datadic['name']=y
    #datadic['value']=int(d)
    datalist.append(d)
'''
datalist = []
threads = []
for i in range(len(a)):
    t = threading.Thread(target=log,args=a[i])
    threads.append(t)
for t in threads:
    t.start()
    t.join()
'''
#print datadic
#f=open('web.json','w+')
#print >> f,json.dumps(datalist)
#f.close()
log()
print datalist
