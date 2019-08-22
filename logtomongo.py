#!/usr/bin/env python
#coding:utf-8
from pymongo import *
import json
import re
regex = re.compile(r'\\(?![/u"])')
client = MongoClient('localhost', 27017)
db = client.weblogjson
collection = db.weblog
with open ('bitbidaccess.log','r+') as f:
        for i in f.readlines():
                i = regex.sub(r"\\\\",i)
                jlog=json.loads(i)
                jlog['time']=int(float(jlog['time']))
                if jlog['restime'] != "-" and  jlog['reqtime'] != "-":
                	jlog['reqtime']=int(float(jlog['reqtime'])*1000)
                	jlog['restime']=int(float(jlog['restime'])*1000)
                collection.insert_one(jlog)
