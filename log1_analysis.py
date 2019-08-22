#!/usr/bin/env python
#coding:utf-8
import commands
import threading
import sys
import json
from multiprocessing import Process,Manager,Pool
manager=Manager()
patter="cat 20160603.log |egrep 'HTTP/1.1\" 200|HTTP/1.1\" 301|HTTP/1.1\" 302'|grep -iEv 'HEAD|spider|bot|getTZ|roleid'|grep -icE "
subpatter="cat 20160603.log |egrep 'HTTP/1.1\" 200|HTTP/1.1\" 301|HTTP/1.1\" 302'|grep -iEv 'slurp|robot|HEAD|spider|bot|getTZ|roleid'|grep -i newsweb |grep -icE "
datalist = manager.list()
def log(x,y):
    d=commands.getoutput(patter+'"'+str(x)+'"')
    datadic={}
    datadic['name']=y
    datadic['value']=int(d)
    datalist.append(datadic)
def log1(x,y):
    d=commands.getoutput(subpatter+'"'+str(x)+'"')
    datadic={}
    datadic['name']=y
    datadic['value']=int(d)
    datalist.append(datadic)
threads = []
a=[('.','总计'),('/home/index.html',u'首页'),('GET / HTTP/1.1','主页'),('ggweb',u'招标公告'),('login',u'我的空间'),('aboutus',u'关于平台'),('memberinfo',u'会员须知'),('search',u'主页搜索框')]
b=[('type.401',u'项目库' ),('type.3002',u'政策法规'),('type.3001001',u'标准文件库'),('type.3001',u'下载中心'),
('type.101',u'新闻资讯'),('type.501',u'曝光台'),('type.201',u'行业动态'),('type.301',u'应用软件')]
for i in range(len(a)):
    t = Process(target=log,args=a[i])
    threads.append(t)
for i in range(len(b)):
    t = Process(target=log1,args=b[i])
    threads.append(t)
pool=Pool(8)
for t in threads:
    pool.apply_async(t)
    #t.start()
    t.close()
    t.join()
print datalist
