#!/usr/bin/env python
#coding:utf-8
import sys
import re
import json
regex = re.compile(r'\\(?![/u"])')
def jsonlog(log):
    log = regex.sub(r"\\\\",log)
    #jlog=json.loads(log)
    #if jlog['cookie']!='-' and jlog['cookie']:
    if '/home!getTZ.action' not in log and '"cookie": "-"' not in log and '"cookie": ""' not in log and '202.99.212.204'  in log and 'Hm_l' in log and 'JSESSIONID' not in log:
        return log
f = open(sys.argv[1],"r")
line = f.readlines()
#print len(line)
result=filter(jsonlog,line)
'''count=0
for i in line:
    i = regex.sub(r"\\\\",i)
    jlog=json.loads(i)
    if jlog['cookie']!='-' and jlog['cookie']:
        count+=1
        #print jlog['cookie']
print count'''
print len(result)
f.close()
