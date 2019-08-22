#!/usr/bin/env python
#coding:utf-8
from pymongo import *
import json
import re
regex = re.compile(r'\\(?![/u"])')
client = MongoClient('localhost', 27017)
db = client.weblogjson
collection = db.weblog
print collection.find({"time":{'$gt':1481472000 ,'$lt':1481482000}}).count()
